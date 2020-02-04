# MeinCampusCrawler
Script to check for exam results

How to use:

1. Install Python  
The script was written and tested with Python 3.7.4

2. Install the following packages:  
`pip3 install selenium`  
`pip3 install selenium`  

3. Choose a Browser and download the coresponding webdriver  
*Firefox:* download [geckodriver](https://github.com/mozilla/geckodriver/releases) and save it to the same directory as the script.  
*Chromium (Raspbian):* To be tested.  
Other browsers haven't been tested but might work as well.  

4. Change the variables to your needs.  
There are two parts of the code that you want to edit:  
* Your credentials/email details (Can be found at the top of the code)
  * you need to enter sour SSo credentials
  * you need to enter the credentials of the mailserver
* Choose you course of study  
If you are or have been enlisted in more then one course of study you have to choose which one you want to check. To specify which one you want, you must edit the variable studdienGang to either std0 or std1 (see image).  
![Screenshot of Studiengang](studiengang.png "Screenshot")

5. Arrange recurring execution  
*Windows:* Use task schedueler.  
*Linux/Raspbian:* Use crontab.


How it works:  
This python script launches a browser instance and navigates to the tabel of exam results. It than checks if the table differs from the last time it checked and if so, it'll send an email with the delta to your mail adress.
