from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login=driver.find_element(By.CSS_SELECTOR,"img[src='/static/assets/images/profile.png']")
        login.click()
        time.sleep(2)
        email = driver.find_element(By.CSS_SELECTOR, "input[type='email'][name='email']")
        email.send_keys("romeo@gmail.com")
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][name='pass']")
        password.send_keys("Sergio@327")
        time.sleep(2)
        submit=driver.find_element(By.CSS_SELECTOR,"button#button")
        submit.click()
        time.sleep(2)
        if "http://127.0.0.1:8000/" in driver.current_url:
            print("Test Passed")
        else:
            print("Test Failed")
        self.assertIn("http://127.0.0.1:8000/", driver.current_url)


        # product=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/list']")
        # product.click()
        # time.sleep(2)
       
        # cart=driver.find_element(By.CSS_SELECTOR,"a.nav-link > img")
        # cart.click()
        # time.sleep(2)
        


if __name__ == '__main__':
    import unittest
    unittest.main()