# from flask import Flask
# app = Flask(__name__, static_folder='.', static_url_path='')
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')
# @app.route('/hello/<name>')
# def hello(name):
#     return name

# app.run(port=8000, debug=True)

from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', message="花子さん")

if __name__ == "__main__":
    app.run(port=8000, debug=True)