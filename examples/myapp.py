from chatdollkit.app import AppBase
from chatdollkit.models import (
    Request, Response, State, IntentExtractionResult, Intent
)
from .skills.echo import EchoSkill


class MyApp(AppBase):
    skills = [EchoSkill]

    def get_prompt(self, request: Request, state: State) -> Response:
        resp = Response(Id="_" if request is None else request.Id)
        resp.AddVoiceTTS("サーバーからのプロンプトです。何か喋ってください。")
        return resp

    async def get_prompt_async(self, request: Request, state: State) -> Response:
        resp = Response(Id="_" if request is None else request.Id)
        resp.AddVoiceTTS("非同期サーバーからのプロンプトです。何か喋ってください。")
        return resp

    def extract_intent(self, request: Request, state: State) -> IntentExtractionResult:
        return IntentExtractionResult(Intent=Intent(Name=EchoSkill.topic))

    async def extract_intent_async(self, request: Request, state: State) -> IntentExtractionResult:
        return IntentExtractionResult(Intent=Intent(Name=EchoSkill.topic))
