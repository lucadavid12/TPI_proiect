from flask import Flask, render_template
from flask import redirect, url_for
from utils.init import get_db_connection

from pacienti import pacient_bp
from programare import programare_bp
from doctori import doctor_bp

app = Flask(__name__)
db = get_db_connection()
app.register_blueprint(pacient_bp, url_prefix="/pacienti")
app.register_blueprint(doctor_bp, url_prefix="/doctori")
app.register_blueprint(programare_bp, url_prefix="/programare")

@app.route("/")
def index():
    return redirect(url_for("pacienti.pacienti"))

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()

# @app.route('/')
# def hello():
#     return render_template('base.html')


