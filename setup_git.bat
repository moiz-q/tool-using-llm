@echo off
echo Initializing Git repository...
git init

echo Adding files...
git add .

echo Creating initial commit...
git commit -m "Initial commit: Tool-Using LLM - Controlled tool calling with JSON schema enforcement, max iterations, and error handling"

echo Creating GitHub repository...
gh repo create tool-using-llm --public --source=. --description="Teach LLMs to use tools reliably without hallucinating outputs - Calculator, document search, web fetch with JSON schema enforcement and error handling"

echo Pushing to GitHub...
git push -u origin main

echo Done! Repository created and pushed to GitHub.
pause
