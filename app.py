from flask import Flask, render_template, request
from generate_recomendations import fetch_tweets
import gensim
app = Flask(__name__)

@app.route('/')
def student():
    return render_template('user_input.html')

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        tweets = fetch_tweets(request.form['topic'],float(request.form['timeframe']))
        return render_template("result.html", tweets = tweets)

if __name__ == '__main__':
    app.run(debug = True)
