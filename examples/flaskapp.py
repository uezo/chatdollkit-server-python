from flask import Flask
from chatdollkit.connector.flaskconnector import FlaskConnector
from echo import Prompter, IntentExtractor, EchoDialog

# create app
app = Flask(__name__)

# configure app
dialog_classes = {
    "echo": EchoDialog
}
FlaskConnector.configure_app(
    app, IntentExtractor, dialog_classes, Prompter, debug=True)

if __name__ == "__main__":
    # run server
    app.run("0.0.0.0", port=12345, debug=True)
