from flask import render_template

def error(messsage):
    return render_template("error.html", error = message)    