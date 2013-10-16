from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from django.conf import settings
import unittest
import time


class FunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


class TestFunctional(FunctionalTestCase):
    def test_one_invite(self):
        # joey opens the browser and goes to the  url
        self.browser.get('http://129.120.93.131:8000/accounts/')
        self.browser.find_element_by_name('username').send_keys('test')
        self.browser.find_element_by_name('password').send_keys('test')
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/form/input').click()
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/div/a').click()
        # type in our username and password and send the return key
        self.browser.find_element_by_name('form-0-first_name').send_keys('jayjay')
        self.browser.find_element_by_name('form-0-last_name').send_keys('jetplane')
        self.browser.find_element_by_name('form-0-username').send_keys('jetplane')
        self.browser.find_element_by_name('form-0-email').send_keys('asdf@asdf.asdf')
        # notice a link to the EOT_PDF model admin and click it
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/form/div[3]/div[4]/div[2]/input').click()
        body = self.browser.find_element_by_tag_name('body')
        time.sleep(1)
        self.assertIn('Jayjay', body.text)
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/div/div[2]/table/tbody/tr[2]/td[3]/form/input').click()


if __name__ == '__main__':
    unittest.main()
