import os
import sys
import time
import difflib
import smtplib
from selenium import webdriver
from pyvirtualdisplay import Display
from email.message import EmailMessage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Your SSO credentials go here
ssoID = "YOUR_SINGLE_SIGN_ON_ID"
ssoPW = "YOUR_SINGLE_SIGN_ON_PASSWORD"

# Your mailserver details go here
mailServerID = "YourMailAddress@Example.de"
mailServerPW = "PasswordForYourMailAddress"
mailServerAdress = "" # Look it up at your mail host. It usually starts with smtp (e.g. smtp.web.de)
mailServerSmtpPort = 587 # Look it up at your mail host. 587 is a common one
targetMailAddress = "TheMailToWhichYourNotificationGoes@fau.de"

# general config
pathToBufferFile = "spiegel"
studienGang = "stg1"
hideBrowser = 0 # 0=hide 1=show

# Change dir to location of this script
os.chdir(sys.path[0])

def sendMail(message):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Note ist Online!'
    msg['From'] = mailServerID
    msg['To'] = targetMailAddress

    s = smtplib.SMTP(host=mailServerAdress, port=mailServerSmtpPort, timeout=30)
    s.starttls()
    s.login(mailServerID, mailServerPW)
    s.send_message(msg)
    s.quit()

def fetchNoten():
    #create a virtual display
    display = Display(visible=hideBrowser, size=(640, 480))
    display.start()
    #open a browser
    driver = webdriver.Chrome()
    driver.set_script_timeout(30) # seconds
    driver.set_page_load_timeout(30) # seconds
    try:
        #open MeinCampus
        driver.get("https://www.campus.uni-erlangen.de/")
        loginButton = driver.find_element_by_id("iconSSO")
        loginButton.click()

        #Login on SSO 
        next_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))
        driver.find_element_by_id("username").send_keys(ssoID)
        driver.find_element_by_id("password").send_keys(ssoPW)
        driver.find_element_by_id("submit_button").click()

        #navigate to Notenspiegel
        next_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "pruefungen")))
        driver.find_element_by_id("pruefungen").click()
        driver.find_element_by_xpath('//*[@id="notenspiegelStudent"]').click()
        # The following click might only be necessary if you are able to choose between
        #more than one course of study (i.e. you finished bachelor and started master,
        #now you have to choose which exam results you want to see)
        if driver.find_element_by_id("selectStg"):
            driver.find_element_by_id(studienGang).click()
            driver.find_element_by_name("submit").click()
        notenspiegel = driver.find_element_by_id("notenspiegel").text
    except:
        print("Something went wrong!")
        notenspiegel = ""
    finally:
        driver.close()
        display.stop()
    return notenspiegel

def checkForDeltas(newVersion):
    #validate
    if newVersion is None:
        return

    if newVersion == "":
        return

    # Create buffer file if it doesn't already exist
    if not os.path.isfile(pathToBufferFile):
        newfile = open(pathToBufferFile, 'w+')
        newfile.close()

    #buffer old version
    with open(pathToBufferFile, 'r') as f:
        oldVersion = f.read()
    f.close()

    #check for diff
    if newVersion != oldVersion:
        #collect diff
        newEntries = ""
        for line in newVersion.splitlines():
            if line not in oldVersion:
                newEntries = newEntries + line + "\n"

        #send report mail
        try:
            sendMail(newEntries)
        except:
            print("Error while sending Email!")
        print(newEntries)

    #save the new version
    with open(pathToBufferFile, 'w') as f:
        f.write(newVersion)
    f.close()

ns = fetchNoten()
checkForDeltas(ns)
