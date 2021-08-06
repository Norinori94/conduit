from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Felületi elem azonosítása
def wait_for_element(browser, by, element):
    return WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((by, element)))


# Felületi elemek azonosítása
def wait_for_elements(browser, by, elements):
    return WebDriverWait(browser, 10).until(
        EC.visibility_of_any_elements_located((by, elements)))


# Bejelentkezés
def login(browser, email, password):
    navbar_sign_in = wait_for_element(browser, By.XPATH, '//a[@href="#/login"]')
    navbar_sign_in.click()

    input_login_email = wait_for_element(browser, By.XPATH, '//input[@placeholder="Email"]')
    input_login_password = wait_for_element(browser, By.XPATH, '//input[@placeholder="Password"]')
    button_sign_in = wait_for_element(browser, By.XPATH, '//button[contains(text(), "Sign in")]')

    input_login_email.send_keys(email)
    input_login_password.send_keys(password)
    button_sign_in.click()


def navbar_elements(browser):
    return wait_for_elements(browser, By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]/li')


def edit_article(browser, article_title, article_about, article_content):
    wait_for_element(browser, By.XPATH, '//input[@placeholder="Article Title"]').clear()
    input_article_title = wait_for_element(browser, By.XPATH, '//input[@placeholder="Article Title"]')
    input_article_title.send_keys(article_title)

    wait_for_element(browser, By.XPATH, '//input[@placeholder="What\'s this article about?"]').clear()
    input_article_about = wait_for_element(browser, By.XPATH, '//input[@placeholder="What\'s this article about?"]')
    input_article_about.send_keys(article_about)

    wait_for_element(browser, By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]').clear()
    input_article_content = wait_for_element(browser, By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')
    input_article_content.send_keys(article_content)

    button_publish_article = wait_for_element(browser, By.XPATH, '//button[@type="submit"]')
    button_publish_article.click()

# def edit_article(browser, article_title, article_about, article_content):
#     input_article_title = wait_for_element(browser, By.XPATH, '//input[@placeholder="Article Title"]')
#     input_article_title.clear()
#     input_article_title.send_keys(article_title)
#
#     input_article_about = wait_for_element(browser, By.XPATH, '//input[@placeholder="What\'s this article about?"]')
#     article_about.clear()
#     input_article_about.send_keys(article_about)
#
#     input_article_content = wait_for_element(browser, By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')
#     article_content.clear()
#     input_article_content.send_keys(article_content)
#
#     button_publish_article = wait_for_element(browser, By.XPATH, '//button[@type="submit"]')
#     button_publish_article.click()