import time

import sys

sys.path.append("../../selenium-3.4.3")

from Logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from routers.BaseRouter import BaseRouter


class ArcherC7(BaseRouter):
    def logIn(self, username: str, password: str):
        usernameInput = self.webdriver.find_element_by_id("userName")
        usernameInput.clear()
        usernameInput.send_keys(username)

        passwordInput = self.webdriver.find_element_by_id("pcPassword")
        passwordInput.clear()
        passwordInput.send_keys(password)

        loginButton = self.webdriver.find_element_by_id("loginBtn")
        loginButton.click()
        time.sleep(2)

    def reboot(self, password):
        mainFrame = self.driverWait.until(EC.presence_of_element_located((By.NAME, "mainFrame")))
        self.webdriver.switch_to_frame(mainFrame)

        self.driverWait.until(EC.presence_of_element_located((By.NAME, "ReleaseIp"))).click()
        time.sleep(2)
       
        self.driverWait.until(EC.presence_of_element_located((By.NAME, "RenewIp"))).click()

        time.sleep(4)
        
        self.webdriver.switch_to.default_content()

        menuFrame = self.driverWait.until(EC.presence_of_element_located((By.NAME, "bottomLeftFrame")))

        self.webdriver.switch_to_frame(menuFrame)

        self.driverWait.until(EC.presence_of_element_located((By.ID, "a72"))).click()


    def logOut(self):
        menuFrame = self.driverWait.until(EC.presence_of_element_located((By.NAME, "bottomLeftFrame")))
        self.webdriver.switch_to_frame(menuFrame)

        self.driverWait.until(EC.presence_of_element_located((By.ID, "a74"))).click()
