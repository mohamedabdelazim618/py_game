import os
import secrets
from collections import Counter

from flask import Flask, render_template, request, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-before-deploying")

# ---- Scoring rules -----------------------------------------------------
BULL_POINTS = 10     # a digit that's in the exact right position
COW_POINTS = 3        # a digit that's in the code, just the wrong position
JACKPOT_TOTAL = 1000   # flat award for cracking the code completely


def generate_pin():
    """
    A 4-digit code drawn with a cryptographically secure generator.
    secrets.randbelow(10000) is uniform over 0..9999, and formatting it
    with leading zeros is a 1-to-1 mapping onto 4 independent, equally
    likely digits (0-9) per slot — so no digit or position is ever
    more likely than any other, and the draw can't be predicted or
    seeded from the outside.
    """
    return f"{secrets.randbelow(10000):04d}"


def score_guess(guess, code):
    """
    Mastermind-style, duplicate-digit-safe scoring.
    Returns (bulls, cows, points).
    """
    bulls = sum(g == c for g, c in zip(guess, code))

    guess_counts = Counter(guess)
    code_counts = Counter(code)
    total_digit_matches = sum(min(guess_counts[d], code_counts[d]) for d in guess_counts)
    cows = total_digit_matches - bulls

    points = JACKPOT_TOTAL if bulls == 4 else bulls * BULL_POINTS + cows * COW_POINTS
    return bulls, cows, points


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    user_pin = None
    generated_pin = None
    result = None
    bulls = cows = points = None

    session.setdefault("total_score", 0)
    session.setdefault("attempts", 0)
    session.setdefault("wins", 0)

    if request.method == "POST":
        if request.form.get("reset") == "1":
            session["total_score"] = 0
            session["attempts"] = 0
            session["wins"] = 0
        else:
            user_input = request.form.get("pin", "")

            if not user_input.isdigit() or len(user_input) != 4:
                error = "Enter exactly 4 digits (0-9)."
            else:
                user_pin = user_input
                generated_pin = generate_pin()
                bulls, cows, points = score_guess(user_pin, generated_pin)
                result = bulls == 4

                session["attempts"] += 1
                session["total_score"] += points
                if result:
                    session["wins"] += 1
                session.modified = True

    return render_template(
        "index.html",
        error=error,
        user_pin=user_pin,
        generated_pin=generated_pin,
        result=result,
        bulls=bulls,
        cows=cows,
        points=points,
        total_score=session.get("total_score", 0),
        attempts=session.get("attempts", 0),
        wins=session.get("wins", 0),
        bull_points=BULL_POINTS,
        cow_points=COW_POINTS,
        jackpot_total=JACKPOT_TOTAL,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
