from ollama_client import OllamaClient

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
                    if hasattr(client, 'search_results'):
                        mode = client.search_results[mode_index]
                    else:
                        mode = list(client.modes.keys())[mode_index]
                    client.set_mode(mode)
                    break
                except (ValueError, IndexError):
                    client.console.print("[bold red]Invalid choice. Please try again.[/bold red]")
                    client.console.print("Type 'next' for next page, 'prev' for previous page, 'search <query>' to search, or enter the mode number.")

        while True:
            client.console.print(f"\n[bold cyan]Current Mode: {client.current_mode}[/bold cyan]")
            client.console.print("Enter your prompt, or type 'new chat' to start a new chat, 'change mode' to switch modes, or 'exit' to quit:")
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
