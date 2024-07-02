import subprocess
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from math import ceil
from youtube_transcript import extract_transcript
from modes import fetch_modes, fetch_prompt
import logging

class OllamaClient:
    def __init__(self, repo_url):
        self.repo_url = repo_url.rstrip('/')
        self.console = Console()
        self.modes = fetch_modes(self.repo_url)
        self.current_mode = None
        self.chat_history = []

        logging.basicConfig(filename='ollama_client.log', level=logging.DEBUG)

    def set_mode(self, mode):
        if mode in self.modes:
            self.current_mode = mode
            self.chat_history = []  # Clear chat history when changing modes
            self.console.print(f"[bold green]Mode set to:[/bold green] {mode}")
            logging.debug(f"Mode set to: {mode}")
        else:
            self.console.print(f"[bold red]Invalid mode.[/bold red] Available modes: {', '.join(self.modes.keys())}")

    def get_response(self, model, prompt):
        MAX_TOKENS = 8000  # Llama 3 token limit

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

        system_prompt = fetch_prompt(self.repo_url, self.current_mode)
        full_prompt = f"{system_prompt}\n\n{prompt}"

        # Truncate the prompt if it exceeds the maximum token limit
        if len(full_prompt.split()) > MAX_TOKENS:
            truncated_prompt = ' '.join(full_prompt.split()[:MAX_TOKENS])
            full_prompt = truncated_prompt + "\n[Content truncated due to length]"

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
                    self.console.clear()
                    self.console.print(Markdown(result))
                    self.console.print(f"[bold cyan]Current Mode: {self.current_mode}[/bold cyan]")
            rc = process.poll()
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
            self.search_results = results
        else:
            self.console.print(f"[bold red]No modes found matching '{query}'.[/bold red]")
