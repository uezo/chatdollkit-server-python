import traceback
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from chatdollkit.models import (
    ApiPromptRequest, ApiPromptResponse,
    ApiSkillsResponse,
    ApiIntentRequest, ApiIntentResponse,
    ApiSkillRequest, ApiSkillResponse,
    SkillNotFoundException
)

router = APIRouter()


@router.get("/ping")
async def get_ping():
    return "ok"


@router.post("/prompt")
async def prompt(fastapi_request: Request):
    try:
        prompt_request = ApiPromptRequest(**(await fastapi_request.json()))
        response = await fastapi_request.app.chatdoll_app.get_prompt_async(
            prompt_request.Request, prompt_request.State
        )
        prompt_response = ApiPromptResponse(
            Response=response, State=prompt_request.State
        )
        return JSONResponse(
            jsonable_encoder(prompt_response), status_code=200)

    except Exception as ex:
        fastapi_request.app.chatdoll_app.logger.error(
            f"Error at prompt: {str(ex)}\n{traceback.format_exc()}")
        prompt_response = \
            ApiPromptResponse.from_exception(
                ex, fastapi_request.app.chatdoll_app.debug)
        return JSONResponse(
            jsonable_encoder(prompt_response), status_code=500)


@router.post("/intent")
async def intent(fastapi_request: Request):
    try:
        intent_request = ApiIntentRequest(**(await fastapi_request.json()))
        intent_extraction_result = \
            await fastapi_request.app.chatdoll_app.extract_intent_async(
                intent_request.Request, intent_request.State
            )
        intent_response = ApiIntentResponse(
            IntentExtractionResult=intent_extraction_result
        )
        return JSONResponse(
            jsonable_encoder(intent_response), status_code=200)

    except Exception as ex:
        fastapi_request.app.chatdoll_app.logger.error(
            f"Error at intent: {str(ex)}\n{traceback.format_exc()}")
        intent_response = \
            ApiIntentResponse.from_exception(
                ex, fastapi_request.app.chatdoll_app.debug)
        return JSONResponse(
            jsonable_encoder(intent_response), status_code=500)


@router.get("/skills")
async def skills(fastapi_request: Request):
    try:
        skills_response = ApiSkillsResponse(
            SkillNames=[
                s.topic for s in fastapi_request.app.chatdoll_app.skills
            ]
        )
        return JSONResponse(
            jsonable_encoder(skills_response), status_code=200)

    except Exception as ex:
        fastapi_request.app.chatdoll_app.logger.error(
            f"Error at skills: {str(ex)}\n{traceback.format_exc()}")
        skills_response = \
            ApiSkillsResponse.from_exception(
                ex, fastapi_request.app.chatdoll_app.debug)
        return JSONResponse(
            jsonable_encoder(skills_response), status_code=500)


@router.post("/skills/{skill_name}")
async def skill(fastapi_request: Request, skill_name: str):
    try:
        skill_request = ApiSkillRequest(**(await fastapi_request.json()))
        response = await fastapi_request.app.chatdoll_app.process_skill_async(
            skill_name, skill_request.Request, skill_request.State,
            skill_request.PreProcess
        )
        skill_response = ApiSkillResponse(
            Response=response, State=skill_request.State,
            User=skill_request.Request.User
        )
        return JSONResponse(
            jsonable_encoder(skill_response), status_code=200)

    except Exception as ex:
        fastapi_request.app.chatdoll_app.logger.error(
            f"Error at processing skill: {str(ex)}\n{traceback.format_exc()}")
        skill_response = \
            ApiSkillResponse.from_exception(
                ex, fastapi_request.app.chatdoll_app.debug)
        status_code = 404 if isinstance(ex, SkillNotFoundException) else 500
        return JSONResponse(
            jsonable_encoder(skill_response), status_code=status_code)
