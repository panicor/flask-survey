from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def show_start():
    """Displays start screen for survey"""
    return render_template("start.html", survey=survey)

@app.route("/start", methods=["POST"])
def start():
    """Starts survey"""
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_q():
    """Handles survey questions"""

    choice = request.form['answer']
    responses = session['responses']
    responses.append(choice)
    session["responses"] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/done")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:q_id>")
def show_q(q_id):
    """Shows current question"""

    responses = session.get("responses")

    if (responses is None):
        return redirect("/")
    elif (len(responses) != q_id):
        flash(f"{q_id} is an invalid question number.")
        return redirect(f"/questions/{len(responses)}")

    q = survey.questions[q_id]
    return render_template("questions.html", id=q_id, question=q, responses=responses)

@app.route("/done")
def done():
    """Shows thank you page"""
    return render_template("done.html")