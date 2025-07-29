from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from scorer import score_candidates

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)
CORS(app)

@app.route("/detect-owner", methods=["POST"])
def detect_owner():
    data = request.get_json()
    reviews = data.get("reviews", [])
    business_name = data.get("business_name", "")

    person_contexts = {}
    for r in reviews:
        txt = r.get("text", "")
        resp = r.get("owner_response", "")
        for segment in [txt, resp]:
            if not segment:
                continue
            doc = nlp(segment)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    name = ent.text.strip()
                    person_contexts.setdefault(name, []).append(segment)

    ranked = score_candidates(person_contexts, reviews, business_name)

    return jsonify({
        "candidates": ranked,
        "best_guess": ranked[0]["name"] if ranked else None
    })