import traceback
from flask import (
    Blueprint,
    make_response,
    request as flask_request,
    current_app
)
from chatdollkit.models import (
    ApiPromptRequest, ApiPromptResponse,
    ApiIntentRequest, ApiIntentResponse,
    ApiSkillRequest, ApiSkillResponse,
    SkillNotFoundException
)


bp = Blueprint("chatdollkit_server_api", __name__)


@bp.route("/ping", methods=["GET"])
def ping():
    return "ok"


@bp.route("/prompt", methods=["POST"])
def prompt():
    try:
        prompt_request = ApiPromptRequest(**flask_request.json)
        response = current_app.chatdoll_app.get_prompt(
            prompt_request.Request, prompt_request.State
        )
        prompt_response = ApiPromptResponse(
            Response=response, State=prompt_request.State
        )
        return make_response(prompt_response.json(), 200)

    except Exception as ex:
        current_app.logger.error(
            f"Error at prompt: {str(ex)}\n{traceback.format_exc()}")
        prompt_response = \
            ApiPromptResponse.from_exception(
                ex, current_app.chatdoll_app.debug)
        return make_response(prompt_response.json(), 500)


@bp.route("/intent", methods=["POST"])
def intent():
    try:
        intent_request = ApiIntentRequest(**flask_request.json)
        intent_extraction_result = current_app.chatdoll_app.extract_intent(
            intent_request.Request, intent_request.State
        )
        intent_response = ApiIntentResponse(
            IntentExtractionResult=intent_extraction_result
        )
        return make_response(intent_response.json(), 200)

    except Exception as ex:
        current_app.logger.error(
            f"Error at intent: {str(ex)}\n{traceback.format_exc()}")
        intent_response = \
            ApiIntentResponse.from_exception(
                ex, current_app.chatdoll_app.debug)
        return make_response(intent_response.json(), 500)


@bp.route("/skill/<skill_name>", methods=["POST"])
def skill(skill_name):
    try:
        skill_request = ApiSkillRequest(**flask_request.json)
        response = current_app.chatdoll_app.process_skill(
            skill_name, skill_request.Request, skill_request.State,
            skill_request.PreProcess
        )
        skill_response = ApiSkillResponse(
            Response=response, State=skill_request.State,
            User=skill_request.Request.User
        )
        return make_response(skill_response.json(), 200)

    except Exception as ex:
        current_app.logger.error(
            f"Error at processing skill: {str(ex)}\n{traceback.format_exc()}")
        skill_response = \
            ApiSkillResponse.from_exception(
                ex, current_app.chatdoll_app.debug)
        status_code = 404 if isinstance(ex, SkillNotFoundException) else 500
        return make_response(skill_response.json(), status_code)
