import feedparser
import pandas as pd
import os


URL_RSS = "https://publisher.assetstore.unity3d.com/feed/justin-garza/Oaisfgakr5kZRuF6p8ates5Hj3A/activity.rss"
DIR = os.path.dirname(os.path.realpath(__file__))

def get_RSS() -> list:
    global URL_RSS
    result = []
    feed = feedparser.parse(URL_RSS)
    feed_entries = feed.entries
    for entry in feed.entries:

        article_title = entry.title
        article_link = entry.link
        article_published_at = entry.published 
        article_published_at_parsed = entry.published_parsed 
        content = entry.summary

        # print ("{}[{}]".format(article_title, article_link))
        # print ("Published at {}".format(article_published_at))
        # print("Content {}".format(content))

        result.append(
            {
                'article_title': article_title,
                'article_link': article_link,
                'content': content,
                'published_datetime': article_published_at
            }
        )
    return result

def send_email(to_email:str,from_email:str,message:str):
    from email.message import EmailMessage
    import ssl
    import smtplib

    import Config
    data = Config.Config().data

    em = EmailMessage()
    em['From'] = from_email
    em['To'] = to_email
    em['Subject'] = 'Unity Asset Store Review (RSS)'
    body = message
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(data['email'],data['password'])
        smtp.sendmail(
            em['From'], em['To'], em.as_string()
            )
        
def main():
    global DIR, URL_RSS
    data_path = os.path.join(DIR,'data.csv')
    data = pd.DataFrame([])
    try:
        data = pd.read_csv(data_path)
    except:
        pass
    ndata = pd.DataFrame(get_RSS())

    dfdiff = pd.concat([data,ndata]).drop_duplicates(keep=False)

    # print(dfdiff)
    # print(len(dfdiff))

    if len(dfdiff) > 0 :
        ndata.to_csv(data_path,index=False)

        message = URL_RSS + '\n\n'
        for r in ndata.to_records()[0:10]:
            for i in r:
                message += str(i) + '\n'
            message += '\n\n'
        print(message)

        send_email(
                to_email='jgarza9788@gmail.com',
                from_email='jgarza9788@gmail.com',
                message=message
                )

if __name__ == "__main__":
    main()

