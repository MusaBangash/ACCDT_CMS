
from flask import Flask,render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy


#My App

app= Flask(__name__)
Scss(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashbord")
def dashboard():
    return render_template("dashboard.html")




if __name__ == "__main__":
    app.run(debug=True)


