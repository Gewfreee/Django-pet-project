from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='class')
def browser():
    print("\n starting browser")
    browser = webdriver.Chrome()
    yield browser
    print("\n closing browser")
    browser.quit()


class TestAuthentication():
    def test_signup(self, browser):
        browser.get("http://localhost:8000/")
        browser.find_element(By.XPATH, "//a[text() = 'Sign up']").click()

        browser.find_element(By.ID, "id_username").send_keys('test_username')
        browser.find_element(By.ID, "id_email").send_keys('test_user@gmail.com')
        browser.find_element(By.ID, "id_password1").send_keys('qwefsdf3243243')
        browser.find_element(By.ID, "id_password2").send_keys('qwefsdf3243243')
        browser.find_element(By.CLASS_NAME, "submit").click()

        assert WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".avatar-container")))

    def test_logout(self, browser):
        browser.get("http://localhost:8000/")

        browser.find_element(By.CSS_SELECTOR, ".avatar-circle").click()
        browser.find_element(By.XPATH, "//a[text() = 'Log out']").click()

        assert  browser.find_element(By.XPATH, "//a[text() = 'Log in']")


    def test_login(self, browser):
        browser.get("http://localhost:8000/")
        browser.find_element(By.XPATH, "//a[text() = 'Log in']").click()

        browser.find_element(By.ID, "id_username").send_keys('test_username')
        browser.find_element(By.ID, "id_password").send_keys('qwefsdf3243243')
        browser.find_element(By.CLASS_NAME, "submit").click()

        assert WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".avatar-container")))

    def test_add_review(self, browser):
        browser.get("http://localhost:8000/")

        browser.find_element(By.ID, "search_query").send_keys("a")
        browser.find_element(By.ID, "search-button").click()
        browser.find_element(By.CSS_SELECTOR, ".card-header a").click()

        browser.find_element(By.CLASS_NAME, "review-textarea").send_keys("Test review")
        browser.find_element(By.CLASS_NAME, "review-add-button").click()

        assert browser.find_element(
            By.XPATH, "//div[@class='review']/p[@class='review-text'][contains(text(), 'Test review')]")
