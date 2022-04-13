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
        Test that index page is loaded correctly
        """
        response = client.get("/")
        assert response.status_code == 200

    def test_should_return_expected_content(self, client):
        """
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
