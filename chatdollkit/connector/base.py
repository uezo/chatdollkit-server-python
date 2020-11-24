from abc import ABC, abstractmethod
import logging
import traceback
from ..models import ApiError, ApiException


class ConnectorBase(ABC):
    ping_uri = "/chatdollkit/ping"
    prompt_uri = "/chatdollkit/prompt"
    intent_extractor_uri = "/chatdollkit/intent"
    dialog_uri_base = "/chatdollkit/dialog"

    def __init__(self, logger=None, debug=False):
        self.logger = logger or logging.getLogger(__class__.__name__)
        self.debug = debug

    # HTTP Request to Request, Context and PreProcess flag
    @abstractmethod
    def parse_request(self, http_request):
        pass

    # Request, Context, Response and Error to HTTP Response
    @abstractmethod
    def make_response(self, request, context, response=None, status_code=200):
        pass

    @abstractmethod
    def make_error_response(self, request, context, exception):
        pass

    def handle_exception(self, exception):
        error_detail = f"{str(exception)}\n{traceback.format_exc()}"
        self.logger.error(error_detail)

        if isinstance(exception, ApiException):
            status_code = exception.status_code
            error_code = exception.error_code
            message = exception.message
        else:
            error_code = "E9999"
            status_code = 500
            message = "Error"

        return ApiError(
            Code=error_code,
            Message=message,
            Detail=error_detail if self.debug else None), status_code
