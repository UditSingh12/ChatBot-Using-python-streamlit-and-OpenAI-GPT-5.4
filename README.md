# IntelliChat

IntelliChat is an AI chatbot built with Python and Streamlit. It uses the
OpenAI Python SDK with OpenRouter as the API provider, so the app can run with
OpenRouter's free model router.

The project gives users a clean chat interface, keeps the conversation history
inside the Streamlit session, and streams AI responses as they are generated.

## Features

- Interactive chatbot UI built with Streamlit
- OpenRouter API support through the OpenAI SDK
- Free-model-first setup using `openrouter/free`
- Streaming AI responses
- Chat history during the current browser session
- Sidebar model selector for free OpenRouter models
- Clear chat button
- Premium dark UI design
- Local `.env` support for private API keys

## Tech Stack

- Python
- Streamlit
- OpenAI Python SDK
- OpenRouter
- python-dotenv

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
|-- .env.example
|-- .gitignore
`-- .streamlit/
    `-- secrets.toml.example
```

## How It Works

The app loads an OpenRouter API key from environment variables, creates an
OpenAI-compatible client, and sends chat messages to OpenRouter using the
selected free model.

By default, the app uses:

```text
openrouter/free
```

This model route is designed to use free models currently available on
OpenRouter.

## Local Setup

Clone the repository:

```bash
git clone https://github.com/UditSingh12/ChatBot-Using-python-streamlit-and-OpenAI.git
cd ChatBot-Using-python-streamlit-and-OpenAI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_MODEL=openrouter/free
OPENROUTER_SITE_NAME=IntelliChat
```

Run the app:

```bash
streamlit run app.py
```

If `streamlit` is not recognized, use:

```bash
python -m streamlit run app.py
```

## OpenRouter API Key

Create an API key from:

```text
https://openrouter.ai/keys
```

Paste the key into your local `.env` file:

```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

Do not commit your real API key to GitHub.

## Security Notes

- Keep `.env` private.
- Do not share your OpenRouter API key.
- Use `.env.example` only as a template.
- The real `.env` file is ignored by Git through `.gitignore`.

## Author

Built by Udit Singh.
