import json
from flask import Flask, render_template, request, redirect, flash, url_for

CLUBS_DATA = "clubs.json"
COMPETITIONS_DATA = "competitions.json"


def loadClubs():
    with open(CLUBS_DATA) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open(COMPETITIONS_DATA) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    club_points = int(club["points"])
    if placesRequired <= 0:
        flash("Error: places value can not be negative")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            400,
        )

    elif club_points >= placesRequired:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        club["points"] = club_points - placesRequired
    else:
        flash("Error: no enough points")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            400,
        )
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
