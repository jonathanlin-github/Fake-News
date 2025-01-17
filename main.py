import tweepy
import requests
from time import sleep
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score
import urllib.request
import requests
from bs4 import BeautifulSoup




def extractText(url):

    #this functions extracts the text that's the article from the link
    response = requests.get(url)
    sleep(2)
    url = response.url

    #get requests to website
    r1 = requests.get(url)
    page = r1.content

    #create a soup reading the HTML of the page
    soup = BeautifulSoup(page, 'html5lib')

    #specific class is the class name that contains the paragraph
    #websites this doesn't support:
    #wsj.com because paywall
    #time.com because paywall
    #buzzfeednews.com cuz html configuration
    #ft.com because paywall
    #telegraph.co because issues w extracting text
    #cbc.ca because issues w extracting text
    #bloomberg.com because issues w extracting text
    #popsci.com because issues w extracting text

    class_name = [] #name of class. This class name can either be the class holding all of the paragraphs (in this case the paragraphs don't have a class name) or it can be the names of the duplicate classes holding all of the text. is an array because some websites may have diff class names depending on the article
    class_type = '' #this will change depending on the class type holding the words. can be p, span, div, etc.
    method_type = 0 #method type 0 is defult. method type 1 is needing a browser agent replicating a mobile device
    if 'nytimes.com' in url:
        class_name.append('css-iynevi evys1bk0')
        method_type = 0
        class_type = 'p'
    elif 'medium.com' in url:
        class_name.append('meteredContent')
        method_type = 0
        class_type = 'article'
    elif 'foxnews.com' in url:
        class_name.append('article-body')
        method_type = 0
        class_type = 'div'
    elif 'tmz.com' in url:
        class_name.append('article__blocks clearfix')
        method_type = 0
        class_type = 'div'
    elif 'buzzfeed.com' in url:
        class_name.append('js-subbuzz__title-text')
        method_type = 0
        class_type = 'span'
    elif 'cnn.com' in url:
        class_name.append('zn-body__paragraph')
        method_type = 0
        class_type = 'div'
    elif 'bbc.com' in url:
        class_name.append('ssrcss-83cqas-RichTextContainer e5tfeyi2')
        class_name.append('css-83cqas-RichTextContainer e5tfeyi2')
        method_type = 0
        class_type = 'div'
    elif 'economist.com' in url:
        class_name.append('article__body-text')
        method_type = 0
        class_type = 'p'
    elif 'reuters.com' in url:
        class_name.append('Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
        method_type = 0
        class_type = 'p'
    elif 'abcnews' in url:
        class_name.append('Article__Content story')
        method_type = 0
        class_type = 'section'
    elif 'apnews.com' in url:
        class_name.append('Article')
        method_type = 0
        class_type = 'div'
    elif 'ndtv.com' in url:
        class_name.append('sp-cn ins_storybody')
        method_type = 0
        class_type = 'div'
    elif 'huffpost.com' in url:
        class_name.append('content-list-component yr-content-list-text text')
        method_type = 1
        class_type = 'div'
    elif 'latimes.com' in url:
        class_name.append('page-article-body')
        method_type = 1
        class_type = 'div'
    elif 'nbcnews.com' in url:
        class_name.append('article-body__content')
        method_type = 0
        class_type = 'div'
    elif 'theguardian' in url:
        class_name.append('css-38z03z')
        method_type = 0
        class_type = 'p'
    elif 'sky.com' in url:
        class_name.append('sdc-article-body sdc-article-body--story sdc-article-body--lead')
        method_type = 0
        class_type = 'div'
    elif 'newsweek.com' in url:
        class_name.append('article-body clearfix paywall')
        class_name.append('article-body v_text paywall')
        method_type = 1
        class_type = 'div'
    elif 'cnbc.com' in url:
        class_name.append('ArticleBody-articleBody')
        method_type = 0
        class_type = 'div'
    elif 'france24.com' in url:
        class_name.append('t-content__body u-clearfix')
        method_type = 1
        class_type = 'div'
    elif 'rt.com' in url:
        class_name.append('article__text text')
        method_type = 0
        class_type = 'div'
    elif 'independent.co' in url:
        class_name.append('sc-pTSbw gOmWnw')
        method_type = 1
        class_type = 'div'
    elif 'xinhuanet.com' in url:
        class_name.append('content')
        method_type = 0
        class_type = 'div'
    elif 'aljazeera.com' in url:
        class_name.append('wysiwyg wysiwyg--all-content')
        method_type = 0
        class_type = 'div'
    elif 'espn.com' in url:
        class_name.append('article-body')
        method_type = 1
        class_type = 'div'
    elif 'nationalgeographic' in url:
        class_name.append('content parsys')
        method_type = 0
        class_type = 'div'
    elif 'npr.org' in url:
        class_name.append('story')
        method_type = 0
        class_type = 'article'
    elif 'bloomberg.com' in url:
        #fix bloomberg
        class_name.append('body-copy-v2 fence-body')
        method_type = 1
        class_type = 'div'
    elif 'news.yahoo.com' in url:
        class_name.append('caas-body')
        method_type = 0
        class_type = 'div'
    elif 'wired.com' in url:
        class_name.append('article__chunks')
        method_type = 0
        class_type = 'div'

    


    entire_text = ''
    if method_type == 0:
        #this combines all of the text in the children of the parent class (the div is parent and pargraphs r children nodes)
        soup = BeautifulSoup(r1.text, 'html.parser')

        #it uses this because there may be different class names depending on the website
        for cn in class_name:
            page_content = soup.find_all(class_type , class_ = cn)
            #for each class, combine the texts of the paras together
            for para in page_content:
                entire_text = entire_text + para.get_text()
        
    if method_type == 1:
        #this method impersonates a mobile browser because some websites block the http requests module
        headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
        }
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        #it uses this because there may be different class names depending on the website
        for cn in class_name:
            page_content = soup.find_all(class_type , class_ = cn)
            #for each class, combine the texts of the paras together
            for para in page_content:
                entire_text = entire_text + para.get_text()


    return entire_text

print('----------Fake News Classifier Model Stats----------')


#PAC model taken from youtube, mainly https://www.youtube.com/watch?v=z_mNVoBcMjM&ab_channel=SATSifaction and then a few other videos

#df is the training csv
df = pd.read_csv('fake-news/train.csv')

#convert the 0 in the labels to real and the 1s to fake for easier readability
conversion_dict = {0: 'Real',1: 'Fake'}
df['label'] = df['label'].replace(conversion_dict)

#makes sure that the training data is relatively balanced
df.label.value_counts()

#trains the model to find the relationship between the text and the label of true or false given
x_train,x_test,y_train,y_test=train_test_split(df['text'], df['label'], test_size=0.8, random_state = 7, shuffle = True)
tfidf_vectorizer=TfidfVectorizer(stop_words='english',max_df = 0.75)

#converts pandas object into readble strings
vec_train = tfidf_vectorizer.fit_transform(x_train.values.astype('U'))
vec_test = tfidf_vectorizer.transform(x_test.values.astype('U'))

#passave aggressive classifier basically creates a hyperplane between true or false and then adjusts itself depending on the article and correct itself
pac=PassiveAggressiveClassifier(max_iter=50)
pac.fit(vec_train,y_train)

#run the model against the given train data that was originally used to make the PAC
y_pred = pac.predict(vec_test)
score=accuracy_score(y_test,y_pred)
print(f'PAC Accuracy: {round(score*100,2)}%')

#this is an elaboration of the previous (currently not printing thought). the values in the array goes as real true, fake true, fake fake, real fake
confusion_matrix(y_test,y_pred, labels=['Real','Fake'])

#gives kfold accuracy
x=tfidf_vectorizer.transform(df['text'].values.astype('U'))
scores = cross_val_score(pac,x,df['label'].values,cv = 5)
print(f'K Fold Accuracy: {round(scores.mean()*100,2)}%')

#reads in more data not related to the test data and sees how well the PAC does
df_true=pd.read_csv('True.csv')
df_true['label']='Real'
#df_true_rep=[df_true['text'][i].replace('WASHINGTON (Reuters) - ','').replace('LONDON (Reuters) - ','').replace('(Reuters) - ','') for i in range(len(df_true['text']))]
#df_true['text']=df_true_rep
df_fake=pd.read_csv('Fake.csv')
df_fake['label']='Fake'
df_final=pd.concat([df_true,df_fake])
df_final=df_final.drop(['subject','date'], axis=1)

def findlabel(newtext):
    vec_newtest=tfidf_vectorizer.transform([newtext])
    y_pred1=pac.predict(vec_newtest)
    return y_pred1[0]



#print(findlabel(extractText(url)))



#gives label 1 if it predicts true, 0 if it predicts false. get the 1s divided by the whole thing
print('')
print('Portion of predicting real articles real:')
print(sum([1 if findlabel((df_true['text'][i]))=='Real' else 0 for i in range(len(df_true['text']))])/df_true['text'].size)

#gives label 1 if it predicts false, 0 if it predicts true. get the 1s divided by the whole thing
print('')
print('Portion of predicting fake articles fake:')
print(sum([1 if findlabel((df_fake['text'][i]))=='Fake' else 0 for i in range(len(df_fake['text']))])/df_fake['text'].size)

# line for the end of the Fake News Classifier Model Stats module
print('----------------------------------------------------')





with open('keys.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

CONSUMER_KEY = content[0]
CONSUMER_SECRET = content[1]
ACCESS_KEY = content[2]
ACCESS_SECRET = content[3]



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
print('Bot Started')



#api.metions_timeline() gives a ResultSet object, which is basically a list. And each element is a Status object



while True:
    f = open('last_tweet_id.txt','r')
    last_tweet_id = f.readlines()[0]
    f.close()


    mentions = api.mentions_timeline(since_id = last_tweet_id)


    for mention in mentions:

        print('-------------------')
        print('')
        print('NEW TWEET: ' + mention.text)
        print('')

        text = mention.text
        text_id = mention.id
        username = '@' + str(mention.user.screen_name)
        url = ''
        # the replied variable is to see if the tweet qualifies to be replied to
        replied = False
        # is_already_reply is a boolean to check that if it's a reply that the bot already did. If this boolean didn't exist, that means that there would be an infinite loop of the bot keep on replying to itself
        is_already_reply = False

        if len(mention.entities['hashtags']) > 0:
            hashtag = mention.entities['hashtags'][0].lower()
            if hashtag == 'validityscanned':
                is_already_reply = True


        #this is to check if there's a link in the original tweet
        if len(mention.entities['urls']) > 0 and is_already_reply == False:
            
            url = mention.entities['urls'][0]['expanded_url']
            response = requests.get(url)
            sleep(1)
            url = response.url
            article_text = extractText(url)

            print('URL: ' + url)
            print('')

            print('Article Text Excerpt: ' + article_text[0:100])
            print('')


            replied = True
        else:
            print('URL: NONE')
            print('')
            print('Article Text Excerpt: ')
            print('')

        if replied == True:
            validity = findlabel(article_text)
            api.update_status('Article is deemed ' + str(validity) + ' #validityscanned \n \n Scanned by Jonathan Lin', text_id, auto_populate_reply_metadata=True)
            print('Replied to link. Determined the link is ' + validity)
            print('')

        if replied == False:
            api.update_status('Error, No Link Detected #validityscanned', text_id, auto_populate_reply_metadata=True)
            print('')
        


    if len(mentions) != 0:
        last_id = mentions[0].id_str
        f = open('last_tweet_id.txt','w')
        f.write(last_id)
        f.close()

    sleep(6)

