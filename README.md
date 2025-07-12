
## Requirements
1. Make sure Python is installed in your machine

2. If you see a venv folder DELETE IT and then go into venv again from your terminal with the following commands:
   "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy z"

3. Start Venv Folder at the same terminal
   "python -m venv venv"

4. Now run this command:
   ".\venv\Scripts\Activate.ps1"

5. Make sure you have all libs and dependecies installed inside the venv run this command:
   'pip install -r requirements.txt'

6. After that you have to install some dependicies manually with the following command:
   "pip install python-dotenv langchain langchain-together PyPDF2"

7. Then again you have to download some libs (especially torch, transformers, etc.), also run:
   "pip install django"
   "pip install python-dotenv langchain langchain_together PyPDF2"
   "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
   "pip install transformers"

## INSTALL ALL OF THIS INSIDE THE VENV 

---

## How to Run

1. After venv is running in that same powershell/terminal run the app
"python manage.py runserver"

2. After Django is up and running simply go to your browser and go at 

3. Ctrl + C on the terminal to stop Django if needed

4. To test the Agents use the files and images inside the medical-agent folder each photo or file will be named according to the agent 
