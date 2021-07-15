# ChatdollKit Server SDK for Python

SDK to create remote skill server for ChatdollKit. See also 👉 [ChatdollKit](https://github.com/uezo/ChatdollKit)

[🇯🇵日本語のREADMEはこちら](https://github.com/uezo/chatdollkit-dialog-python/blob/master/README.ja.md)

# Install

```bash
$ pip install chatdollkit
```

Also install application framework you like. We support [Flask](https://flask.palletsprojects.com/) and [FastAPI](https://fastapi.tiangolo.com/).

```bash
$ pip install flask
```

Or

```bash
$ pip install fastapi uvicorn
```


# Quick start

## Server side

Run example API server that just echo what user says.

```bash
$ python run_flask.py
```

Or

```bash
$ uvicorn run_fastapi:app --port 12345 --reload
```

## Client side

See [ChatdollKit Documentation > Setup Skill client (ChatdollKit device)](https://github.com/uezo/ChatdollKit/blob/master/manual.md#setup-skill-client-chatdollkit-device) to use `Examples/SkillServer`.

If you want to run skill server on host other than localhost configure URLs on the inspector of `HttpSkillRouter` and `HttpPrompter`.

After setting up both server and client, run your Chatdoll app and start conversation. Your 3D model will echo what you say.


# Create your own Skill Server

Basically Skill(s), Server application and Entrypoint are required to create your Skill Server as following chapters.

First of all, make `allinone.py` and import required libraries.

```python
from flask import Flask
from chatdollkit.app import SkillBase, AppBase
from chatdollkit.models import (
    Request, Response, State, IntentExtractionResult, Intent
)
from chatdollkit.controllers.flask_controller import bp as api_bp
```

## 1. Skill

Make `EchoSkill` class that extends `SkillBase` and implement `process` methods to return response that includes a Text-to-Speech voice request.

```python
class EchoSkill(SkillBase):
    topic = "echo"

    def process(self, request: Request, state: State) -> Response:
        # Just echo
        resp = Response(Id=request.Id)
        resp.AddVoiceTTS(request.Text)
        return resp
```

## 2. Server application

Make `MyApp` that extends `AppBase` and implement `get_prompt` methods that requires voice input to user and `extract_intent` to route to `EchoSkill`.

```python
class MyApp(AppBase):
    # Register skill(s)
    skills = [EchoSkill]

    def get_prompt(self, request: Request, state: State) -> Response:
        # Return prompt message
        resp = Response(Id="_" if request is None else request.Id)
        resp.AddVoiceTTS("This prompt is from server. Please say something.")
        return resp

    def extract_intent(self, request: Request, state: State) -> IntentExtractionResult:
        # Always extract Echo intent
        return IntentExtractionResult(Intent=Intent(Name=EchoSkill.topic))
```

## 3. Application entry point

Lastly, Add the instance of `MyApp` to Flask application and register API controller blueprint to app.

```python
# Create Flask app
app = Flask(__name__)
# Create ChatdollKit server app and set it to Flask application
app.chatdoll_app = MyApp(app.logger, True)
# Register API controller
app.register_blueprint(api_bp)

if __name__ == "__main__":
    # Start API
    app.run(port="12345", debug=True)
```

See the example if you want to create FastAPI-based skill server.


# Use other application framework

To use application framework other than Flask and FastAPI, create controller that handles http request from ChatdollKit client by your self. You can reuse Skill, Server application and models. See `chatdollkit.controllers.flask_controller.py` or `fastapi_controller.py`.
