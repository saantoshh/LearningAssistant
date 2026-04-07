📚 SATHI – Smart AI Tech Helper

A smart AI-powered learning assistant built with Flask (Python) that helps students manage their study routine, track progress, take notes, and revise using flashcards.

🚀 Features

✨ AI Chat Assistant

Ask about time, date, schedule, progress, notes, and more
Smart keyword-based responses

📝 Notes Management

Add, view, and delete notes
Stored locally in a text file

🧠 Flashcards System

Create and review flashcards
Randomized quiz-style learning

📊 Study Progress Tracker

Track study time per subject
Get percentage-based progress insights

📅 Schedule Manager

Save and view daily study routines
Automatically detects current day

💬 Motivational Quotes

Random inspirational quotes to stay motivated
🛠️ Tech Stack
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript
Storage: JSON & Text Files
Other Tools: Flask-CORS, python-dotenv


Learning-assistant/
│
├── app.py
├── .env
├── data/
│   ├── notes.txt
│   ├── progress.json
│   ├── flashcards.json
│   └── schedule.json
│
|
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    └── js/


    
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/sathi-learning-assistant.git
cd sathi-learning-assistant

2️⃣ Create Virtual Environment
python -m venv venv

▶️ Activate Environment
Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate

3️⃣ Install Dependencies
pip install flask flask-cors python-dotenv

4️⃣ Run the Application
python app.py

5️⃣ Open in Browser
http://localhost:5000

📡 API Endpoints
🤖 AI Assistant


POST /ask_ai
📝 Notes
GET /notes → Get all notes

POST /notes → Add a note

DELETE /notes/<id> → Delete a note

🧠 Flashcards
GET /flashcard → Get random flashcard

POST /flashcard → Add flashcard

GET /flashcards → Get all flashcards


📊 Progress
GET /progress → Get study progress

POST /progress → Add study time


📅 Schedule
GET /schedule → Get schedule

POST /schedule → Save schedule


💬 Quotes

GET /quote → Get random motivational quote


🎯 Use Cases

📚 Students managing daily study routines

🧠 Revision using flashcards

📊 Tracking productivity

💻 Simple offline learning assistant


🔮 Future Improvements

🔐 User authentication (Login/Register)

☁️ Database integration (MySQL / MongoDB)

🤖 Real AI integration (OpenAI API)

📱 Mobile responsive UI

📊 Graph-based analytics dashboard

