from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, validators
from wtforms.validators import DataRequired



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-rank.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)


class Movie(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(50), unique=True, nullable=False)
    year = db.Column("year", db.Integer, unique=False, nullable=False)
    description = db.Column("description", db.String(300), unique=False, nullable=False)
    rating = db.Column("rating", db.Float, unique=False, nullable=False)
    ranking = db.Column("ranking", db.Integer, unique=True, nullable=False)
    review = db.Column("review", db.String(300), unique=False, nullable=False)
    img = db.Column("img_url", db.String(300), nullable=False)


class RateForm(FlaskForm):
    new_rating = FloatField(label="Your rating out of 10", validators=[validators.DataRequired()])
    new_review = StringField(label="Your review", validators=[validators.DataRequired()])
    update = SubmitField(label="Update")


with app.app_context():
    SQLAlchemy.create_all(db)



# new_movie = Movie(
#     title="Phone Book",
#     year=2002,
#     description="bla bla bla bla ",
#     rating=6.9,
#     ranking=10,
#     review="he heh u hi",
#     img="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()

@app.route("/")
def home():
    movies = Movie.query.all()
    return render_template("index.html", films=movies)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    form = RateForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = form.new_rating
        movie.review = form.new_review
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
