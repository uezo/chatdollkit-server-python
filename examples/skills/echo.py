from chatdollkit.app import SkillBase
from chatdollkit.models import (
    Request, Response, State
)


class EchoSkill(SkillBase):
    topic = "echo"

    def pre_process(self, request: Request, state: State) -> Response:
        return Response(Id=request.Id)

    async def pre_process_async(self, request: Request, state: State) -> Response:
        return await super().pre_process_async(request, state)

    def process(self, request: Request, state: State) -> Response:
        resp = Response(Id=request.Id)
        resp.AddVoiceTTS(request.Text)
        return resp

    async def process_async(self, request: Request, state: State) -> Response:
        resp = Response(Id=request.Id)
        resp.AddVoiceTTS(request.Text)
        return resp
