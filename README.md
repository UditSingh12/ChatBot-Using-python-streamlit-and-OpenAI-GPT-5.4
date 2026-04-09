# ChatBot-Using-python-streamlit-and-OpenAI-GPT-5.4

🤖 AI Chatbot using Python, Streamlit & OpenAI
📌 Overview

This project is an interactive AI chatbot built using Python and Streamlit, integrated with the OpenAI API to generate intelligent, real-time responses.

The application provides a clean chat interface where users can ask questions and receive responses dynamically, making it suitable for learning, experimentation, and deployment.

🚀 Features
💬 Interactive chat interface using Streamlit
⚡ Real-time response streaming (token-by-token output)
🧠 Context-aware conversation (chat history maintained)
🔐 Secure API key management using .env
🪶 Lightweight and easy to deploy
📦 Clean project structure with best practices
🛠️ Tech Stack
Language: Python
Framework: Streamlit
API: OpenAI API
Environment Management: python-dotenv
📂 Project Structure
├── Chatbot.py        # Main application file
├── requirements.txt # Project dependencies
├── .env             # API key (not pushed to GitHub)
├── .gitignore       # Ignore sensitive and unnecessary files
└── README.md        # Project documentation
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/Uditsingh12/Chatbot-using-python-streamlit-and-OpenAI.git
cd Chatbot-using-python-streamlit-and-OpenAI
2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate   # For Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Set Up Environment Variables

Create a .env file in the root directory and add:

OPENAI_API_KEY=your_api_key_here

⚠️ Important: Never share your API key publicly.

5️⃣ Run the Application
streamlit run Chatbot.py
🧠 How It Works
User enters a query in the chat interface
The query is sent to the OpenAI API
The model processes the input and generates a response
Response is streamed and displayed in real-time
Chat history is stored using Streamlit session state
🔐 Security Best Practices
API key is stored in .env file
.env is ignored using .gitignore
No sensitive data is exposed in the code
📌 Future Improvements
Add chatbot memory (long-term context)
File upload (PDF / CSV chatbot)
Voice input/output
Deployment on cloud (Streamlit Cloud / AWS / Render)
UI enhancements
🧑‍💻 Author

Udit Singh

GitHub: https://github.com/Uditsingh12
📄 License

This project is open-source and available under the MIT License.

⭐ Support

If you like this project:

⭐ Star this repository
🍴 Fork it
🛠️ Contribute
