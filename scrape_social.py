import tweepy
from facebook_scraper import get_posts
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from googletrans import Translator
translator = Translator()
import warnings
warnings.filterwarnings('ignore')

def get_replies(replies, id):
    '''
    Get replies on 1 comment on a FB post
    '''
    rep = pd.DataFrame(range(id+1, id+1+len(replies)),columns=["id"])
    rep["cmt"] = np.nan
    rep["parent_id"] = id
    x = 0
    for reply in replies:
        rep.loc[x,"cmt"] = reply.get("comment_text")
        x+=1
    return rep

def get_fb_comments(post_url):
    '''
    Get comments and replies from a facebook post
    '''
    post = get_posts(post_urls=[post_url], 
                     extra_info = True, 
                     options = {"comments":True}, 
                     cookies=None)
    df = pd.DataFrame.from_dict(post)
    lst = df["comments_full"][0]
    cmt = pd.DataFrame(columns=["id", "cmt","parent_id"])
    cnt = 0
    for i in lst:
        cmt.loc[cnt,"id"] = cnt
        cmt.loc[cnt,"cmt"] = i.get("comment_text")
        replies = i.get("replies")
        if replies:
            rep = get_replies(replies,cnt)
            cmt = cmt.append(rep)
        cnt = len(cmt)
    return pd.DataFrame(cmt["cmt"])

def get_twt_comments(tweet_ID,bearer):
    '''
    Get comments on a tweets
    '''
    t_c = tweepy.Client(bearer_token=bearer)
    q = f"conversation_id:{tweet_ID} is:reply"
    ts= tweepy.Paginator(t_c.search_recent_tweets, 
                              query=q, 
                              max_results=100).flatten(limit=10000)
    lst=[]
    for t in ts:
        lst.append(t)
    trimmed_lst = [str(i) for i in lst]
    rep = pd.DataFrame(trimmed_lst,columns=["cmt"])
    return  pd.DataFrame(rep['cmt'])

def clean_data(df):
    """ Function for cleaning data, and process steps tp preapare data for sentiment analysis
    including: remove users and link, remove punctuations, remove stopwords
    and lemmatizate text
    """
    df.columns = ["cmt"]
    t = df.cmt.reset_index(drop = True)

    # Remove user mentions including @ and user name; links
    t = t.str.replace('@[^\s]+','')
    t = t.str.replace("http\S+", "")

    # Remove punctuations 
    t = t.str.replace('[^\w\s]','')

    #Remove stopwords
    stop = stopwords.words('english')
    t = t.apply(lambda x: " ".join([str.lower(x) for x in x.split() if x not in stop]))

    # Drop NA
    nan_sum = t.isna().sum().sum()
    if(nan_sum>0):
        print(nan_sum, " NAN found\nremoved...")
        t = t.dropna()
    else:
        print("no NAN found")    

    # Drop duplicates
    dupli_sum = t.duplicated().sum()
    if(dupli_sum>0):
        print(dupli_sum, " duplicates found\nremoved...")
        t = t.loc[False==t.duplicated()]
    else:
        print("no duplicates found")

    #Lemmatization for removing tenses and transform words into its original forms.
    lemmatizer = WordNetLemmatizer()
    def lemmatize_text(s):
        new = " ".join([lemmatizer.lemmatize(w) for w in s.strip().split(" ")])
        return new
    t = t.apply(lemmatize_text)
    t= pd.DataFrame(t)
    t = t[t.cmt.isin([' ',''])==False]
    return t
