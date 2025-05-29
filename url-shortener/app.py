from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///short_urls.db'
db = SQLAlchemy(app)

# Database model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    short_url = db.Column(db.String(10), unique=True)

# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=6))
        if not URL.query.filter_by(short_url=short_url).first():
            return short_url

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        original_url = request.form['original_url']
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url:
            short_url = existing_url.short_url
        else:
            short_url = generate_short_url()
            new_url = URL(original_url=original_url, short_url=short_url)
            db.session.add(new_url)
            db.session.commit()
    return render_template('index.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
