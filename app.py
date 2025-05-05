from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.workouts = []

    def add_workout(self, workout_type, duration):
        self.workouts.append({
            "type": workout_type,
            "duration": duration,
            "date": datetime.now().date()
        })

    def get_advice(self):
        return ""

class BeginnerUser(User):
    def get_advice(self):
        return "Focus on consistency and basic exercises."

class IntermediateUser(User):
    def get_advice(self):
        return "Start including strength training and longer cardio sessions."

class AdvancedUser(User):
    def get_advice(self):
        return "Incorporate HIIT and track macros for better results."

user = None  # Global user object

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global user
        name = request.form["name"]
        age = int(request.form["age"])
        level = request.form["level"].lower()

        if level == "beginner":
            user = BeginnerUser(name, age)
        elif level == "intermediate":
            user = IntermediateUser(name, age)
        elif level == "advanced":
            user = AdvancedUser(name, age)
        else:
            user = BeginnerUser(name, age)

        return redirect(url_for("workout"))

    return render_template("index.html")

@app.route("/workout", methods=["GET", "POST"])
def workout():
    if request.method == "POST":
        workout_type = request.form["type"]
        duration = int(request.form["duration"])
        user.add_workout(workout_type, duration)

        if "finish" in request.form:
            return redirect(url_for("report"))

    return render_template("workout.html", name=user.name)

@app.route("/report")
def report():
    return render_template("report.html", user=user)

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
#http://127.0.0.1:5000/