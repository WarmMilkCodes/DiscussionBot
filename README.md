# AI Discussion Post Generator

This is a simple Python script that uses the OpenAI API to generate discussion posts based on a theme or question.

## Setup

1. **Install dependencies**:

```bash
pip install openai python-dotenv
```

2. **Configuration**:

- Create a `.env` file with your OpenAI API key (reference line 1 of sample_env.txt)
- Modify `config.json` file with the desired settings

## Usage

```bash
python main.py
```

## Configuration Options (config.json)

| Section      | Key          | Description                          |
|--------------|--------------|--------------------------------------|
| ai_settings  | model        | OpenAI model (e.g., gpt-4, gpt-3.5-turbo) |
|              | max_tokens   | Maximum response length (50-4000)    |
|              | temperature  | Creativity level (0.0-2.0)           |
| file_paths   | posts        | Path to discussion posts file        |

## File Structure

- `main.py`: Main script for generating discussion posts
- `config.json`: Configuration file
- `discussion_posts.txt`: File containing discussion posts (input)
- `.env`: Environment file with OpenAI API key

# Requirements

- python-dotenv
- openai>=1.0.0
- streamlit>=1.30.0

# Run with command line

```bash
python main.py
```

# Run with UI

```bash
streamlit run app.py
```

