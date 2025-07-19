
# ChatGPT Link Converter

A simple, cross-platform Python tool to convert one or more ChatGPT share links into high-quality PDF files. It preserves the full conversation, including images, tables, and expandable "thinking traces."

## Features

- **High-Quality PDFs:** Renders pages with a real browser engine for perfect fidelity.
- **Cross-Platform:** Works on Windows, macOS, and Linux.
- **Handles Multiple Links:** Convert multiple conversations into separate PDFs in one command.
- **Preserves Dynamic Content:** Automatically clicks and expands "Thought for..." sections to include them in the output.

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/chatgpt-link-converter.git
    cd chatgpt-link-converter
    ```

2.  **Install dependencies using Poetry:**
    This command will create a virtual environment and install all required libraries.
    ```bash
    poetry install
    ```

3.  **Install browser binaries:**
    The first time you run, `playwright` needs to download the browser engines it uses. This is a one-time setup.
    ```bash
    poetry run playwright install
    ```

## Usage

Run the script from your terminal, providing one or more ChatGPT share links as arguments.

```bash
poetry run python converter.py <url1> <url2> ...
```

### Example

```bash
poetry run python converter.py https://chatgpt.com/share/687c01a3-5108-800b-8e2f-0d660b756012
```

This will create a PDF file named `chatgpt-share-687c01a3-5108-800b-8e2f-0d660b756012.pdf` in the project directory.

## How It Works

This tool uses the `playwright` library to control a headless browser. For each URL provided, it:

1.  Launches a Chromium browser in the background.
2.  Navigates to the ChatGPT share link.
3.  Waits for the page and all its dynamic content to load completely.
4.  Finds and clicks all "Thought for..." dropdowns to expand them.
5.  Extracts the final, rendered HTML of the main conversation thread.
6.  Generates a clean, high-quality PDF from that specific HTML.

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
