import logging
from chatdollkit.models import (
    Request, Response, State, IntentExtractionResult,
    SkillNotFoundException
)


class SkillBase:
    topic = None

    def __init__(self, logger: logging.Logger = None, debug: bool = False):
        assert self.topic is not None
        self.logger = logger
        self.debug = debug

    def pre_process(self, request: Request, state: State) -> Response:
        return Response(Id=request.Id)

    async def pre_process_async(self, request: Request, state: State) -> Response:
        return Response(Id=request.Id)

    def process(self, request: Request, state: State) -> Response:
        return Response(Id=request.Id)

    async def process_async(self, request: Request, state: State) -> Response:
        return Response(Id=request.Id)


class AppBase:
    skills = []

    def __init__(self, logger: logging.Logger = None, debug: bool = False):
        self.logger = logger or logging.getLogger(__class__.__name__)
        self.debug = debug
        self.__skills = {s.topic: s for s in self.skills}
        if len(self.__skills) == 0:
            self.logger.warning("No skills has been registered yet.")

    def get_skill(self, skill_name: str) -> SkillBase:
        skill_class = self.__skills.get(skill_name)
        if not skill_class:
            raise SkillNotFoundException(
                message=f"Skill '{skill_name}' not found"
            )

        if isinstance(skill_class, SkillBase):
            skill = skill_class
            skill.logger = skill.logger or self.logger
            skill.debug = self.debug
        else:
            skill = skill_class(self.logger, self.debug)

        return skill

    def get_prompt(self, request: Request, state: State) -> Response:
        pass

    async def get_prompt_async(self, request: Request, state: State) -> Response:
        pass

    def extract_intent(self, request: Request, state: State) -> IntentExtractionResult:
        pass

    async def extract_intent_async(self, request: Request, state: State) -> IntentExtractionResult:
        pass

    def process_skill(self, skill_name: str, request: Request, state: State, pre_process: bool) -> Response:
        skill = self.get_skill(skill_name)

        if pre_process:
            return skill.pre_process(request, state)
        else:
            return skill.process(request, state)

    async def process_skill_async(self, skill_name: str, request: Request, state: State, pre_process: bool) -> Response:
        skill = self.get_skill(skill_name)

        if pre_process:
            return await skill.pre_process_async(request, state)
        else:
            return await skill.process_async(request, state)
