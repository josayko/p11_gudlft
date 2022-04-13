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
        data = response.data
        expected_data = b'<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>GUDLFT Registration</title>\n</head>\n<body>\n    <h1>Welcome to the GUDLFT Registration Portal!</h1>\n    Please enter your secretary email to continue:\n    <form action="showSummary" method="post">\n        <label for="email">Email:</label>\n        <input type="email" name="email" id=""/>\n        <button type="submit">Enter</button>\n    </form>\n</body>\n</html>'
        assert data == expected_data
