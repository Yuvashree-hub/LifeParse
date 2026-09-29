from flask import Flask, render_template, request, jsonify
import spacy
import re

app = Flask(__name__)

# Load spaCy English model (en_core_web_sm)
# If not present, download via: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def extract_info(text):
    """
    Main NLP function using spaCy Named Entity Recognition (NER)
    and rule-based pattern matching.
    """
    doc = nlp(text)

    tasks = []
    events = []
    dates_times = []
    people = []
    locations = []
    categories = set()

    # Keywords for category determination
    academic_keywords = ["exam", "test", "quiz", "assignment", "homework", "lecture", "study", "revise", "nlp", "university", "class", "subject", "chapter", "professor"]
    career_keywords = ["internship", "job", "resume", "cv", "interview", "office", "meeting", "project", "work", "client", "boss", "application", "deadline", "salary"]
    personal_keywords = ["doctor", "gym", "workout", "buy", "grocery", "party", "dinner", "lunch", "family", "friend", "movie", "shopping", "flight", "trip"]

    # 1. Category Classification based on keyword matching
    text_lower = text.lower()
    for kw in academic_keywords:
        if kw in text_lower:
            categories.add("Academic")
    for kw in career_keywords:
        if kw in text_lower:
            categories.add("Career")
    for kw in personal_keywords:
        if kw in text_lower:
            categories.add("Personal")

    if not categories:
        categories.add("General")

    # 2. Extract Named Entities using spaCy NER
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            if ent.text.strip() not in dates_times:
                dates_times.append(ent.text.strip())
        elif ent.label_ == "PERSON":
            if ent.text.strip() not in people:
                people.append(ent.text.strip())
        elif ent.label_ in ["GPE", "LOC", "FAC"]:  # Geopolitical Entity / Location / Facility
            if ent.text.strip() not in locations:
                locations.append(ent.text.strip())
        elif ent.label_ in ["EVENT", "WORK_OF_ART"]:
            if ent.text.strip() not in events:
                events.append(ent.text.strip())

    # 3. Rule-Based Task Extraction using Dependency Parsing & POS Tagging
    # Look for Action Verbs (need to revise, submit, buy, call, complete, etc.)
    task_trigger_verbs = ["need", "have", "must", "should", "want", "plan", "submit", "revise", "complete", "finish", "buy", "call", "send", "prepare", "organize"]
    
    # Process sentences individually
    for sent in doc.sents:
        sent_text = sent.text.strip()
        
        # Verb-based task identification
        for token in sent:
            if token.pos_ == "VERB" and token.lemma_.lower() in ["submit", "revise", "complete", "finish", "buy", "call", "send", "prepare", "write", "clean"]:
                # Construct task phrase from the verb to the end of the clause/phrase
                phrase_tokens = [t.text for t in token.subtree if t.pos_ not in ["PUNCT"]]
                task_phrase = " ".join(phrase_tokens).strip()
                # Clean up if phrase is too long or contains temporal modifiers handled elsewhere
                if task_phrase and len(task_phrase.split()) <= 8 and task_phrase not in tasks:
                    tasks.append(task_phrase.capitalize())

            # Identify modal verbs or intent phrases like "need to <verb>", "have to <verb>"
            if token.lemma_.lower() in ["need", "have", "want", "plan"] and any(child.lemma_ == "to" for child in token.children):
                for child in token.children:
                    if child.dep_ == "xcomp": # Open clausal complement (e.g., "to revise")
                        task_phrase = " ".join([t.text for t in child.subtree if t.pos_ not in ["PUNCT"]])
                        if task_phrase and task_phrase not in tasks:
                            tasks.append(task_phrase.capitalize())

        # Keyword-based Event detection backup (e.g., "NLP exam", "Team meeting")
        event_keywords = ["exam", "test", "interview", "meeting", "conference", "party", "match", "appointment", "webinar"]
        for kw in event_keywords:
            if kw in sent_text.lower():
                # Extract the noun phrase containing the event keyword
                for chunk in sent.noun_chunks:
                    if kw in chunk.text.lower() and chunk.text.strip().capitalize() not in events:
                        events.append(chunk.text.strip().capitalize())

    # Fallback cleanups
    tasks = list(dict.fromkeys(tasks))  # Remove duplicates preserving order
    events = list(dict.fromkeys(events))

    return {
        "tasks": tasks,
        "events": events,
        "dates_times": dates_times,
        "people": people,
        "locations": locations,
        "categories": list(categories)
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "text" not in data or not data["text"].strip():
        return jsonify({"error": "Please enter some text to organize."}), 400

    user_text = data["text"]
    result = extract_info(user_text)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)