golf-text
=========

SMS-based golf score recording app.  This web app is built to receive sms (text message) requests for
managing rounds of golf and calculating scores.

Basic commands are as follows:  

"create" - adds a new entry into the players table associated with the number sending the text  
"round" - creates a new round and associates the round to the player sending the text  
"score **number**" - adds the submitted score to the running total for the round currently associated to the player  
"score" - returns the current score for the current round  
"name **name**" - sets the player name for the associated number, defaults to 'golfer'  
"combine **player_name** **player_name**" - combines the current round scores for the two players, return net score  
"compare **player_name** **player_name**" - compare two players and return the stroke winner  
"match **team1_player_name** **team1_player_name** **team2_player_name** **team2_player_name** - combine the scores for each team and compare with other team, returning winning pair  

I use [Plivo](http://www.plivo.com) to handle the SMS sending/receiving so all I have to do is deal with the
request query and returning the XML response, which I do with [web.py](http://webpy.org).
