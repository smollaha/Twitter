from flask import Flask, render_template, request
from generate_recomendations import fetch_tweets
import gensim
app = Flask(__name__)
model = None

def load_model():
    global model
    print('uploading the model...')
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = True)
    print('model loaded successfully!')
    
@app.route('/')
def student():
    return render_template('user_input.html')

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        tweets = fetch_tweets(model, request.form['sub_topic'],request.form['topic'],float(request.form['timeframe']))
        return render_template("result.html", tweets = tweets)

if __name__ == '__main__':
    load_model()
    app.run(debug = True)
