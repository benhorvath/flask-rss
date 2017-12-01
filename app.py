
import os
import sys
import time

import feedparser
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

if (sys.version_info < (3, 0)):
    reload(sys)
    sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# RSS article data model
class Article(db.Model):

    __tablename__ = 'articles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String, primary_key=True)
    published = db.Column(db.Date)
    updated = db.Column(db.Date)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    summary = db.Column(db.String(1028))
    link = db.Column(db.String(1028))
    rss = db.Column(db.String(1028))

    def __repr__(self):
        return '<Article ID: %s>' % self.id

# RSS collection and save to db
class RSSFeedCollection(object):

    def __init__(self, feed_urls):
        self.feeds = feed_urls
        self.articles = []

    def update_feeds(self):
        for feed in self.feeds:
            parsed_feed = feedparser.parse(feed)
            for story in parsed_feed['entries']:
                row = {'id': str(story['id']),
                       'published': self._convert_dt(story['published_parsed']),
                       'updated': self._convert_dt(story['updated_parsed']),
                       'title': str(story['title']),
                       'author': str(story['author']),
                       'summary': str(story['summary']),
                       'link': str(story['link']),
                       'rss': str(feed)}
                self.articles.append(row)

    def insert_articles(self, db):
        existing_ids = [a.id for a in Article.query.all()]
        for article in self.articles:
            if article['id'] not in existing_ids:
                x = Article(id=article['id'],
                             published=article['published'],
                             updated=article['updated'],
                             title=article['title'],
                             author=article['author'],
                             summary=article['summary'],
                             link=article['link'],
                             rss=article['rss'])
                try:
                    db.session.rollback()
                    db.session.add(x)
                except sqlalchemy.exc.IntegrityError:  # row already exists
                    pass
                except Exception as e:
                    raise(e)
        db.session.commit()

    def _convert_dt(self, dt):
        return str(time.strftime('%Y-%m-%d', dt))


@app.route('/')
@app.route('/<int:page>', methods=['GET'])
def show_all(page=1):

    per_page = app.config['ARTICLES_PER_PAGE']
    title = app.config['TITLE']
    description = app.config['DESCRIPTION']

    if page == 1:
        feed_urls = app.config['RSS_FEEDS']
        feeds = RSSFeedCollection(feed_urls)
        feeds.update_feeds()
        feeds.insert_articles(db)

    return render_template('show_all.html',
                            title=app.config['TITLE'],
                            description = app.config['DESCRIPTION'],
                            articles=Article.query.order_by(Article.updated.desc()).paginate(page, per_page, error_out=False))


if __name__ == '__main__':

    app.run()