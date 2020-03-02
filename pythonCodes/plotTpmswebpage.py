#thing to install
#pip install -U Flask

from flask import Flask

app = Flask(__name__)

@app.route("/")


def home():
    return render_template(“home.html”)

def main():
    print("##################################################################################################")
    home()
    app.run(debug=True)









if __name__ == '__main__':
    main()