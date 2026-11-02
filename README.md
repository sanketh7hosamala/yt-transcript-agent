# yt-mcp-agent
A YouTube video agent built using a custom MCP server and OpenAI's Agent's SDK. It can extract video transcripts given link fetch specialized instructions for things like: writing blog posts, video chapters, and social posts.

Resources:
- [Talk recording](https://youtu.be/w-Ml3NivoFo)
- [Slides](https://drive.google.com/file/d/1id7V9nrNetW72k6vERS6oTy0bW0wEloo/view?usp=sharing)

>This example is a prelude to [Cohort 7](https://github.com/ShawhinT/AI-Builders-Bootcamp-7/tree/main) of the [AI Builders Bootcamp](https://maven.com/shaw-talebi/ai-builders-bootcamp).

## Requirements

- Python 3.13+
- OpenAI API key
- `uv` package manager (recommended)

## How to run this example

### uv (recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd yt-mcp-agent
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Set up your OpenAI API key**
   
   Create a `.env` file in the root directory:
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the agent**
   ```bash
   uv run main.py
   ```

5. **Interact with agent**
   
   Once running, you can ask the agent to analyze YouTube videos. Try prompts like:
   - "Summarize this: https://youtu.be/N3vHJcHBS-w?si=aw8PV0acYHJGPy7R"
   - "Generate chapter timestamps with links"
   - "Write me a LinkedIn post about the video"

### Base Python/pip

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd yt-mcp-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Set up your OpenAI API key**
   
   Create a `.env` file in the root directory:
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

5. **Run the agent**
   ```bash
   python main.py
   ```

6. **Interact with agent**
