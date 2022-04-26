import json
from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request, url_for

CLUBS_DATA = "clubs.json"
COMPETITIONS_DATA = "competitions.json"
POINTS_PER_PLACE = 3

# CLUBS_DATA = "tests/mock_clubs.json"
# COMPETITIONS_DATA = "tests/mock_competitions.json"


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
    return render_template("index.html", clubs=clubs)


@app.route("/showSummary", methods=["POST"])
def showSummary():
    if request.form["email"] == "":
        flash("Error: empty email field")
        return (
            render_template("index.html", clubs=clubs),
            400,
        )
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Error: unknown email")
        return render_template("index.html", clubs=clubs), 400
    return render_template("welcome.html", club=club, competitions=competitions, clubs=clubs)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return (
            render_template("welcome.html", club=club, competitions=competitions, clubs=clubs),
            400,
        )

    if foundClub and foundCompetition:
        competition_date = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
        if competition_date < datetime.now():
            flash("Error: can not purchase a place for past competitions")
            return (
                render_template(
                    "welcome.html",
                    club=foundClub,
                    competitions=competitions,
                    clubs=clubs,
                ),
                200,
            )

        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return (
            render_template("welcome.html", club=foundClub, competitions=competitions, clubs=clubs),
            400,
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        placesRequired = int(request.form["places"])
        if placesRequired > 12:
            flash("Error: can not purchase more than 12 places")
            return (
                render_template("welcome.html", club=club, competitions=competitions, clubs=clubs),
                200,
            )
        competition_places = int(competition["numberOfPlaces"])
        if placesRequired > competition_places:
            flash("Error: no places available")
            return (
                render_template("welcome.html", club=club, competitions=competitions, clubs=clubs),
                200,
            )

        club_points = int(club["points"])
        if placesRequired <= 0:
            flash("Error: places value can not be negative")
            return (
                render_template("welcome.html", club=club, competitions=competitions, clubs=clubs),
                400,
            )

        elif club_points >= placesRequired * POINTS_PER_PLACE:
            if competition["name"] in club and (club[competition["name"]] + placesRequired) > 12:
                flash("Error: can not purchase more than 12 places")
                return (
                    render_template(
                        "welcome.html",
                        club=club,
                        competitions=competitions,
                        clubs=clubs,
                    ),
                    400,
                )
            competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
            club["points"] = club_points - placesRequired * POINTS_PER_PLACE
            if competition["name"] in club:
                club[competition["name"]] += placesRequired
            else:
                club[competition["name"]] = placesRequired
        else:
            flash("Error: no enough points")
            return (
                render_template("welcome.html", club=club, competitions=competitions, clubs=clubs),
                200,
            )
        flash("Great-booking complete!")
    except ValueError:
        flash("Error: Value error")
    return render_template("welcome.html", club=club, competitions=competitions, clubs=clubs)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
