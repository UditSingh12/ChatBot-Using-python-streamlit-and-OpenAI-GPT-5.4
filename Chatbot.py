"""Compatibility entry point for Streamlit Cloud.

The existing deployed app may still point to Chatbot.py. Keep the main
application code in app.py and import it here so both entry points work.
"""

from app import *  # noqa: F401,F403
