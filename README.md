# Flask-RSS

Ever wanted to share a curated list of RSS feeds with your friends? Flask-RSS will do just that! It is a very simple app making use of Flask, SQLAlchemy, and the FeedParser package.

It is designed to work with Heroku. You can get a free account with a free database, adjust your configuraton in config.py, commit to your Heroku app, and you're all set in less than five minutes!

## Steps

1. Clone this repo to your computer
2. Install requirements:
  ```bash
    pip install -r requirements.txt
    ```
3. Create an account with Heroku. You'll need at least a hobby (free) account, and set up a database. You'll probably have the best luck with Postgres.
4. Go to your new database's settings, and look for its credentials. Find the connection string.
5. Edit config.py to paste the connection string as the value for ```SQLALCHEMY_DATABASE_URI```.
6. While you're in config:
  * Change the ```TITLE``` and ```DESCRIPTION``` to better represent your feeds
  * Make the ```SECRET KEY``` something unique to your app
  * Finally, use ```RSS_FEEDS``` to store the feeds you want to collect and update.

You're all done! Run ```python app.py``` and visit your app locally (usually host is 127.0.0.1 on port 8080).