from flask import (
    make_response as flask_make_response,
    request as flask_request,
    abort
)
from . import ConnectorBase
from ..models import ApiRequest, ApiResponse


class FlaskConnector(ConnectorBase):
    # HTTP Request(Flask) to Request, Context and PreProcess flag
    def parse_request(self, http_request):
        api_request = ApiRequest(**http_request.json)
        return api_request.Request, api_request.Context, api_request.PreProcess

    # Request, Context and Response to HTTP Response
    def make_response(self, request, context, response=None, status_code=200):
        api_response = ApiResponse(
            Request=request, Context=context, Response=response
        )
        return flask_make_response(api_response.json(), status_code)

    # Request, Context and Error to HTTP Response
    def make_error_response(self, request, context, exception):
        error, status_code = self.handle_exception(exception)
        api_response = ApiResponse(
            Request=request, Context=context, Error=error
        )
        return flask_make_response(api_response.json(), status_code)

    # Configuration for quick start
    @classmethod
    def configure_app(cls, app, intent_extractor_class, dialog_classes,
                      prompter_class=None, debug=False):
        connector = cls(logger=app.logger, debug=debug)
        intent_extractor = intent_extractor_class(
            connector, logger=app.logger, debug=debug)
        dialogs = {
            k: v(connector, logger=app.logger, debug=debug)
            for k, v in dialog_classes.items()
        }
        prompter = prompter_class(
                connector, logger=app.logger, debug=debug
            ) if prompter_class else None

        @app.route(cls.ping_uri, methods=["GET"])
        def get_ping():
            return "ok"

        @app.route(cls.intent_extractor_uri, methods=["POST"])
        def extract_intent():
            return intent_extractor.execute(flask_request)

        @app.route(cls.dialog_uri_base + "/<name>", methods=["POST"])
        def process_dialog(name):
            dialog = dialogs.get(name)
            if not dialog:
                return abort(404)
            else:
                return dialog.execute(flask_request)

        if prompter:
            @app.route(cls.prompt_uri, methods=["POST"])
            def get_prompt():
                return prompter.execute(flask_request)
