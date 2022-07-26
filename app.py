from flask import Flask, render_template, request, redirect
import distance
import location
import logging
import database
from admin.admin import admin


SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(admin, url_prefix='/admin')

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)
logging.basicConfig(
    level=logging.WARNING,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)
logging.basicConfig(
    level=logging.ERROR,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)
logging.basicConfig(
    level=logging.CRITICAL,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)

import sys
sh = logging.StreamHandler(sys.stdout)

logger = logging.getLogger()

logger.addHandler(sh)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    global _id
    if request.method == "POST":
        city = request.form['city']
        street = request.form['street']
        house = request.form['house']

        local = city + street + house
        try:
            coordinates = location.location(local)
            logger.info(coordinates)
            Lo1 = float(coordinates[0])
            La1 = float(coordinates[1])
        except:
            return "При вычислении координат ошибка"

        try:
            calculated = distance.create_lo_la(coordinates)
            logger.info(calculated)
        except:
            return "При вычислении расстояния ошибка"

        etr = (city, street, house, Lo1, La1, calculated)
        logger.info(etr)
        _id = database.receiver(city, street, house, Lo1, La1, calculated)
        return redirect('/calculated_distance/' + f"{_id}")
    else:
        return render_template("create-article.html")


@app.route('/calculated_distance')
def calculated_distance():
    computed = database.calculated()
    return render_template("calculated_distance.html", computed=computed)


@app.route('/calculated_distance/<int:id>')
def post_detail(id):
    post = database.calculated_id(id)
    logger.info(post)
    return render_template("calculated_distance.html", post=post)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = database.calculated()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    try:
        database.delete_calculated(id)
        return redirect('/posts')
    except:
        return "При удалении статьи возникли ошибки"


if __name__ == "__main__":
    app.run(debug=True)
