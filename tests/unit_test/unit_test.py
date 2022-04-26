from server import POINTS_PER_PLACE, loadClubs, loadCompetitions

CLUBS_NB = 3
COMPETITIONS_NB = 2
UNKNOWN_EMAIL = "unknown@unknown.org"
EMPTY_EMAIL = ""
UNKNOWN_COMPETITION = "unknown"
UNKNOWN_CLUB = "unknown"


class TestDatabase:
    def test_loadClubs(self):
        """
        Test that clubs data are loaded correctly
        """
        clubs_list = loadClubs()
        assert len(clubs_list) == CLUBS_NB

    def test_loadCompetitions(self):
        """
        Test that competitions data are loaded correctly
        """
        competitions_list = loadCompetitions()
        assert len(competitions_list) == COMPETITIONS_NB


class TestIndex:
    def test_should_return_status_code_200(self, client):
        """
        Case: happy path
            Test that index page is loaded correctly
        """
        response = client.get("/")
        assert response.status_code == 200

    def test_should_return_expected_content(self, client):
        """
        Case: happy path
            Test that index page is loaded correctly
        """
        response = client.get("/")
        data = response.data.decode()
        assert ("GUDLFT Registration") in data
        assert ("Please enter your secretary email to continue:") in data


class TestShowSummary:
    def test_login_with_known_email(self, client, mock_data):
        """
        Case: happy path
            Test log in with a known email returns status code 200 and
        expected content
        """
        email = mock_data["clubs"][0]["email"]
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 200
        assert ("GUDLFT Registration") in response.data.decode()
        assert ("Welcome, " + email) in response.data.decode()

    def test_login_with_unknown_email(self, client):
        """
        Case: sad path
            Test log in with an unknown email returns status code 400 and
        expected content
        """
        email = UNKNOWN_EMAIL
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 400
        assert ("Error: unknown email") in response.data.decode()

    def test_login_with_empty_email(self, client):
        """
        Case: sad path
            Test log in with an empty email returns status code 400 and
        expected content
        """
        email = EMPTY_EMAIL
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 400
        assert ("Error: empty email field") in response.data.decode()


class TestBook:
    def test_book_past_competitions(self, client, mock_data):
        """
        Case: happy path
            Test should not be able to book for past competitions
        """
        competition_name = mock_data["competitions"][0]["name"]
        club_name = mock_data["clubs"][3]["name"]
        response = client.get("/book/" + competition_name + "/" + club_name)
        data = response.data.decode()
        assert response.status_code == 200
        assert ("Error: can not purchase a place for past competitions") in data
        assert ("Great-booking complete!") not in data

    def test_should_return_status_code_200_expected_content(self, client, mock_data):
        """
        Case: happy path
            Test that the page is loaded correctly
        """
        competition_name = mock_data["competitions"][1]["name"]
        club_name = mock_data["clubs"][0]["name"]
        response = client.get("/book/" + competition_name + "/" + club_name)
        data = response.data.decode()
        assert response.status_code == 200
        assert ("Booking for " + competition_name) in data
        assert ("Fall Classic") in data
        assert ("Places available: 13") in data
        assert ("How many places") in data

    def test_book_from_unknown_club(self, client, mock_data):
        """
        Case: sad path
        """
        competition_name = mock_data["competitions"][1]["name"]
        club_name = UNKNOWN_CLUB
        response = client.get("/book/" + competition_name + "/" + club_name)
        data = response.data.decode()
        assert response.status_code == 400
        assert ("Something went wrong-please try again") in data

    def test_book_unknown_competition(self, client, mock_data):
        """
        Case: sad path
        """
        competition_name = UNKNOWN_COMPETITION
        club_name = mock_data["clubs"][0]["name"]
        response = client.get("/book/" + competition_name + "/" + club_name)
        data = response.data.decode()
        assert response.status_code == 400
        assert ("Something went wrong-please try again") in data


class TestPurchasePlaces:
    def test_should_not_purchase_more_than_12_places(self, client, mock_data):
        """
        Case: sad path
        """
        competition_name = mock_data["competitions"][1]["name"]
        club_name = mock_data["clubs"][3]["name"]

        response = client.post(
            "/purchasePlaces",
            data={"places": "13", "competition": competition_name, "club": club_name},
        )
        assert response.status_code == 200
        assert ("Error: can not purchase more than 12 places") in response.data.decode()

    def test_purchase_no_places_available(self, client, mock_data):
        """
        Case: sad path
        """
        competition_name = mock_data["competitions"][1]["name"]
        club_name = mock_data["clubs"][0]["name"]
        club_name2 = mock_data["clubs"][3]["name"]
        client.post(
            "/purchasePlaces",
            data={"places": "2", "competition": competition_name, "club": club_name},
        )
        response = client.post(
            "/purchasePlaces",
            data={"places": "12", "competition": competition_name, "club": club_name2},
        )
        assert response.status_code == 200
        assert ("Error: no places available") in response.data.decode()

    def test_purchase_negative_number_of_places(self, client, mock_data):
        """
        Case: sad path
        """
        competition_name = mock_data["competitions"][1]["name"]
        club_name = mock_data["clubs"][3]["name"]

        response = client.post(
            "/purchasePlaces",
            data={
                "places": -1,
                "competition": competition_name,
                "club": club_name,
            },
        )
        assert response.status_code == 400
        assert ("Error: places value can not be negative") in response.data.decode()

    def test_purchase_no_enough_points(self, client, mock_data):
        """
        Case: sad path
        """
        competition_name = mock_data["competitions"][1]["name"]
        club_name = mock_data["clubs"][1]["name"]
        club_points = int(mock_data["clubs"][1]["points"])

        response = client.post(
            "/purchasePlaces",
            data={
                "places": club_points + 1,
                "competition": competition_name,
                "club": club_name,
            },
        )
        assert response.status_code == 200
        assert ("Error: no enough points") in response.data.decode()

    def test_purchase_places_points_are_deducted(self, client, mock_data):
        """
        Case: happy path
        """
        competition_name = mock_data["competitions"][1]["name"]
        club_name = mock_data["clubs"][1]["name"]
        club_points = int(mock_data["clubs"][1]["points"])
        response = client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "competition": competition_name,
                "club": club_name,
            },
        )
        points_remaining = club_points - 1 * POINTS_PER_PLACE
        assert response.status_code == 200
        assert ("Great-booking complete!") in response.data.decode()
        assert (f"Points available: {points_remaining}") in response.data.decode()


class TestLogout:
    def test_logout(self, client):
        """
        Case: happy path
            Test that the user is correctly logged out.
        """
        response = client.get("/logout")
        assert response.status_code == 302
