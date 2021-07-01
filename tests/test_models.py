import sys
import os
sys.path.append(os.pardir)
from uuid import uuid4
from chatdollkit.models import (
    AnimatedVoiceRequest,
    ChatdollKitException,
    Response,
    TTSConfiguration,
    VoiceSource,
    ApiResponseBase
)


def test_add_voice():
    req = AnimatedVoiceRequest()

    req.AddVoice("voice_01")
    req.AddVoice("voice_02", PreGap=1.0, PostGap=2.0, AsNewFrame=True)

    assert req.AnimatedVoices[0].Voices[0].Name == "voice_01"
    assert req.AnimatedVoices[0].Voices[0].PreGap == 0.0
    assert req.AnimatedVoices[0].Voices[0].PostGap == 0.0
    assert req.AnimatedVoices[0].Voices[0].Text is None
    assert req.AnimatedVoices[0].Voices[0].Url is None
    assert req.AnimatedVoices[0].Voices[0].TTSConfig is None
    assert req.AnimatedVoices[0].Voices[0].Source == 0
    assert req.AnimatedVoices[0].Voices[0].UseCache is False

    assert req.AnimatedVoices[1].Voices[0].Name == "voice_02"
    assert req.AnimatedVoices[1].Voices[0].PreGap == 1.0
    assert req.AnimatedVoices[1].Voices[0].PostGap == 2.0
    assert req.AnimatedVoices[1].Voices[0].Text is None
    assert req.AnimatedVoices[1].Voices[0].Url is None
    assert req.AnimatedVoices[1].Voices[0].TTSConfig is None
    assert req.AnimatedVoices[1].Voices[0].Source == 0
    assert req.AnimatedVoices[1].Voices[0].UseCache is False


def test_add_voice_web():
    req = AnimatedVoiceRequest()

    req.AddVoiceWeb("https://voice_01")
    req.AddVoiceWeb("https://voice_02", PreGap=1.0, PostGap=2.0, Name="voice_02", UseCache=False, AsNewFrame=True)

    assert req.AnimatedVoices[0].Voices[0].Name == ""
    assert req.AnimatedVoices[0].Voices[0].PreGap == 0.0
    assert req.AnimatedVoices[0].Voices[0].PostGap == 0.0
    assert req.AnimatedVoices[0].Voices[0].Text is None
    assert req.AnimatedVoices[0].Voices[0].Url == "https://voice_01"
    assert req.AnimatedVoices[0].Voices[0].TTSConfig is None
    assert req.AnimatedVoices[0].Voices[0].Source == 1
    assert req.AnimatedVoices[0].Voices[0].UseCache is True

    assert req.AnimatedVoices[1].Voices[0].Name == "voice_02"
    assert req.AnimatedVoices[1].Voices[0].PreGap == 1.0
    assert req.AnimatedVoices[1].Voices[0].PostGap == 2.0
    assert req.AnimatedVoices[1].Voices[0].Text is None
    assert req.AnimatedVoices[1].Voices[0].Url == "https://voice_02"
    assert req.AnimatedVoices[1].Voices[0].TTSConfig is None
    assert req.AnimatedVoices[1].Voices[0].Source == 1
    assert req.AnimatedVoices[1].Voices[0].UseCache is False


def test_add_voice_tts():
    req = AnimatedVoiceRequest()

    req.AddVoiceTTS("テスト01")
    tts_config = TTSConfiguration(Name="AwesomeTTS", Params={"param01": "value01", "param02": "value02"})
    req.AddVoiceTTS("テスト02", PreGap=1.0, PostGap=2.0, Name="voice_02", TTSConfig=tts_config, UseCache=False, AsNewFrame=True)
    assert req.AnimatedVoices[0].Voices[0].Name == ""
    assert req.AnimatedVoices[0].Voices[0].PreGap == 0.0
    assert req.AnimatedVoices[0].Voices[0].PostGap == 0.0
    assert req.AnimatedVoices[0].Voices[0].Text == "テスト01"
    assert req.AnimatedVoices[0].Voices[0].Url is None
    assert req.AnimatedVoices[0].Voices[0].TTSConfig is None
    assert req.AnimatedVoices[0].Voices[0].Source == 2
    assert req.AnimatedVoices[0].Voices[0].UseCache is True

    assert req.AnimatedVoices[1].Voices[0].Name == "voice_02"
    assert req.AnimatedVoices[1].Voices[0].PreGap == 1.0
    assert req.AnimatedVoices[1].Voices[0].PostGap == 2.0
    assert req.AnimatedVoices[1].Voices[0].Text == "テスト02"
    assert req.AnimatedVoices[1].Voices[0].Url is None
    assert req.AnimatedVoices[1].Voices[0].TTSConfig == tts_config
    assert req.AnimatedVoices[1].Voices[0].Source == 2
    assert req.AnimatedVoices[1].Voices[0].UseCache is False


def test_add_animation():
    req = AnimatedVoiceRequest()

    req.AddAnimation("anim_01")
    req.AddAnimation("anim_02", LayerName="Upper Body", Duration=1.0, FadeLength=2.0, Weight=0.5, PreGap=3.0, Description="test animation")
    req.AddAnimation("anim_03", AsNewFrame=True)

    anim_01 = req.AnimatedVoices[0].Animations["Base Layer"][0]
    assert anim_01.Name == "anim_01"
    assert anim_01.LayerName == "Base Layer"
    assert anim_01.Duration == 0.0
    assert anim_01.FadeLength == -1.0
    assert anim_01.Weight == 1.0
    assert anim_01.PreGap == 0.0
    assert anim_01.Description is None

    anim_02 = req.AnimatedVoices[0].Animations["Upper Body"][0]
    assert anim_02.Name == "anim_02"
    assert anim_02.LayerName == "Upper Body"
    assert anim_02.Duration == 1.0
    assert anim_02.FadeLength == 2.0
    assert anim_02.Weight == 0.5
    assert anim_02.PreGap == 3.0
    assert anim_02.Description == "test animation"

    anim_03 = req.AnimatedVoices[1].Animations["Base Layer"][0]
    assert anim_03.Name == "anim_03"
    assert anim_03.LayerName == "Base Layer"


def test_add_face():
    req = AnimatedVoiceRequest()

    req.AddFace("face_01")
    req.AddFace("face_02", Duration=1.0, Description="test face")

    assert req.AnimatedVoices[0].Faces[0].Name == "face_01"
    assert req.AnimatedVoices[0].Faces[0].Duration == 0.0
    assert req.AnimatedVoices[0].Faces[0].Description is None

    assert req.AnimatedVoices[0].Faces[1].Name == "face_02"
    assert req.AnimatedVoices[0].Faces[1].Duration == 1.0
    assert req.AnimatedVoices[0].Faces[1].Description == "test face"


def test_add_voice_animation_face():
    req = AnimatedVoiceRequest()

    # Frame 1
    req.AddVoice("voice_01")
    req.AddVoice("voice_02")
    req.AddAnimation("anim_01")
    req.AddAnimation("anim_02")
    req.AddAnimation("anim_03", LayerName="Upper Body")
    req.AddAnimation("anim_04", LayerName="Upper Body")
    req.AddFace("face_01")
    req.AddFace("face_02")
    # Frame 2
    req.AddVoice("voice_11", AsNewFrame=True)
    req.AddVoice("voice_12")
    req.AddAnimation("anim_11")
    req.AddAnimation("anim_12")
    req.AddAnimation("anim_13", LayerName="Upper Body")
    req.AddAnimation("anim_14", LayerName="Upper Body")
    req.AddFace("face_11")
    req.AddFace("face_12")

    assert req.AnimatedVoices[0].Voices[0].Name == "voice_01"
    assert req.AnimatedVoices[0].Voices[1].Name == "voice_02"
    assert req.AnimatedVoices[0].Animations["Base Layer"][0].Name == "anim_01"
    assert req.AnimatedVoices[0].Animations["Base Layer"][1].Name == "anim_02"
    assert req.AnimatedVoices[0].Animations["Upper Body"][0].Name == "anim_03"
    assert req.AnimatedVoices[0].Animations["Upper Body"][1].Name == "anim_04"
    assert req.AnimatedVoices[0].Faces[0].Name == "face_01"
    assert req.AnimatedVoices[0].Faces[1].Name == "face_02"

    assert req.AnimatedVoices[1].Voices[0].Name == "voice_11"
    assert req.AnimatedVoices[1].Voices[1].Name == "voice_12"
    assert req.AnimatedVoices[1].Animations["Base Layer"][0].Name == "anim_11"
    assert req.AnimatedVoices[1].Animations["Base Layer"][1].Name == "anim_12"
    assert req.AnimatedVoices[1].Animations["Upper Body"][0].Name == "anim_13"
    assert req.AnimatedVoices[1].Animations["Upper Body"][1].Name == "anim_14"
    assert req.AnimatedVoices[1].Faces[0].Name == "face_11"
    assert req.AnimatedVoices[1].Faces[1].Name == "face_12"


def test_tesponse():
    resp = Response(Id="_")

    resp.AddVoice("local_voice")
    resp.AddVoiceTTS("tts_voice")
    resp.AddVoiceWeb("http://web_voice")
    resp.AddAnimation("walk")
    resp.AddFace("smile")
    avreq = resp.AnimatedVoiceRequest
    assert avreq.AnimatedVoices[0].Voices[0].Name == "local_voice"
    assert avreq.AnimatedVoices[0].Voices[0].Source == VoiceSource.Local
    assert avreq.AnimatedVoices[0].Voices[1].Text == "tts_voice"
    assert avreq.AnimatedVoices[0].Voices[1].Source == VoiceSource.TTS
    assert avreq.AnimatedVoices[0].Voices[2].Url == "http://web_voice"
    assert avreq.AnimatedVoices[0].Voices[2].Source == VoiceSource.Web
    assert avreq.AnimatedVoices[0].Animations["Base Layer"][0].Name == "walk"
    assert avreq.AnimatedVoices[0].Faces[0].Name == "smile"


def test_chatdollkit_exception():
    cex1 = ChatdollKitException()
    assert cex1.error_code == "0000"
    assert cex1.message == "Error"

    cex2 = ChatdollKitException(
        error_code="1234",
        message="error_message"
    )
    assert cex2.error_code == "1234"
    assert cex2.message == "error_message"
    assert str(cex2) == "error_message"


def test_api_response_base():
    ex = Exception("default exception")

    api_response1 = ApiResponseBase.from_exception(ex)
    assert api_response1.Error.Code == "E9999"
    assert api_response1.Error.Message == "Unexpected error"

    api_response2 = ApiResponseBase.from_exception(ex, True)
    assert api_response2.Error.Code == "E9999"
    assert api_response2.Error.Message == "Unexpected error"
    assert api_response2.Error.Detail.startswith("default exception\n")

    cex = ChatdollKitException(error_code="CE1234", message="cdk exception")
    api_response3 = ApiResponseBase.from_exception(cex, True)
    assert api_response3.Error.Code == "CE1234"
    assert api_response3.Error.Message == "cdk exception"
    assert api_response3.Error.Detail.startswith("cdk exception\n")
