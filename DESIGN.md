For the website, I decided to use flask, HTML, and javascript simply because of the templating abilities of flask
and for how quickly we can also integrate SQL commands into flask. From using flask and HTML for C$50 finance, I believed that
using flask and HTML was the best way to quickly create a lightweight website as opposed to using other alternatives like PHP.
It also allowed for rapid testing as I could simply run "flask run" in the CS50 IDE to see the website.

I chose to use bootstrap because we were familiar with it, and also because of it's extensive documentation. For the website itself,
I didn't include any pictures or much decorations. This is because I believe the function of the website comes before the aesthetics.
I made sure that the texts were properly aligned and intuitively grouped, however, in order to make sure the website served its
purpose well.

For the home page I decided that a simple home page with some information about what this website serves to do would suffice,
as it would also serve as a navigation center for the other links. I wanted to make sure what I was doing through the website
is backed up by science and believable, hence why I included the link to the Westmead Program in it.

For the exercise page, in terms of aesthetics, I tried to make sure everything was straightforward and immediatley understandable -
Hence the three big sections: your speed, the sample, and your passage.The flow is designed to easily allow any user to understand
that they should first take note of their speed, listen to the sample for an idea of how fast they should speak, and proceed with the
exercise.

For the login system, I tried to make it as bare-bones as possible so that users can register and sign in as quick as possible.
Using much of the same logic as C$50 finance, the register page only has a username and password field, the latter of which is hashed,
which is then inserted into a database along with a user_id. The login page is identical, but instead checks the database to see
if the username and passwords match, and if so, a session will be created and the user_id will be included.

The login system was important because I wanted to make sure users can slowly improve as they visit the website. The website stores,
in a seperate table, their current reading speed, and as they speak clearer and faster, that speed should slowly increase. The
Westmead program isn't supposed to be done in a day, and the login system is to make sure users can save their progress and continue
where they left off. This speed is then requested from the database and used for the exercises.

For the exercise's code, I first designed the sample reader as a way to help users listen to an "ideal" speed at which they should
talk. For this, I used the web speech API included in modern browsers.Unfortunately, the pauses and lengths of each word were erratic
using the speech synthesis API (we've come a long way from "robot talk"!), and thus I had to write code to manually slow down the rate
at which the machine speaks in proportion to the speed, as well as forcibly pause the reading in between words through calculating how long it
took to say the word, and how many millisecondsit would take in order for the targetted milliseconds per word to be reached.
I also made sure to include a stop button in caseusers decided they didn't want to listen any more, to prevent
having them wait for the sample to finish.

For the actual passage reading code, it was a bit more complicated. In order to recognize speech I used a speech recognition API that
is included in modern browsers, and used events to call functions whenever a word is detected. First of all, the speech recognition API is still experimental,
and thus it doesn't exactly produce the most optimal results. Sometimes it returns multiple words, and sometimes it didn't recognize
a word. For this reason I had to iterate through the entire list of recognized words, matching words with the actual text passage, and
accounting for missing words the computer didn't recognize. I also included a "karaoke"-like style system where each word will be bolded
when they are supposed to be spoken, to help the user pace themselves, which was done through a setInterval() bolding words one by one.
As each word also includes a "confidence" attribute and a "timestamp", I used those attributes as a way to determine how clearly the user spoke
(along with the number of missed words), as well as their overall pacing. For confidence, I simply averaged the confidence attributes of each detected word.
For pacing, I had to determine how much time it took for each word in the passage to be read, and then subtracted that with how much time each word should take,
before averaging all of these differences. All of these data - pacing average, accuracy average, and missing words were used to
create a results screen, as I wanted the user to see their performance and reflect. They are also used to determine the change in the
user's speaking speed. If their averages were very low and missed a lot of words, their speed would decrease a lot for them to practice
more in the lower regions. If they scored very well, their speed increased instead. I decided to cap the speed increase to 2 (which
would require perfect averages and no missed words) as I didn't want users to move up too quickly. The Westmead program is a slow
process, and reducing stuttering takes time. Lastly, I also included a stop function to the reading, which would prematurely stop
the passage in case something happens. However, it would usually lead to a loss in reading speed as many words would be missed, which
was intentional on my part as I didn't want users saying one word, getting perfect accuracy, missing words, and pacing, and stopping
immediately.

After all of this, the user's new speed is calculated and via a POST request to flask, updated in the database, and the user can then
go for another exercise. I purposely made it redirect back to the exercise page to encourage users to continue practicing, striving to
do better next time and keep improving. I decided to put no upper limit on how fast a user's speed can be, in case users might want to
use the website as a way to train for rapping or speed talking.