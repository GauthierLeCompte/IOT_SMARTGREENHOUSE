from flask import Flask, jsonify
from flask_cors import CORS
import uuid

# Create app from flask
app = Flask(__name__)

# To update app constantly
app.config.from_object(__name__)

CORS(app, resources={r"/*": {'origins': '*'}})

@app.route('/', methods=['GET'])
def greetings():
    return "Hello w"

@app.route('/homepage', methods=['GET'])
def homepage():
    return ("YEEEW")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Front end
# - npm install -g @vue/cli
# - npm install --save-dev eslint eslint-plugin-vue