# MeinCampusCrawler  
**What?**  
A script to check for new exam results on [mein Campus](https://www.campus.uni-erlangen.de).  

**Why?**  
[Because I should be studying right now](https://en.wikipedia.org/wiki/Procrastination).  

**How?**  
This python script launches a browser instance and navigates to the table of results. It than checks if the table differs from the last time it checked and if so, it'll send an email with the delta to your mail address.

**What do I need?**
* Preferably a Raspberry Pi. Because of it's cross-platform functionality, the python script should work on Windows as well (with minor changes) but it hasn't been tested.
* Two mail addresses: one is used to send a notification and the one you want to receive the notification.

**How to use:**
1. Install Python  
The script was written and tested with Python 3.7.4  
`sudo apt-get install python3`

2. Install the following packages:  
`pip3 install selenium`  
`pip3 install pyvirtualdisplay`  

3. Choose a Browser and download the corresponding webdriver  
**Firefox:** download [geckodriver](https://github.com/mozilla/geckodriver/releases) and save it to the same directory as the script.  
**Chromium (Raspbian):** To be tested.  
**Other browsers** haven't been tested but might work as well.  

4. Change the variables to your needs.  
There are several variables that you want to edit:  
* Your credentials/email details
  * you need to enter your SSO credentials
  * you need to enter the credentials of the mailserver
* Choose your course of study  
If you are or have been enlisted in more then one course of study you have to choose which one you want to check. To specify which one you want, you must edit the variable studdienGang to either std0 or std1 (see image).  
![Screenshot of Studiengang](studiengang.png "Screenshot")

5. Arrange recurring execution  
**Windows:** Use task schedueler.  
**Linux/Raspbian:** Use [crontab](https://crontab-generator.org/).


