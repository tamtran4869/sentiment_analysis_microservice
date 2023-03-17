import os
cwd = os.getcwd()
import scrape_social as ss
import warnings
warnings.filterwarnings('ignore')
from flask import Flask, request, jsonify,render_template
from transformers import pipeline
from googletrans import Translator
import time

# Innitial variables, translator and pre_trained sentiment model                          
lab_dict ={ 'LABEL_2' : 'Positive',
            'LABEL_1' : 'Neutral',
            'LABEL_0' : 'Negative'
            }
translator = Translator()
sentiment_analysis = pipeline('sentiment-analysis',model='cardiffnlp/twitter-roberta-base-sentiment')

# Build app
app = Flask(__name__)
app.app_context().push()
@app.route("/", methods=["GET", "POST"])
def sentiment():
    '''
    Get information from the form.
    Use scrape social (ss) program to get comment from the post, clean data and predict sentiment label
    Return sentiment analysis and detail comments in the html template
    '''
    if request.method == "POST":
        type = request.form['type']
        print(type)
        url = request.form['url']
        print(url)
        bearer = request.form['bearer']
        print(bearer)
        print('---------------------')
        if request.form['analysis_button']=='Analysis':
            try:
                label =[]
                en = []

                if str.lower(type) == "facebook":
                    df = ss.get_fb_comments(url)
                if str.lower(type) == "twitter":
                    if not bearer:
                        return render_template('form.html',result = "Add bearer key for twitter sentiment")
                    else:
                        tweet_ID = url.split("/")[-1]
                        df = ss.get_twt_comments(tweet_ID,bearer)

                df = ss.clean_data(df)
                for cmt in df.cmt:
                    print(cmt)
                    if translator.detect(cmt).lang != 'en':
                        en_cmt = translator.translate(cmt,dest='en').text
                        time.sleep(0.005)
                    else:
                        en_cmt = cmt
                    out = sentiment_analysis(en_cmt)
                    print(out)
                    label.append(lab_dict[out[0]['label']])
                    en.append(en_cmt)

                df['en'] = en
                df["target"]= label
                outcome = df.target.value_counts().to_dict()
                res = render_template('form.html',
                                      result = outcome, 
                                      tables = [df.to_html()], 
                                      titles=df.columns.values,
                                      url = url)
                return res
            except Exception as e:
                return render_template('form.html',result = jsonify({"error": str(e)}))
    return render_template('form.html',result = None, tables = [],url = None)


if __name__ == "__main__":
    app.run(debug=True)

