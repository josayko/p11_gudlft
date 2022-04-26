# third party imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# local application imports
import server

# other imports

# constants

SERVICE = Service(ChromeDriverManager().install(), log_path="tests/functional_test/chromedriver.log")  # noqa


def test_happy_path():

    driver = webdriver.Chrome(service=SERVICE)

    driver.get("http://127.0.0.1:5000/")
    driver.implicitly_wait(2)

    # Login
    email = server.loadClubs()[0]["email"]
    login = driver.find_element(By.NAME, "email")
    login.send_keys(email)
    login.submit()
    driver.implicitly_wait(2)

    # Verify if the user is logged in
    assert ("Welcome, " + email) in driver.find_element(By.TAG_NAME, "h2").text

    # Select a competition
    select_comp = driver.find_element(by=By.XPATH, value="/html/body/ul/li[2]/a")
    select_comp.click()
    driver.implicitly_wait(2)

    # verify if the user is in the book place page
    assert ("Fall Classic") in driver.find_element(By.TAG_NAME, "h2").text

    # book a place
    book = driver.find_element(By.NAME, "places")
    book.send_keys("2")
    book.submit()
    driver.implicitly_wait(2)

    # Logout
    logout = driver.find_element(By.LINK_TEXT, "Logout")
    logout.click()
    driver.implicitly_wait(2)

    # Verify if the user is logged out
    assert "GUDLFT Registration" in driver.title

    # Close the browser
    driver.quit()


def test_wrong_email():
    """
    Test a path where the user try to login with a wrong email.
    """

    # configs
    driver = webdriver.Chrome(service=SERVICE)

    # Get index page
    driver.get("http://127.0.0.1:5000/")
    driver.implicitly_wait(2)

    # Login with a user
    email = "wrong@email.com"
    login = driver.find_element(By.NAME, "email")
    login.send_keys(email)
    login.submit()
    driver.implicitly_wait(2)

    # Verify if the user is logged in
    assert "GUDLFT Registration" in driver.title

    driver.quit()
