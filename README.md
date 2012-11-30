golf-text
=========

SMS-based golf score recording app.  This web app is built to receive sms (text message) requests for
managing rounds of golf and calculating scores.

Basic commands are as follows:  

"create" - adds a new entry into the players table associated with the number sending the text  
"round" - creates a new round and associates the round to the player sending the text  
"score **number**" - adds the submitted score to the running total for the round currently associated to the player  
"score" - returns the current score for the current round  
"name" - sets the player name for the associated number, defaults to 'golfer'

I use [Plivo](http://www.plivo.com) to handle the SMS sending/receiving so all I have to do is deal with the
request query and returning the XML response.
