# Recommender System
 In this project, I wrote an app that takes topic and
sub-topic and time T as input data and returns the most relevant streaming
tweets to the topic and sub topic in the last T seconds. The streaming tweets
are collected, cleaned and vectorized to get the result.

Here are a list of descriptions for each folder in this reposition.
-  *jupyter notebooks/twitter_proj.ipynb*

   A notebook that documents the steps for 
   - saving  streaming related  tweets to the topic in the given time frame
   - cleaning and pre-processing the saved tweets
   - vectorization using the pretrained model GoogleNews-vectors-negative300.bin
   - returning the most similar tweets related to the given topic and sub-topic by means of the similarity score 
-  *Twitter/scripts/lib*

   contains 

   - *data_collection.py*

      gets the latest tweets for the topic for the time frame

   - *data_preprocessing.py*
     
     cleaning, and vectorizing  given tweets

   - *generate_recomendations.py*
    
     generats the most related tweets to the user inpot topic and sub-topic
-  *app.py*

   a Flask app that user  submits  Sub-Topic, Topic and Timeframe  at /user_input.html and  it returns 
   the most relevent tweets at /results.html
- *Twitter/scripts/front-end/user_input.html*

  a table for the user to submit Sub-Topic, Topic and Timeframe
- *Twitter/scripts/front-end/results.html*
  
  a table of results of the related tweets is saved here.
  
