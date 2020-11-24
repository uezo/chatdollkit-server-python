# ChatdollKit Server SDK for Python

SDK to create backend APIs for ChatdollKit. See also 👉 [ChatdollKit](https://github.com/uezo/ChatdollKit)

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

Run example API server that just echo what user says.

```bash
$ python flaskapp.py
```

On Unity, attach `HttpDialogRouter` and `HttpPrompter` to your 3D model and configure like below:

- Intent Extractor Uri: `http://localhost:12345/chatdollkit/intent`
- Dialog Processor Uri Base: `http://localhost:12345/chatdollkit/dialog`
- Prompter Uri: `http://localhost:12345/chatdollkit/prompter`
- Ping Uri: `http://localhost:12345/chatdollkit/ping`

NOTE: Text-to-Speech service is required

Run your Chatdoll app and start conversation. Your 3D model will echo what you say.


# Create your own dialog

Create classes that extend `PrompterBase`, `IntentExtractorBase`, and `DialogProcessorBase` and override their methods.

```python
class MyPrompter(PrompterBase):
    def get_prompt(self, context, response):
        response.AddVoiceTTS("May I help you?")

class MyIntentExtractor(IntentExtractorBase):
    def extract_intent(self, request, context):
        # define conditions to decide intent
        if ("weather" in request.Text):
            request.Intent = "weather"
        elif ("translation" in request.Text):
            request.Intent = "translation"
        else:
            request.Intent = "chat"
            request.IntentPriority = Priority.Low

class WeatherDialog(DialogProcessorBase):
    def process(self, request, context, response):
        weather = get_weather() # getting weather
        response.AddVoiceTTS(
            f"It's {weather} today.")
```

If you use FastAPI or some application frameworks that support async, override `get_prompt_async`, `extract_intent_async` and `process_async` instead.

After that configure app with these classes.

```python
dialog_classes = {
    "weather": WeatherDialog,
    "translation": TranslationDialog,
    "chat": ChatDialog
}
FlaskConnector.configure_app(
    app, MyIntentExtractor, dialog_classes, MyPrompter, debug=True)
```

# Use other application framework

To use application framework other than Flask and FastAPI, create and use connector class that extends `ConnectorBase` and override these methods:

- `parse_request` : convert HTTP request object to internal api objects
- `make_response`: convert internal api objects to HTTP response
- `make_error_response`: convert internal api objects to HTTP response with error info
