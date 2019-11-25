# Recommender System
 In this project, I wrote an app that takes topic and
sub-topic and time T as input data and returns the most relevant streaming
tweets to the topic and sub topic in the last T seconds. The streaming tweets
are collected, cleaned and vectorized to get the result.

Here are a list of descriptions for each folder in this reposition.
-  *jupyter notebooks/twitter_proj.ipynb*

   A notebook that documents the steps 
   - save streaming related  tweets to the topic in the given time frame
   - clean and pre-process the saved tweets
   - vectorization using the pretrained model GoogleNews-vectors-negative300.bin
   - return the most similar tweets related to the given topic and sub-topic by means of the similarity score 
-  *Twitter/scripts/lib*

   contains 

   - *data_collection.py*

      gets the latest tweets for the topic in the time frame

   - *data_preprocessing.py*
     
     cleans and vectorizes  given tweets

   - *generate_recomendations.py*
    
     generates the most related tweets to the user input topic and sub-topic
-  *app.py*

   a Flask app that user  submits  Sub-Topic, Topic and Timeframe  at /user_input.html and  it returns 
   the most relevant tweets at /results.html
- *Twitter/scripts/front-end*
   - */user_input.html*

     a table for the user to submit Sub-Topic, Topic and Timeframe
    - */results.html*
  
      a table of results of the related tweets is saved here.
  
