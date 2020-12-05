import logging
from .models import Response


class PrompterBase:
    def __init__(self, connector, logger=None, debug=False):
        self.connector = connector
        self.logger = logger or logging.getLogger(__class__.__name__)
        self.debug = debug

    def execute(self, http_request):
        request, context, _ = \
            self.connector.parse_request(http_request)
        response = Response(Id=context.Id)

        try:
            self.get_prompt(request, context, response)
            return self.connector.make_response(request, context, response)

        except Exception as ex:
            return self.connector.make_error_response(request, context, ex)

    async def execute_async(self, http_request):
        request, context, _ = \
            await self.connector.parse_request(http_request)
        response = Response(Id=context.Id)

        try:
            await self.get_prompt_async(context, response)
            return self.connector.make_response(request, context, response)

        except Exception as ex:
            return self.connector.make_error_response(request, context, ex)

    def get_prompt(self, request, context):
        pass

    async def get_prompt_async(self, request, context):
        self.logger.warning("get_prompt_async() is executed synchronously")
        self.get_prompt(request, context)


class IntentExtractorBase:
    def __init__(self, connector, logger=None, debug=False):
        self.connector = connector
        self.logger = logger or logging.getLogger(__class__.__name__)
        self.debug = debug

    def execute(self, http_request):
        request, context, _ = self.connector.parse_request(http_request)

        try:
            self.extract_intent(request, context)
            return self.connector.make_response(request, context)

        except Exception as ex:
            return self.connector.make_error_response(request, context, ex)

    async def execute_async(self, http_request):
        request, context, _ = await self.connector.parse_request(http_request)

        try:
            await self.extract_intent_async(request, context)
            return self.connector.make_response(request, context)

        except Exception as ex:
            return self.connector.make_error_response(request, context, ex)

    def extract_intent(self, request, context):
        pass

    async def extract_intent_async(self, request, context):
        self.logger.warning("extract_intent_async() is executed synchronously")
        self.extract_intent(request, context)


class DialogProcessorBase:
    def __init__(self, connector, logger=None, debug=False):
        self.connector = connector
        self.logger = logger or logging.getLogger(__class__.__name__)
        self.debug = debug

    def execute(self, http_request):
        request, context, is_preprocess = \
            self.connector.parse_request(http_request)
        response = Response(Id=request.Id)

        try:
            if is_preprocess:
                self.pre_process(request, context, response)
            else:
                self.process(request, context, response)
            return self.connector.make_response(request, context, response)
        except Exception as ex:
            return self.connector.make_error_response(request, context, ex)

    async def execute_async(self, http_request):
        request, context, is_preprocess = \
            await self.connector.parse_request(http_request)
        response = Response(Id=request.Id)

        try:
            if is_preprocess:
                await self.pre_process_async(request, context, response)
            else:
                await self.process_async(request, context, response)
            return self.connector.make_response(request, context, response)
        except Exception as ex:
            return self.connector.make_error_response(request, context, ex)

    def pre_process(self, request, context, response):
        pass

    def process(self, request, context, response):
        pass

    async def pre_process_async(self, request, context, response):
        self.logger.warning("pre_process_async() is executed synchronously")
        self.pre_process(request, context, response)

    async def process_async(self, request, context, response):
        self.logger.warning("process_async() is executed synchronously")
        self.process(request, context, response)
