import os
import sys

sys.path.append("de.marius")
sys.path.append("selenium-3.4.3")

from configparser import ConfigParser

from selenium.common.exceptions import WebDriverException

from routers.BaseRouter import BaseRouter

from routers.RouterFactory import RouterFactory
from selenium import webdriver
from DriverSetup import DriverSetup
from Logger import Logger, LogLevel

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

import time

import datetime


def initConfig():
    config = ConfigParser()
    configPath = os.path.join(os.getcwd(), "Config.ini")
    config.read(filenames=configPath)
    sections = config.sections()
    if len(sections) == 0 or (not sections.__contains__("actions")):
        Logger.logInfo("Config file is empty. Bye!")
        quit()
    if len(config.items("actions")) == 0:
        Logger.logInfo("Nothing to do. Bye!")
        quit()
    return config


def handleRouterTask(router: BaseRouter, username: str, password: str, task: str):
    # ToDo: this can be done a lot nicer

    if task == 'login':
        router.logIn(username, password)
    elif task == 'reboot':
        router.reboot(password)
    elif task == 'logout':
        router.logOut()


def performActions(driverPath: str, config: ConfigParser, actions):
    Logger.logInfo("")
    for action in actions:
        Logger.logInfo("Performing action: " + action)
        webInterfaceUrl = config.get(action, "routerIP")
        username = config.get(action, "username")
        password = config.get(action, "password")
        tasks = config.get(action, "tasks")
        tasks = [task.strip() for task in tasks.split(',')]
        Logger.logInfo("IP: " + webInterfaceUrl
                       + " username: " + username
                       + " password: " + password
                       + " tasks: " + tasks.__str__())

        driver = webdriver.Chrome()
        router = RouterFactory(driver, webInterfaceUrl).getRouter()
        for task in tasks:
            tryHandleRouterTask(password, router, task, username)
        driver.close()
        Logger.logInfo("Finished action: " + action)
        Logger.logInfo("")
    Logger.logInfo("##### Router Automator Done #####")
    Logger.logInfo("")


def tryHandleRouterTask(password, router, task, username):
    try:
        handleRouterTask(router, username, password, task)
    except Exception as wde:
        Logger.logError("Performing task '" + task + "' produced exception: " + wde.__str__())
    except:
        Logger.logError("Unknown exception while performing task '" + task + "'")
    finally:
        Logger.logInfo("Performed task: " + task)

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

# Initialize logging
Logger.init("RouterAutomator.log", LogLevel.INFO)

# Initialize the webdriver
Logger.logInfo("")
Logger.logInfo("####### Router Automator #######")
driverSetup = DriverSetup()
driverSetup.init()

# Parse the Config
config = initConfig()

flag = 1
while (flag):

    time.sleep(30)
    if not ping("www.google.com"):
        # Run any active actions
        activeActionTuples = filter(lambda action: action[1] == 'true', config.items("actions"))
        activeActionNames = map(lambda action: action[0], activeActionTuples)
        performActions(driverSetup.getDriverPath(), config, activeActionNames)
        print("Renew network at ")
        currentDT = datetime.datetime.now()
        print (currentDT.strftime("%Y-%m-%d %H:%M:%S"))



