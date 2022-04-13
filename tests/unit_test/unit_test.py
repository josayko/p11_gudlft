import server

CLUBS_NB = 3
COMPETITIONS_NB = 2
UNKNOWN_EMAIL = "test@test.org"
EMPTY_EMAIL = ""
UNKNOWN_COMPETITION = "test"
UNKNOWN_CLUB = "test"

class TestDatabase():
    def test_loadClubs(self):
        """
        Verify that clubs data are loaded correctly
        """
        clubs_list = server.loadClubs()
        assert len(clubs_list) == CLUBS_NB
    
    def test_loadCompetitions(self):
        """
        Verify that competitions data are loaded correctly
        """
        competitions_list = server.loadCompetitions()
        assert len(competitions_list) == COMPETITIONS_NB