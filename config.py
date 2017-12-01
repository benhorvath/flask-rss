TITLE = 'Flask-RSS'
DESCRIPTION = 'Automated article curration via RSS feeds'
SQLALCHEMY_DATABASE_URI = 'dialect+driver://username:password@host:port/database'
SQLALCHEMY_ECHO = False
SECRET_KEY = 'change this to a unique key for your app'
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
ARTICLES_PER_PAGE = 10
RSS_FEEDS = ['https://feeds.feedburner.com/techcrunch',
             'http://feeds.feedburner.com/simplyrecipes',
             'https://feeds.feedburner.com/boingboing/ibag']