from server import loadClubs, loadCompetitions, POINTS_PER_PLACE


class TestIntegration:
    def test_integration(self, client):
        """
        Integration test
        """
        # index
        response = client.get("/")
        assert response.status_code == 200

        # loadClubs
        club = loadClubs()[0]

        # loadCompetitions
        competition = loadCompetitions()[1]

        # showSummary
        email = club["email"]
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 200
        assert ("GUDLFT Registration") in response.data.decode()
        assert ("Welcome, " + email) in response.data.decode()

        # book
        competition_name = competition["name"]
        club_name = club["name"]
        response = client.get("/book/" + competition_name + "/" + club_name)
        data = response.data.decode()
        assert response.status_code == 200
        assert ("Booking for " + competition_name) in data
        assert ("Fall Classic") in data
        assert ("Places available: 13") in data
        assert ("How many places") in data

        # purchasePlaces
        club_points = int(club["points"])
        response = client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "competition": competition_name,
                "club": club_name,
            },
        )
        places_remaining = club_points - 1 * POINTS_PER_PLACE
        assert response.status_code == 200
        assert ("Great-booking complete!") in response.data.decode()
        assert (f"Points available: {places_remaining}") in response.data.decode()

        # logout
        response = client.get("/logout")
        assert response.status_code == 302
