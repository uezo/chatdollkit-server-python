from fastapi import FastAPI
from chatdollkit.connector.fastapiconnector import FastAPIConnector
from echo import Prompter, IntentExtractor, EchoDialog

# create app
app = FastAPI()

# configure app
dialog_classes = {
    "echo": EchoDialog
}
FastAPIConnector.configure_app(
    app, IntentExtractor, dialog_classes, Prompter, debug=True)

# to run,
# $ uvicorn fastapiapp:app --port 12345 --reload
