## Download and setup:
1. Download the zip file for all files here (the name of the file should be SpeechPacer.zip. If not, rename it to this):
2. Open the CS50 IDE
4. In the top left of the CS50 IDE, press file, and in the dropdown menu press Upload Local Files. Select the zip file.
5. On the left sidebar, make sure that the zip file is in the home directory (i.e. not in any folder).
6. In a terminal, cd to your downloads folder, and execute the following commands: 
```
unzip SpeechPacer.zip
cd SpeechPacer
flask run
```
7. Use the link to open the webpage

## Tutorial (please use the latest version of Google Chrome for maximum compatibility):
1. On the top right, register for a new account by entering an entername and password
2. After you submit, you should be directed to the log in page. Login with the same information you just put in.
3. In the top navbar, click exercises to be brought to the exercises screen.
4. IMPORTANT: in your search bar, ensure that there is a small lock to the left of the URL. If you instead see the message "Not Secure", do the following:
 a. Close your current tab for SpeechPacer
 b. Without rerunning flask, click the link in the terminal again
 c. Proceed directly to the exercises page
 d. You should still be logged in, but the page should now be secure
 e. this is caused by the fact that the page doesn't have a certificate (yet). An insecure connection disables the microphone and other
    utilities, and thus havine a secure connection is paramount for this webpage.
 f. If this still doesn't work, try quitting the browser and trying again, but do not click the "exercise tab" immediately without
    being logged in. Log in first through the login button, and then press the exercise tab.
 g. If the microphone is indeed working, you should see a circle symbol on your tab at the top.
5. You should see that your speed as of right now is 50 words per minute. Everyone starts off as this in the beginning
6. Click the "Listen to sample" button to hear the computer read out a passage at that speed, for your reference.
7. When you're ready, click the Start Exercise! Button, and begin to read out your passage as they become bolded
 a. Make sure to speak as clearly as possible, as the speech recognition API is still experimental.
8. After your passage is done, you should see a results screen with your statistics and your change in speed
 a. Doing well results in a speed increase and vice versa, with the amount being proportional to how well you've done.
9. Clicking away from the results screen will automatically reload the page and save your results and new speed. You may try again!
 a. Make sure that the webpage is still secure (indicated by a lock), rather than "Not Secure", or else there will be no results.

## Demo: 
https://user-images.githubusercontent.com/56591145/188769014-6aedd35a-aa10-4169-94ce-f0e351f517fe.mp4

