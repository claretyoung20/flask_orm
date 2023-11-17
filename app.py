from flask import Flask
from routes.user_api import user_app
from routes.post_api import post_app
from routes.comment_api import comment_app
from utilities import db
import os

app = Flask(__name__)

# Import and register blueprints
app.register_blueprint(post_app, url_prefix='')
app.register_blueprint(comment_app, url_prefix='')
app.register_blueprint(user_app, url_prefix='')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI2']
db.init_app(app)


# Create tables in the database
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Hello, this is the home page!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(5300), debug=True)
