from GoogleNews import GoogleNews


def run_google_news():
    googlenews = GoogleNews(lang='en', region='US', period='30d', encode='utf-8')
    print(googlenews.get_news('APPLE'))
