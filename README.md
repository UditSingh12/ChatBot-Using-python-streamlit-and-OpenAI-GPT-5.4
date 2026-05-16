# IntelliChat

A Streamlit chatbot that talks to OpenRouter through the OpenAI Python SDK.

## Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a local `.env` file. You can copy `.env.example` and replace the key:

```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_MODEL=openrouter/free
```

3. Start the app:

```bash
streamlit run app.py
```

## Deploy On Streamlit Community Cloud

Use `app.py` as the main file.

In your Streamlit app settings, add these secrets:

```toml
OPENROUTER_API_KEY = "your-openrouter-api-key-here"
OPENROUTER_MODEL = "openrouter/free"
OPENROUTER_SITE_NAME = "IntelliChat"
```

Do not upload `.env` or `.streamlit/secrets.toml` to GitHub.

`openrouter/free` automatically routes requests to the free models currently
available on OpenRouter.
