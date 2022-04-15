import server

CLUBS_NB = 3
COMPETITIONS_NB = 2
UNKNOWN_EMAIL = "test@test.org"
EMPTY_EMAIL = ""
UNKNOWN_COMPETITION = "test"
UNKNOWN_CLUB = "test"


class TestDatabase:
    def test_loadClubs(self):
        """
        Test that clubs data are loaded correctly
        """
        clubs_list = server.loadClubs()
        assert len(clubs_list) == CLUBS_NB

    def test_loadCompetitions(self):
        """
        Test that competitions data are loaded correctly
        """
        competitions_list = server.loadCompetitions()
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
    def test_login_with_known_email(self, client):
        """
        Case: happy path
            Test log in with a known email returns status code 200 and
        expected content
        """
        email = server.loadClubs()[0]["email"]
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
        assert ("<strong>Error</strong>: unknown email") in response.data.decode()

    def test_login_with_empty_email(self, client):
        """
        Case: sad path
            Test log in with an empty email returns status code 400 and
        expected content
        """
        email = EMPTY_EMAIL
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 400
        assert ("<strong>Error</strong>: empty email field") in response.data.decode()


class TestBook:
    def test_should_return_status_code_200_expected_content(self, client):
        """
        Case: happy path
            Test that the page is loaded correctly
        """
        competition_name = server.loadCompetitions()[0]["name"]
        club_name = server.loadClubs()[0]["name"]
        response = client.get("/book/" + competition_name + "/" + club_name)
        data = response.data.decode()
        assert response.status_code == 200
        assert ("Booking for " + competition_name) in data
        assert ("Spring Festival") in data
        assert ("Places available: 25") in data
        assert ("How many places") in data

    def test_book_from_unknown_club():
        """
        Case: sad path
        """
        pass

    def test_book_unknown_competition():
        """
        Case: sad path
        """
        pass


class TestPurchasePlaces:
    def test_should_not_book_more_than_12_places():
        """
        Case: sad path
        """
        pass

    def test_book_no_places_available():
        """
        Case: sad path
        """
        pass

    def test_book_negative_number_of_places():
        """
        Case: sad path
        """
        pass

    def test_book_no_enough_points():
        """
        Case: sad path
        """
        pass

    def test_book_places_points_are_deducted():
        """
        Case: happy path
        """
        pass


class TestLogout:
    def test_logout(self, client):
        """
        Case: happy path
            Test that the user is correctly logged out.
        """
        response = client.get("/logout")
        assert response.status_code == 302
