import os, json, random, datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- FILE PATHS ----------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

NOTES_FILE = DATA_DIR / "notes.txt"
PROGRESS_FILE = DATA_DIR / "progress.json"
FLASHCARD_FILE = DATA_DIR / "flashcards.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"

RECOMMENDED_TIME = {
    "Python": 120,
    "HTML": 60,
    "CSS": 60,
    "JavaScript": 90,
    "OOP": 60,
    "DSA": 120,
    "Development": 90
}

# ---------------- HELPERS ----------------
def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return default

def write_json(path, data):
    try:
        path.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error writing {path}: {e}")

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

# -------- AI CHAT --------
@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    prompt = request.json.get("prompt", "").lower()
    if not prompt:
        return jsonify({"response": "Please ask something."})

    # Get current time
    now = datetime.datetime.now()
    
    if "time" in prompt:
        return jsonify({"response": f"Current time is {now.strftime('%I:%M %p')}"})

    if "date" in prompt or "today" in prompt:
        return jsonify({"response": f"Today is {now.strftime('%A, %B %d, %Y')}"})
    
    if "schedule" in prompt or "routine" in prompt:
        day = now.strftime("%A")
        schedule = read_json(SCHEDULE_FILE, {})
        if day in schedule:
            return jsonify({"response": f"Let me show you today's schedule!", "action": "show_schedule"})
        return jsonify({"response": "No schedule found for today."})
    
    if "progress" in prompt or "study" in prompt:
        return jsonify({"response": "Here's your study progress!", "action": "show_progress"})
    
    if "flashcard" in prompt or "quiz" in prompt:
        return jsonify({"response": "Let me get a flashcard for you!", "action": "show_flashcard"})
    
    if "note" in prompt:
        return jsonify({"response": "Would you like to see your notes?", "action": "show_notes"})

    # Default response
    responses = [
        "I'm SATHI, your Smart AI Tech Helper! 😊 How can I assist you today?",
        "I'm here to help with your studies! Ask me about your schedule, progress, or notes.",
        "Need help with something? I can show you flashcards, schedules, or track your progress!",
    ]
    return jsonify({"response": random.choice(responses)})

# -------- NOTES --------
@app.route("/notes", methods=["GET"])
def get_notes():
    notes = []
    if NOTES_FILE.exists():
        for i, line in enumerate(NOTES_FILE.read_text().splitlines(), 1):
            if line.strip():  # Skip empty lines
                notes.append({"id": i, "text": line.strip()})
    return jsonify({"notes": notes})

@app.route("/notes", methods=["POST"])
def add_note():
    note = request.json.get("note", "").strip()
    if note:
        with open(NOTES_FILE, "a", encoding='utf-8') as f:
            f.write(note + "\n")
        return jsonify({"message": "Note added successfully!", "success": True})
    return jsonify({"message": "Note cannot be empty", "success": False})

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    if not NOTES_FILE.exists():
        return jsonify({"message": "No notes found", "success": False})
    
    lines = NOTES_FILE.read_text().splitlines()
    if 0 < id <= len(lines):
        lines.pop(id-1)
        NOTES_FILE.write_text("\n".join(lines) + "\n")
        return jsonify({"message": "Note deleted", "success": True})
    return jsonify({"message": "Invalid note ID", "success": False})

# -------- FLASHCARDS --------
@app.route("/flashcard", methods=["GET"])
def get_flashcard():
    cards = read_json(FLASHCARD_FILE, [])
    if not cards:
        return jsonify({"error": "No flashcards available. Add some first!"})
    
    card = random.choice(cards)
    # Handle both old and new format
    if "question" in card:
        return jsonify({
            "front": card["question"],
            "back": card["answer"]
        })
    return jsonify(card)

@app.route("/flashcard", methods=["POST"])
def add_flashcard():
    card = request.json
    front = card.get("front", "").strip()
    back = card.get("back", "").strip()
    
    if not front or not back:
        return jsonify({"message": "Both question and answer required", "success": False})
    
    cards = read_json(FLASHCARD_FILE, [])
    cards.append({"front": front, "back": back})
    write_json(FLASHCARD_FILE, cards)
    return jsonify({"message": "Flashcard added!", "success": True})

@app.route("/flashcards", methods=["GET"])
def get_all_flashcards():
    cards = read_json(FLASHCARD_FILE, [])
    return jsonify({"flashcards": cards})

# -------- PROGRESS --------
@app.route("/progress", methods=["GET"])
def get_progress():
    data = read_json(PROGRESS_FILE, {})
    result = []
    for sub, rec in RECOMMENDED_TIME.items():
        studied = data.get(sub, 0)
        percent = int((studied / rec) * 100) if rec else 0
        result.append({
            "name": sub,
            "studied": studied,
            "recommended": rec,
            "percentage": min(percent, 100)
        })
    return jsonify({"subjects": result})

@app.route("/progress", methods=["POST"])
def add_progress():
    subject = request.json.get("subject")
    minutes = int(request.json.get("minutes", 0))
    
    if not subject or minutes <= 0:
        return jsonify({"message": "Invalid input", "success": False})
    
    data = read_json(PROGRESS_FILE, {})
    data[subject] = data.get(subject, 0) + minutes
    write_json(PROGRESS_FILE, data)
    return jsonify({"message": f"Logged {minutes} minutes for {subject}", "success": True})

# -------- SCHEDULE --------
@app.route("/schedule", methods=["GET"])
def get_schedule():
    schedule = read_json(SCHEDULE_FILE, {})
    now = datetime.datetime.now()
    current_day = now.strftime("%A")
    return jsonify({
        "schedule": schedule,
        "currentDay": current_day
    })

@app.route("/schedule", methods=["POST"])
def save_schedule():
    schedule_data = request.json
    write_json(SCHEDULE_FILE, schedule_data)
    return jsonify({"message": "Schedule saved!", "success": True})

# -------- QUOTE GENERATOR --------
@app.route("/quote", methods=["GET"])
def get_quote():
    quotes = [
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
        {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
        {"text": "Experience is the name everyone gives to their mistakes.", "author": "Oscar Wilde"},
        {"text": "In order to be irreplaceable, one must always be different.", "author": "Coco Chanel"},
        {"text": "The best way to predict the future is to invent it.", "author": "Alan Kay"},
        {"text": "Learning never exhausts the mind.", "author": "Leonardo da Vinci"},
    ]
    return jsonify(random.choice(quotes))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)