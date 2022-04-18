import pytest
import server

MOCK_COMPETITIONS_PATH = "tests/mock_competitions.json"
MOCK_CLUBS_PATH = "tests/mock_clubs.json"


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    client = server.app.test_client()

    yield client


@pytest.fixture
def mock_data(mocker):
    """
    Monkey patch data
    """
    mock_clubs = open(MOCK_CLUBS_PATH, "w")
    mock_clubs.write(
        """
        {"clubs": [
            {
                "name":"Simply Lift",
                "email":"john@simplylift.co",
                "points":"13"
            },
            {
                "name":"Iron Temple",
                "email": "admin@irontemple.com",
                "points":"4"
            },
            {   "name":"She Lifts",
                "email": "kate@shelifts.co.uk",
                "points":"12"
            },
            {
                "name":"Mock Club",
                "email": "test@test.org",
                "points":"42"
            }
        ]}
        """
    )
    mock_clubs.close()
    mock_competitions = open(MOCK_COMPETITIONS_PATH, "w")
    mock_competitions.write(
        """
        {"competitions": [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic 2022",
                "date": "2022-10-22 13:30:00",
                "numberOfPlaces": "13"
            }
        ]}
        """
    )
    mock_competitions.close()
    mocker.patch.object(server, "CLUBS_DATA", MOCK_CLUBS_PATH)
    mocker.patch.object(server, "COMPETITIONS_DATA", MOCK_COMPETITIONS_PATH)
    competitions = server.loadCompetitions()
    clubs = server.loadClubs()

    comps = mocker.patch.object(server, "competitions", competitions)
    c = mocker.patch.object(server, "clubs", clubs)

    mock_data = {
        "competitions": comps,
        "clubs": c,
    }

    return mock_data
