
![logo](image.png)
# Mockingbird - Ollama Client

Ollama Client is a Python-based application designed to interface with the Ollama model to generate responses based on different prompts. It can extract transcripts from YouTube videos, use them as input, and manage multiple modes of operation. The application is modular, with components handling different aspects of its functionality.

## Features

- **Mode Selection:** Choose from various pre-defined modes to set the context for the responses.
- **YouTube Transcript Extraction:** Extract and use transcripts from YouTube videos as input prompts.
- **Streaming Responses:** Display responses in real-time as they are generated.
- **Markdown Rendering:** Format and display responses using Markdown for better readability.
- **Command-Line Interface:** User-friendly command-line interface for easy interaction.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/ollama-client.git
   cd ollama-client
   ```

2. **Install Poetry:**

   If you don't have Poetry installed, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).

3. **Install dependencies:**

   ```sh
   poetry install
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add your GitHub API key:

   ```env
   GITHUB_API_KEY=your_github_api_key
   ```

## Usage

1. **Run the application:**

   ```sh
   poetry run python main.py
   ```

2. **Select a mode:**

   The application will display a list of available modes. Use the number corresponding to the mode to select it. You can also use `next` and `prev` to navigate through pages of modes or `search <query>` to find a specific mode.

3. **Enter your prompt:**

   After selecting a mode, you can enter your prompt. To use a YouTube video transcript as the prompt, type `yt <YouTube URL>`.

4. **Commands:**

   - `new chat`: Start a new conversation and clear the chat history.
   - `change mode`: Switch to a different mode.
   - `exit`: Exit the application.

## Project Structure

```plaintext
/path/to/project
│
├── main.py                  # Entry point for the application
├── modes.py                 # Mode fetching and management
├── ollama_client.py         # Main application logic
└── youtube_transcript.py    # YouTube transcript extraction
```

## Example

1. **Start the application:**

   ```sh
   poetry run python main.py
   ```

2. **Select a mode:**

   ```plaintext
   Select a mode:
   ┏━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ No. ┃ Mode             ┃ No. ┃ Mode                         ┃ No. ┃ Mode                           ┃
   ┡━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │   1 │ agility_story    │  11 │ analyze_personality          │  21 │ ask_secure_by_design_questions │
   │   2 │ ai               │  12 │ analyze_presentation         │  22 │ capture_thinkers_work          │
   │   3 │ analyze_answers  │  13 │ analyze_prose                │  23 │ check_agreement                │
   │   4 │ analyze_claims   │  14 │ analyze_prose_json           │  24 │ clean_text                     │
   │   5 │ analyze_debate   │  15 │ analyze_prose_pinker         │  25 │ coding_master                  │
   │   6 │ analyze_incident │  16 │ analyze_spiritual_text       │  26 │ compare_and_contrast           │
   │   7 │ analyze_logs     │  17 │ analyze_tech_impact          │  27 │ create_5_sentence_summary      │
   │   8 │ analyze_malware  │  18 │ analyze_threat_report        │  28 │ create_academic_paper          │
   │   9 │ analyze_paper    │  19 │ analyze_threat_report_trends │  29 │ create_ai_jobs_analysis        │
   │  10 │ analyze_patent   │  20 │ answer_interview_question    │  30 │ create_aphorisms               │
   └─────┴──────────────────┴─────┴──────────────────────────────┴─────┴────────────────────────────────┘
   Page 1/4
   Type 'next' for next page, 'prev' for previous page, 'search <query>' to search, or enter the mode number.
   Enter your choice: 1
   ```

3. **Enter a prompt:**

   ```plaintext
   Enter your prompt, or type 'new chat' to start a new chat, 'change mode' to switch modes, or 'exit' to quit:
   yt https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

   The application will extract the transcript from the provided YouTube video and use it as the prompt.

## License

This project is licensed under the MIT License.

---

Feel free to customize this README further according to your needs.
