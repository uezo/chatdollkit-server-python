from chatdollkit import (
    PrompterBase,
    IntentExtractorBase,
    DialogProcessorBase
)


class Prompter(PrompterBase):
    def get_prompt(self, context, response):
        response.AddVoiceTTS("こんにちは。何か喋ってください。")

    async def get_prompt_async(self, context, response):
        response.AddVoiceTTS("こんにちは。何か喋ってください。これは非同期処理です。")


class IntentExtractor(IntentExtractorBase):
    def extract_intent(self, request, context):
        request.Intent = "echo"

    async def extract_intent_async(self, request, context):
        request.Intent = "echo"


class EchoDialog(DialogProcessorBase):
    def process(self, request, context, response):
        response.AddVoiceTTS(
            f"あなたが喋った内容は、{request.Text}、です。")

    async def process_async(self, request, context, response):
        response.AddVoiceTTS(
            f"あなたが喋った内容は、{request.Text}、です。これは非同期処理です。")
