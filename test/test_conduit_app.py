import time

from selenium import webdriver
from conduit_app_methods import *


class TestConduitApp(object):

    def setup(self):
        self.browser = webdriver.Chrome("C://Windows//chromedriver.exe")
        self.browser.maximize_window()
        self.browser.get("http://localhost:1667/")

        self.username = "teszt001"
        self.email = "teszt001@email.hu"
        self.password = "Teszt001"

    def teardown(self):
        self.browser.quit()

    # Adatkezelési nyilatkozat használata teszt
    def test_accept_cookies(self):
        div_cookie = wait_for_element(self.browser, By.XPATH, '//div[@class="cookie__bar__content"]/div')
        assert div_cookie.text == "We use cookies to ensure you get the best experience on our website. Learn More..."
        button_cookie_accept = wait_for_element(self.browser, By.XPATH, '//button['
                                                                        '@class="cookie__bar__buttons__button '
                                                                        'cookie__bar__buttons__button--accept"]')
        button_cookie_accept.click()

        cookies = self.browser.get_cookies()
        cookie = []

        for i in cookies:
            for k in i.values():
                cookie.append(k)

        assert "vue-cookie-accept-decline-cookie-policy-panel" in cookie

    # Regisztráció teszt
    def test_registration(self):
        navbar_sign_up = wait_for_element(self.browser, By.XPATH, '//a[@href="#/register"]')
        navbar_sign_up.click()

        input_registration_username = wait_for_element(self.browser, By.XPATH, '//input[@placeholder="Username"]')
        input_registration_email = wait_for_element(self.browser, By.XPATH, '//input[@placeholder="Email"]')
        input_registration_password = wait_for_element(self.browser, By.XPATH, '//input[@placeholder="Password"]')
        button_sign_up = wait_for_element(self.browser, By.XPATH, '//button[contains(text(), "Sign up")]')

        input_registration_username.send_keys(self.username)
        input_registration_email.send_keys(self.email)
        input_registration_password.send_keys(self.password)
        button_sign_up.click()

        div_title = wait_for_element(self.browser, By.XPATH, '//div[@class="swal-title"]')
        div_text = wait_for_element(self.browser, By.XPATH, '//div[@class="swal-text"]')
        button_registration_ok = wait_for_element(self.browser, By.XPATH, '//button[@class="swal-button '
                                                                          'swal-button--confirm"]')

        assert div_title.text == "Welcome!"
        assert div_text.text == "Your registration was successful!"
        button_registration_ok.click()

    # Bejelentkezés teszt
    def test_login(self):
        navbar_sign_in = wait_for_element(self.browser, By.XPATH, '//a[@href="#/login"]')
        navbar_sign_in.click()

        input_login_email = wait_for_element(self.browser, By.XPATH, '//input[@placeholder="Email"]')
        input_login_password = wait_for_element(self.browser, By.XPATH, '//input[@placeholder="Password"]')
        button_sign_in = wait_for_element(self.browser, By.XPATH, '//button[contains(text(), "Sign in")]')

        input_login_email.send_keys(self.email)
        input_login_password.send_keys(self.password)
        button_sign_in.click()

        time.sleep(1)
        navbar_elements_text_list = []

        for n in navbar_elements(self.browser):
            navbar_elements_text_list.append(n.text)

        assert self.username in navbar_elements_text_list

    # Új adat bevitel teszt
    def test_post_new_article(self):
        login(self.browser, self.email, self.password)
        time.sleep(1)
        navbar_new_article = wait_for_element(self.browser, By.XPATH, '//a[@href="#/editor"]')
        navbar_new_article.click()

        article_title = "Title of the article - Test"
        article_about = "This article is about testing..."
        article_content = "This is a test article."

        edit_article(self.browser, article_title, article_about, article_content)

        new_article_title = wait_for_element(self.browser, By.XPATH, '//h1')
        new_article_content = wait_for_element(self.browser, By.XPATH, '//div[@class="col-xs-12"]/div/p')
        author_of_article = wait_for_element(self.browser, By.XPATH, '//a[@class="author"]')

        assert new_article_title.text == article_title
        assert new_article_content.text == article_content
        assert author_of_article.text == self.username

    # Meglévő adat módosítás teszt
    def test_edit_article(self):
        login(self.browser, self.email, self.password)
        time.sleep(1)
        navbar_username = wait_for_element(self.browser, By.XPATH, '//a[@href="#/@teszt001/"]')
        navbar_username.click()
        time.sleep(1)

        article_list = wait_for_elements(self.browser, By.XPATH, '//a[@href="#/articles/title-of-the-article--test"]')
        article_list[0].click()

        button_edit_article = wait_for_element(self.browser, By.XPATH, '//a[@href="#/editor/title-of-the-article'
                                                                       '--test"]')
        button_edit_article.click()

        article_title = "Title of the article - Test2 - Edited"
        article_about = "This article is about testing...2 - Edited"
        article_content = "This is a test article.2 - Edited"

        edit_article(self.browser, article_title, article_about, article_content)

        new_article_title = wait_for_element(self.browser, By.XPATH, '//h1')
        new_article_content = wait_for_element(self.browser, By.XPATH, '//div[@class="col-xs-12"]/div/p')

        assert new_article_title.text == article_title
        assert new_article_content.text == article_content

    # Több oldalas lista bejárása teszt
    def test_navigate_in_pages(self):
        login(self.browser, self.email, self.password)
        navbar_home = wait_for_element(self.browser, By.XPATH, '//a[@href="#/"]')
        navbar_home.click()

        pages = wait_for_elements(self.browser, By.XPATH, '//a[@class="page-link"]')
        number_of_page = 1

        for p in pages[1:]:
            p.click()
            number_of_page += 1

        assert number_of_page == len(pages)

    # Kijelentkezés teszt
    def test_logout(self):
        login(self.browser, self.email, self.password)
        time.sleep(1)
        number_of_navbar_elements_before_log_out = len(navbar_elements(self.browser))
        navbar_log_out = wait_for_element(self.browser, By.XPATH, '//a[@active-class="active"]')
        navbar_log_out.click()
        number_of_navbar_elements_after_log_out = len(navbar_elements(self.browser))

        assert number_of_navbar_elements_after_log_out < number_of_navbar_elements_before_log_out
