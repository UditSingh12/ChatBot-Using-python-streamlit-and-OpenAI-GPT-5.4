# GitHub Upload Plan - Secure & Push Project

## Steps:
- [x] Secure API key in Chatbot.py (env var + dotenv + fixed model)
- [x] Create .gitignore (sensitive files ignored)
- [x] Create .env.example and update TODO.md
- [x] Create README.md with project description
- [ ] Get GitHub username and repo name from user
- [ ] git init
- [ ] git add .
- [ ] git commit -m "Initial commit: C++ programs + secure Streamlit chatbot"
- [ ] User creates repo on github.com/new (public/private)
- [ ] git remote add origin https://github.com/[username]/[repo].git
- [ ] git branch -M main
- [ ] git push -u origin main
- [ ] Test: Clone repo, check no API key (grep -r sk-proj), run chatbot with own key
