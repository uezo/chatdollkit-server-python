from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from . import ConnectorBase
from ..models import ApiRequest, ApiResponse


class FastAPIConnector(ConnectorBase):
    # HTTP Request(FastAPI) to Request, Context and PreProcess flag
    async def parse_request(self, http_request):
        api_request = ApiRequest(**(await http_request.json()))
        return api_request.Request, api_request.Context, api_request.PreProcess

    # Request, Context and Response to HTTP Response
    def make_response(
            self, request, context, response=None, status_code=200):
        api_response = ApiResponse(
            Request=request, Context=context, Response=response
        )
        return JSONResponse(
            jsonable_encoder(api_response), status_code=status_code)

    # Request, Context and Error to HTTP Response
    def make_error_response(self, request, context, exception):
        error, status_code = self.handle_exception(exception)
        api_response = ApiResponse(
            Request=request, Context=context, Error=error
        )
        return JSONResponse(
            jsonable_encoder(api_response), status_code=status_code)

    # Configuration for quick start
    @classmethod
    def configure_app(cls, app, intent_extractor_class, dialog_classes,
                      prompter_class=None, debug=False):
        connector = cls(debug=debug)
        intent_extractor = intent_extractor_class(
            connector, debug=debug)
        dialogs = {
            k: v(connector, debug=debug)
            for k, v in dialog_classes.items()
        }
        prompter = prompter_class(
                connector, debug=debug
            ) if prompter_class else None

        @app.get(cls.ping_uri)
        async def get_ping():
            return "ok"

        @app.post(cls.intent_extractor_uri)
        async def extract_intent(http_request: Request):
            return await intent_extractor.execute_async(http_request)

        @app.post(cls.dialog_uri_base + "/{name}")
        async def process_dialog(name, http_request: Request):
            dialog = dialogs.get(name)
            if not dialog:
                raise HTTPException(status_code=404, detail="dialog not found")
            else:
                return await dialog.execute_async(http_request)

        if prompter:
            @app.post(cls.prompt_uri)
            async def get_prompt(http_request: Request):
                return await prompter.execute_async(http_request)
