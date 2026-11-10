from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/google155e5a17fdae6bf2.html')
def google_verification():
    return render_template('google155e5a17fdae6bf2.html')

if __name__ == '__main__':
    app.run(debug=True)