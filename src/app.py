import os
import requests
import subprocess
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from math import ceil
from youtube_transcript import extract_transcript  # Import the new module

class OllamaClient:
    def __init__(self, repo_url):
        self.repo_url = repo_url.rstrip('/')
        self.console = Console()
        self.modes = self.fetch_modes()
        self.current_mode = None
        self.chat_history = []

    def fetch_modes(self):
        api_url = f"{self.repo_url}/contents/patterns"
        headers = {
            'Authorization': f'token {os.getenv("GITHUB_API_KEY")}'
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            modes = {item['name']: item['name'] for item in data if item['type'] == 'dir'}
            return modes
        else:
            self.console.print(f"[bold red]Failed to fetch modes from repository. Status code: {response.status_code}[/bold red]")
            return {}

    def fetch_prompt(self, mode):
        api_url = f"{self.repo_url}/contents/patterns/{mode}/system.md"
        headers = {
            'Authorization': f'token {os.getenv("GITHUB_API_KEY")}'
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            content = requests.get(data['download_url']).text
            return content
        else:
            self.console.print(f"[bold red]Failed to fetch prompt for mode '{mode}'. Status code: {response.status_code}[/bold red]")
            return ""

    def set_mode(self, mode):
        if mode in self.modes:
            self.current_mode = mode
            self.console.print(f"[bold green]Mode set to:[/bold green] {mode}")
        else:
            self.console.print(f"[bold red]Invalid mode.[/bold red] Available modes: {', '.join(self.modes.keys())}")

    def get_response(self, model, prompt):
        if not self.current_mode:
            self.console.print("[bold red]Please set a mode before making a request.[/bold red]")
            return

        if prompt.startswith("yt "):
            video_url = prompt.split(" ", 1)[1]
            self.console.print("[bold blue]Extracting transcript from YouTube video...[/bold blue]")
            transcript = extract_transcript(video_url)
            if "Error" in transcript:
                self.console.print(f"[bold red]{transcript}[/bold red]")
                return
            else:
                self.console.print("[bold green]Transcript extracted successfully.[/bold green]")
                prompt = transcript

        # Concatenate chat history with the new prompt
        system_prompt = self.fetch_prompt(self.current_mode)
        full_prompt = "\n".join(self.chat_history) + f"\n{system_prompt} {prompt}"
        command = f"ollama run {model} '{full_prompt}'"

        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            result = ""
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    result += output.strip() + "\n"
                    # Clear the console before rendering updated Markdown to avoid formatting issues
                    self.console.clear()
                    self.console.print(Markdown(result))
            rc = process.poll()

            # Update chat history with the latest interaction
            self.chat_history.append(f"{system_prompt} {prompt}")
            self.chat_history.append(result.strip())

            return result
        except subprocess.CalledProcessError as e:
            self.console.print(f"[bold red]Command error:[/bold red] {e.stderr}")

    def display_modes(self, page=1, per_page=30):
        modes_list = list(self.modes.keys())
        total_pages = ceil(len(modes_list) / per_page)

        if page > total_pages or page < 1:
            self.console.print(f"[bold red]Invalid page number. Please enter a number between 1 and {total_pages}.[/bold red]")
            return

        table = Table(title="Available Modes")
        table.add_column("No.", justify="right", style="cyan", no_wrap=True)
        table.add_column("Mode", style="magenta")
        table.add_column("No.", justify="right", style="cyan", no_wrap=True)
        table.add_column("Mode", style="magenta")
        table.add_column("No.", justify="right", style="cyan", no_wrap=True)
        table.add_column("Mode", style="magenta")

        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        rows = [modes_list[i:i+10] for i in range(start_index, end_index, 10)]

        for i in range(10):
            row = []
            for col in range(3):
                if len(rows) > col and len(rows[col]) > i:
                    row.append(str(start_index + col * 10 + i + 1))
                    row.append(rows[col][i])
                else:
                    row.append("")
                    row.append("")
            table.add_row(*row)

        self.console.clear()
        self.console.print(table)
        self.console.print(f"Page {page}/{total_pages}")

    def search_mode(self, query):
        results = [mode for mode in self.modes.keys() if query.lower() in mode.lower()]
        if results:
            table = Table(title="Search Results")
            table.add_column("No.", justify="right", style="cyan", no_wrap=True)
            table.add_column("Mode", style="magenta")

            for i, mode in enumerate(results, start=1):
                table.add_row(str(i), mode)

            self.console.clear()
            self.console.print(table)
            self.search_results = results  # Save search results for selection mapping
        else:
            self.console.print(f"[bold red]No modes found matching '{query}'.[/bold red]")

def main():
    repo_url = 'https://api.github.com/repos/danielmiessler/fabric'
    client = OllamaClient(repo_url)
    model = 'llama3'
    current_page = 1

    while True:
        client.console.print("Select a mode:")
        client.display_modes(current_page)
        client.console.print("Type 'next' for next page, 'prev' for previous page, 'search <query>' to search, or enter the mode number.")
        
        while True:
            mode_choice = input("Enter your choice: ").strip()
            if mode_choice.startswith("search "):
                query = mode_choice.split("search ", 1)[1]
                client.search_mode(query)
                client.console.print("Type 'next' for next page, 'prev' for previous page, 'search <query>' to search, or enter the mode number.")
            elif mode_choice == 'next':
                current_page += 1
                client.display_modes(current_page)
                client.console.print("Type 'next' for next page, 'prev' for previous page, 'search <query>' to search, or enter the mode number.")
            elif mode_choice == 'prev':
                current_page -= 1
                client.display_modes(current_page)
                client.console.print("Type 'next' for next page, 'prev' for previous page, 'search <query>' to search, or enter the mode number.")
            else:
                try:
                    mode_index = int(mode_choice) - 1
                    if hasattr(client, 'search_results'):  # Check if search results are available
                        mode = client.search_results[mode_index]
                    else:
                        mode = list(client.modes.keys())[mode_index]
                    client.set_mode(mode)
                    break  # Break out of the outer loop to go to the inner loop for prompts
                except (ValueError, IndexError):
                    client.console.print("[bold red]Invalid choice. Please try again.[/bold red]")
                    client.console.print("Type 'next' for next page, 'prev' for previous page, 'search <query>' to search, or enter the mode number.")

        while True:
            client.console.print("\nEnter your prompt, or type 'new chat' to start a new chat, 'change mode' to switch modes, or 'exit' to quit:")
            prompt = input().strip()
            if prompt.lower() == 'new chat':
                client.chat_history = []
                client.console.print("[bold blue]Chat history cleared. Start a new conversation.[/bold blue]")
            elif prompt.lower() == 'change mode':
                break
            elif prompt.lower() == 'exit':
                client.console.print("[bold red]Exiting the application.[/bold red]")
                return
            else:
                response = client.get_response(model, prompt)

if __name__ == "__main__":
    main()
