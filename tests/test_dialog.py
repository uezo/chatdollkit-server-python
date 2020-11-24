import sys
import os
sys.path.append(os.pardir)
from chatdollkit import (
    RequestType,
    ApiRequest,
    ApiResponse,
    ApiException,
    ConnectorBase,
    PrompterBase,
    IntentExtractorBase,
    DialogProcessorBase,
)


class EchoPrompter(PrompterBase):
    def get_prompt(self, context, response):
        if context.Id == "handled_error":
            raise ApiException(400, "E0123", "Handled error pp")
        elif context.Id == "unhandled_error":
            raise Exception("Unhandled error pp")

        context.Topic.RequiredRequestType = RequestType.QRCode
        response.AnimatedVoiceRequest.StartIdlingOnEnd = False
        response.AnimatedVoiceRequest.AddVoice("prompt voice")


class EchoIntentExtractor(IntentExtractorBase):
    def extract_intent(self, request, context):
        if request.Text == "handled_error":
            raise ApiException(400, "E1234", "Handled error ie")
        elif request.Text == "unhandled_error":
            raise Exception("Unhandled error ie")

        request.Intent = "echo"


class EchoDialog(DialogProcessorBase):
    def pre_process(self, request, context, response):
        if request.Text == "handled_error":
            raise ApiException(400, "E2345", "Handled error preproc")
        elif request.Text == "unhandled_error":
            raise Exception("Unhandled error preproc")

        context.Data["key1"] = "val1"
        context.Data["key2"] = "val2"
        response.AnimatedVoiceRequest.AddVoice("pre_process: " + request.Text)

    def process(self, request, context, response):
        if request.Text == "handled_error":
            raise ApiException(400, "E3456", "Handled error proc")
        elif request.Text == "unhandled_error":
            raise Exception("Unhandled error proc")

        context.Data["key1"] = "val1_updated"
        context.Data["key3"] = "val3"
        response.AnimatedVoiceRequest.AddVoice("process: " + request.Text)


class LocalConnector(ConnectorBase):
    def parse_request(self, http_request):
        api_request = ApiRequest(**http_request)
        return api_request.Request, api_request.Context, api_request.PreProcess

    def make_response(self, request, context, response=None, status_code=200):
        api_response = ApiResponse(
            Request=request, Context=context, Response=response
        )
        return api_response, status_code

    def make_error_response(self, request, context, exception):
        error, status_code = self.handle_exception(exception)
        api_response = ApiResponse(
            Request=request, Context=context, Error=error
        )
        return api_response, status_code


def get_prompt_request_dict():
    return {
        "Context": {
            "Id": "fd9bbbb1-ae28-491b-87c1-9e08ebdf6c0c", "UserId": "user0123456789", "Timestamp": "2020-11-16T09:45:42.393658+00:00", "IsNew": True, "Topic": {"Name": None, "Status": None, "IsNew": True, "ContinueTopic": False, "Previous": None, "Priority": 0, "RequiredRequestType": 0}, "Data": {}},
    }


def get_intent_request_dict():
    return {
        "Request": {
            "Id": "983440e5-474f-4351-8d24-bb3dc14057bf", "Type": 0, "Timestamp": "2020-11-16T09:45:47.827355+00:00", "User": {"Id": "user0123456789", "DeviceId": None, "Name": None, "Nickname": None, "Data": {}}, "Text": "これはテストです", "Payloads": None, "Intent": None, "IntentPriority": 50, "Entities": {}, "Words": None, "IsAdhoc": False, "IsCanceled": False},
        "Context": {
            "Id": "fd9bbbb1-ae28-491b-87c1-9e08ebdf6c0c", "UserId": "user0123456789", "Timestamp": "2020-11-16T09:45:42.393658+00:00", "IsNew": True, "Topic": {"Name": None, "Status": None, "IsNew": True, "ContinueTopic": False, "Previous": None, "Priority": 0, "RequiredRequestType": 0}, "Data": {}},
    }


def get_pre_process_request_dict():
    return {
        "Request": {
            "Id": "983440e5-474f-4351-8d24-bb3dc14057bf", "Type": 0, "Timestamp": "2020-11-16T09:45:47.827355+00:00", "User": {"Id": "user0123456789", "DeviceId": None, "Name": None, "Nickname": None, "Data": {}}, "Text": "これはテストです", "Payloads": None, "Intent": None, "IntentPriority": 50, "Entities": {}, "Words": None, "IsAdhoc": False, "IsCanceled": False},
        "Context": {
            "Id": "fd9bbbb1-ae28-491b-87c1-9e08ebdf6c0c", "UserId": "user0123456789", "Timestamp": "2020-11-16T09:45:42.393658+00:00", "IsNew": True, "Topic": {"Name": None, "Status": None, "IsNew": True, "ContinueTopic": False, "Previous": None, "Priority": 0, "RequiredRequestType": 0}, "Data": {}},
        "PreProcess": True
    }


def get_process_request_dict():
    return {
        "Request": {
            "Id": "983440e5-474f-4351-8d24-bb3dc14057bf", "Type": 0, "Timestamp": "2020-11-16T09:45:47.827355+00:00", "User": {"Id": "user0123456789", "DeviceId": None, "Name": None, "Nickname": None, "Data": {}}, "Text": "これはテストです", "Payloads": None, "Intent": None, "IntentPriority": 50, "Entities": {}, "Words": None, "IsAdhoc": False, "IsCanceled": False},
        "Context": {
            "Id": "fd9bbbb1-ae28-491b-87c1-9e08ebdf6c0c", "UserId": "user0123456789", "Timestamp": "2020-11-16T09:45:42.393658+00:00", "IsNew": True, "Topic": {"Name": None, "Status": None, "IsNew": True, "ContinueTopic": False, "Previous": None, "Priority": 0, "RequiredRequestType": 0}, "Data": {"key1": "val1", "key2": "val2"}},
        "PreProcess": False
    }


connector = LocalConnector(debug=False)
connector_debug = LocalConnector(debug=True)


def test_get_prompt():
    prompter = EchoPrompter(connector_debug)
    api_response, status_code = \
        prompter.execute(get_prompt_request_dict())

    assert status_code == 200
    assert api_response.Context.Topic.RequiredRequestType == RequestType.QRCode
    assert api_response.Response.AnimatedVoiceRequest.StartIdlingOnEnd is False
    assert api_response.Response.AnimatedVoiceRequest.AnimatedVoices[0].Voices[0].Name == "prompt voice"


def test_get_prompt_handled_error():
    prompter = EchoPrompter(connector_debug)
    prompt_request = get_prompt_request_dict()
    prompt_request["Context"]["Id"] = "handled_error"
    api_response, status_code = \
        prompter.execute(prompt_request)

    assert status_code == 400
    assert api_response.Error.Code == "E0123"
    assert api_response.Error.Message == "Handled error pp"
    assert api_response.Error.Detail.startswith("Handled error pp")


def test_get_prompt_unhandled_error():
    prompter = EchoPrompter(connector_debug)
    prompt_request = get_prompt_request_dict()
    prompt_request["Context"]["Id"] = "unhandled_error"
    api_response, status_code = \
        prompter.execute(prompt_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail.startswith("Unhandled error pp")


def test_get_prompt_error_nodebug():
    prompter = EchoPrompter(connector)
    prompt_request = get_prompt_request_dict()
    prompt_request["Context"]["Id"] = "unhandled_error"
    api_response, status_code = \
        prompter.execute(prompt_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail is None


def test_extract_intent():
    intent_extractor = EchoIntentExtractor(connector_debug)
    api_response, status_code = \
        intent_extractor.execute(get_intent_request_dict())

    assert status_code == 200
    assert api_response.Request.Intent == "echo"


def test_extract_intent_handled_error():
    intent_extractor = EchoIntentExtractor(connector_debug)
    intent_request = get_intent_request_dict()
    intent_request["Request"]["Text"] = "handled_error"
    api_response, status_code = intent_extractor.execute(intent_request)

    assert status_code == 400
    assert api_response.Error.Code == "E1234"
    assert api_response.Error.Message == "Handled error ie"
    assert api_response.Error.Detail.startswith("Handled error ie")


def test_extract_intent_unhandled_error():
    intent_extractor = EchoIntentExtractor(connector_debug)
    intent_request = get_intent_request_dict()
    intent_request["Request"]["Text"] = "unhandled_error"
    api_response, status_code = intent_extractor.execute(intent_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail.startswith("Unhandled error ie")


def test_extract_intent_error_nodebug():
    intent_extractor = EchoIntentExtractor(connector)
    intent_request = get_intent_request_dict()
    intent_request["Request"]["Text"] = "unhandled_error"
    api_response, status_code = intent_extractor.execute(intent_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail is None


def test_pre_process():
    echo_dialog = EchoDialog(connector_debug)
    api_response, status_code = echo_dialog.execute(get_pre_process_request_dict())

    assert status_code == 200
    assert api_response.Response.AnimatedVoiceRequest.AnimatedVoices[0].Voices[0].Name == "pre_process: これはテストです"
    assert api_response.Context.Data["key1"] == "val1"
    assert api_response.Context.Data["key2"] == "val2"


def test_pre_process_handled_error():
    echo_dialog = EchoDialog(connector_debug)
    pre_process_request = get_pre_process_request_dict()
    pre_process_request["Request"]["Text"] = "handled_error"
    api_response, status_code = echo_dialog.execute(pre_process_request)

    assert status_code == 400
    assert api_response.Error.Code == "E2345"
    assert api_response.Error.Message == "Handled error preproc"
    assert api_response.Error.Detail.startswith("Handled error preproc")


def test_pre_process_unhandled_error():
    echo_dialog = EchoDialog(connector_debug)
    pre_process_request = get_pre_process_request_dict()
    pre_process_request["Request"]["Text"] = "unhandled_error"
    api_response, status_code = echo_dialog.execute(pre_process_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail.startswith("Unhandled error preproc")


def test_pre_process_error_nodebug():
    echo_dialog = EchoDialog(connector)
    pre_process_request = get_pre_process_request_dict()
    pre_process_request["Request"]["Text"] = "unhandled_error"
    api_response, status_code = echo_dialog.execute(pre_process_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail is None


def test_process():
    echo_dialog = EchoDialog(connector_debug)
    api_response, status_code = echo_dialog.execute(get_process_request_dict())

    assert status_code == 200
    assert api_response.Response.AnimatedVoiceRequest.AnimatedVoices[0].Voices[0].Name == "process: これはテストです"
    assert api_response.Context.Data["key1"] == "val1_updated"
    assert api_response.Context.Data["key2"] == "val2"
    assert api_response.Context.Data["key3"] == "val3"


def test_process_handled_error():
    echo_dialog = EchoDialog(connector_debug)
    process_request = get_process_request_dict()
    process_request["Request"]["Text"] = "handled_error"
    api_response, status_code = echo_dialog.execute(process_request)

    assert status_code == 400
    assert api_response.Error.Code == "E3456"
    assert api_response.Error.Message == "Handled error proc"
    assert api_response.Error.Detail.startswith("Handled error proc")


def test_process_unhandled_error():
    echo_dialog = EchoDialog(connector_debug)
    process_request = get_process_request_dict()
    process_request["Request"]["Text"] = "unhandled_error"
    api_response, status_code = echo_dialog.execute(process_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail.startswith("Unhandled error proc")


def test_process_error_nodebug():
    echo_dialog = EchoDialog(connector)
    process_request = get_process_request_dict()
    process_request["Request"]["Text"] = "unhandled_error"
    api_response, status_code = echo_dialog.execute(process_request)

    assert status_code == 500
    assert api_response.Error.Code == "E9999"
    assert api_response.Error.Message == "Error"
    assert api_response.Error.Detail is None
