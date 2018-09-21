from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def main():
    app.run(port=6666, host="0.0.0.0")

if __name__ == '__main__':
    main()