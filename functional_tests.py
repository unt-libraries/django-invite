from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from django.conf import settings
import unittest
import time


class FunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser2 = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser2.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        self.browser2.quit()


class TestFunctional(FunctionalTestCase):
    def test_one_basic_invite(self):
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
        # click send
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/form/div[3]/div[4]/div[2]/input').click()
        body = self.browser.find_element_by_tag_name('body')
        time.sleep(1)
        self.assertIn('Jayjay', body.text)
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/div/div[2]/table/tbody/tr[2]/td[3]/form/input').click()

    def test_one_complex_invite_and_registration(self):
        # grab a trash email address
        self.browser2.get('http://mailinator.com/')
        email = self.browser2.find_element_by_id('inboxfield').send_keys('jayjayjetplane@mailinator.com')
        self.browser2.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/div/btn').click()
        # joey opens the browser and goes to the  url
        self.browser.get('http://129.120.93.131:8000/accounts/')
        self.browser.find_element_by_name('username').send_keys('test')
        self.browser.find_element_by_name('password').send_keys('test')
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/form/input').click()
        # click the invite button
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/div/a').click()
        # type in our username and password and send the return key
        self.browser.find_element_by_name('form-0-first_name').send_keys('jayjay')
        self.browser.find_element_by_name('form-0-last_name').send_keys('jetplane')
        self.browser.find_element_by_name('form-0-username').send_keys('jetplane')
        self.browser.find_element_by_name('form-0-email').send_keys('jayjayjetplane@mailinator.com')
        # make superuser
        self.browser.find_element_by_xpath('//*[@id="id_form-0-is_super_user"]').click()
        self.browser.find_element_by_name('form-0-greeting').send_keys('This is a custom greeting that will be send to all email addresses.')
        # select the permissions and groups
        select = Select(self.browser.find_element_by_id('id_form-0-permissions'))
        select.select_by_visible_text('invite | invitation | Can add invitation')
        groups = Select(self.browser.find_element_by_id('id_form-0-groups'))
        groups.select_by_visible_text('ALL INVITE')
        # click send
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/form/div[3]/div[4]/div[2]/input').click()
        body = self.browser.find_element_by_tag_name('body')
        time.sleep(1)
        self.assertIn('Jayjay', body.text)
        # give a bit of time for the email to arrive.
        time.sleep(15)
        self.browser2.get('http://mailinator.com/inbox.jsp?to=jayjayjetplane')
        self.browser2.find_element_by_xpath('//*[@id="mailcontainer"]/li[1]/a/div[1]').click()
        self.browser2.find_element_by_xpath('//*[@id="mailshowdiv"]/div[3]/div/div/a').click()
        window_handles = self.browser2.window_handles
        self.browser2.switch_to_window(window_handles[1])
        self.browser2.find_element_by_xpath('//*[@id="id_password"]').send_keys('password')
        self.browser2.find_element_by_xpath('//*[@id="id_password2"]').send_keys('password')
        self.browser2.find_element_by_xpath('//*[@id="body"]/div[2]/div/div/form/div[5]/input').click()

    def test_eleven_basic_invites(self):
        # joey opens the browser and goes to the  url
        self.browser.get('http://129.120.93.131:8000/accounts/')
        self.browser.find_element_by_name('username').send_keys('test')
        self.browser.find_element_by_name('password').send_keys('test')
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/form/input').click()
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/div/a').click()
        for i in range(10):
            self.browser.find_element_by_xpath('//*[@id="add"]/i').click()
        for i in range(11):
            # type in data
            self.browser.find_element_by_name('form-%s-first_name' % i).send_keys('jayjay')
            self.browser.find_element_by_name('form-%s-last_name' % i).send_keys('jetplane')
            self.browser.find_element_by_name('form-%s-username' % i).send_keys('jetplane')
            self.browser.find_element_by_name('form-%s-email' % i).send_keys('asdf@asdf.asdf')
        # click send
        self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/form/div[3]/div[4]/div[2]/input').click()
        body = self.browser.find_element_by_tag_name('body')
        time.sleep(1)
        self.assertIn('Jayjay', body.text)
        # delete the invites
        for i in range(11):
            self.browser.find_element_by_xpath('//*[@id="body"]/div[2]/div/div/div[2]/table/tbody/tr[2]/td[3]/form/input').click()


if __name__ == '__main__':
    unittest.main()
