from datetime import datetime
from pydantic import BaseModel
from pydantic.typing import Optional, List, Dict, Any


# Model
class TTSConfiguration(BaseModel):
    Name: str = ""
    Params: dict = {}


class VoiceSource:
    Local = 0
    Web = 1
    TTS = 2


class Voice(BaseModel):
    Name: str
    PreGap: float
    PostGap: float
    Text: Optional[str]
    Url: Optional[str]
    TTSConfig: Optional[TTSConfiguration]
    Source: int = VoiceSource.Local
    UseCache: bool = True


class Animation(BaseModel):
    Name: str
    LayerName: Optional[str]
    Duration: float
    FadeLength: float
    Weight: float
    PreGap: float
    Description: Optional[str]


class FaceExpression(BaseModel):
    Name: str
    Duration: float
    Description: Optional[str]


class AnimatedVoice(BaseModel):
    Voices: List[Voice] = []
    Animations: Dict[str, Animation] = {}
    Faces: List[FaceExpression] = []


class AnimatedVoiceRequest(BaseModel):
    AnimatedVoices: List[AnimatedVoice] = []
    DisableBlink: bool = True
    StopIdlingOnStart: bool = True
    StartIdlingOnEnd: bool = True
    StopLayeredAnimations: bool = True
    BaseLayerName: str = "Base Layer"

    def CreateNewFrame(self):
        self.AnimatedVoices.append(AnimatedVoice())
        return len(self.AnimatedVoices)

    def AddVoice(self, Name, PreGap=0.0, PostGap=0.0, AsNewFrame=False):
        if AsNewFrame or len(self.AnimatedVoices) == 0:
            self.CreateNewFrame()
        self.AnimatedVoices[-1].Voices.append(
            Voice(Name=Name, PreGap=PreGap, PostGap=PostGap,
                  Source=VoiceSource.Local, UseCache=False))

    def AddVoiceWeb(self, Url, PreGap=0.0, PostGap=0.0, Name=None,
                    UseCache=True, AsNewFrame=False):
        if AsNewFrame or len(self.AnimatedVoices) == 0:
            self.CreateNewFrame()
        self.AnimatedVoices[-1].Voices.append(
            Voice(Name=Name or "", PreGap=PreGap, PostGap=PostGap,
                  Url=Url, UseCache=UseCache, Source=VoiceSource.Web))

    def AddVoiceTTS(self, Text, PreGap=0.0, PostGap=0.0, Name=None,
                    TTSConfig=None, UseCache=True, AsNewFrame=False):
        if AsNewFrame or len(self.AnimatedVoices) == 0:
            self.CreateNewFrame()
        self.AnimatedVoices[-1].Voices.append(
            Voice(Name=Name or "", PreGap=PreGap, PostGap=PostGap,
                  Text=Text, TTSConfig=TTSConfig, UseCache=UseCache,
                  Source=VoiceSource.TTS))

    def AddAnimation(self, Name, *, LayerName=None, Duration=0.0,
                     FadeLength=-1.0, Weight=1.0, PreGap=0.0, Description=None,
                     AsNewFrame=False):
        if AsNewFrame or len(self.AnimatedVoices) == 0:
            self.CreateNewFrame()
        target_layer = LayerName or self.BaseLayerName
        if target_layer not in self.AnimatedVoices[-1].Animations:
            self.AnimatedVoices[-1].Animations[target_layer] = []
        self.AnimatedVoices[-1].Animations[target_layer].append(
            Animation(Name=Name, LayerName=target_layer, Duration=Duration,
                      FadeLength=FadeLength, Weight=Weight,
                      PreGap=PreGap, Description=Description))

    def AddFace(self, Name, Duration=0.0, Description=None, AsNewFrame=False):
        if AsNewFrame or len(self.AnimatedVoices) == 0:
            self.CreateNewFrame()
        self.AnimatedVoices[-1].Faces.append(
            FaceExpression(Name=Name, Duration=Duration,
                           Description=Description))


# Dialog
class RequestType:
    Undecided = 0
    Voice = 1
    Camera = 2
    QRCode = 3


class Priority:
    Lowest = 0
    Low = 25
    Normal = 50
    High = 75
    Highest = 100


class Topic(BaseModel):
    Name: Optional[str]
    Status: Optional[str]
    IsNew: bool
    ContinueTopic: bool
    Previous: Any
    Priority: int
    RequiredRequestType: int


class Context(BaseModel):
    Id: str
    UserId: str
    Timestamp: datetime
    IsNew: bool
    Topic: Topic
    Data: dict


class User(BaseModel):
    Id: str
    DeviceId: Optional[str]
    Name: Optional[str]
    Nickname: Optional[str]
    Data: dict


class WordNode(BaseModel):
    Word: str
    Part: str
    PartDetail1: str
    PartDetail2: str
    PartDetail3: str
    StemType: str
    StemForm: str
    OriginalForm: str
    Kana: str
    Pronunciation: str

    @classmethod
    def from_janome(cls, tokens):
        words = []
        for t in tokens:
            ps = t.part_of_speech.split(",")
            words.append(cls(
                Word=t.surface,
                Part=ps[0] if len(ps) > 1 and ps[0] != "*" else "",
                PartDetail1=ps[1] if len(ps) > 2 and ps[1] != "*" else "",
                PartDetail2=ps[2] if len(ps) > 3 and ps[2] != "*" else "",
                PartDetail3=ps[3] if len(ps) > 4 and ps[3] != "*" else "",
                StemType=t.infl_type if t.infl_type != "*" else "",
                StemForm=t.infl_form if t.infl_form != "*" else "",
                OriginalForm=t.base_form if t.base_form != "*" else "",
                Kana=t.reading if t.reading != "*" else "",
                Pronunciation=t.phonetic if t.phonetic != "*" else ""
            ))
        return words


class Request(BaseModel):
    Id: str
    Type: int
    Timestamp: datetime
    User: Optional[User]
    Text: Optional[str]
    Payloads: Any
    Intent: Optional[str]
    IntentPriority: int
    Entities: dict
    Words: Optional[List[WordNode]]
    IsAdhoc: bool
    IsCanceled: bool


class Response(BaseModel):
    Id: str
    Timestamp: datetime = datetime.utcnow()
    Text: Optional[str]
    AnimatedVoiceRequests: List[AnimatedVoiceRequest] = [AnimatedVoiceRequest()]
    Payloads: Optional[str]

    @property
    def AnimatedVoiceRequest(self):
        return self.AnimatedVoiceRequests[-1]

    @AnimatedVoiceRequest.setter
    def AnimatedVoiceRequest(self, value):
        self.AnimatedVoiceRequests[-1] = value

    def AddVoice(self, Name, PreGap=0.0, PostGap=0.0, AsNewFrame=False):
        self.AnimatedVoiceRequest.AddVoice(Name, PreGap, PostGap, AsNewFrame)

    def AddVoiceWeb(self, Url, PreGap=0.0, PostGap=0.0, Name=None,
                    UseCache=True, AsNewFrame=False):
        self.AnimatedVoiceRequest.AddVoiceWeb(
            Url, PreGap, PostGap, Name, UseCache, AsNewFrame)

    def AddVoiceTTS(self, Text, PreGap=0.0, PostGap=0.0, Name=None,
                    TTSConfig=None, UseCache=True, AsNewFrame=False):
        self.AnimatedVoiceRequest.AddVoiceTTS(
            Text, PreGap, PostGap, Name, TTSConfig, UseCache, AsNewFrame)

    def AddAnimation(self, Name, *, LayerName=None, Duration=0.0,
                     FadeLength=-1.0, Weight=1.0, PreGap=0.0, Description=None,
                     AsNewFrame=False):
        self.AnimatedVoiceRequest.AddAnimation(
            Name, LayerName=LayerName, Duration=Duration,
            FadeLength=FadeLength, Weight=Weight, PreGap=PreGap,
            Description=Description, AsNewFrame=AsNewFrame)

    def AddFace(self, Name, Duration=0.0, Description=None, AsNewFrame=False):
        self.AnimatedVoiceRequest.AddFace(
            Name, Duration, Description, AsNewFrame)


# API
class ApiRequest(BaseModel):
    Request: Optional[Request]
    Context: Context
    PreProcess: bool = False


class ApiError(BaseModel):
    Code: str
    Message: str
    Detail: Optional[str]


class ApiResponse(BaseModel):
    Request: Optional[Request]
    Context: Context
    Response: Optional[Response]
    Error: Optional[ApiError]


class ApiException(Exception):
    def __init__(self, status_code=500, error_code="0000",
                 message="Error", root_cause=None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.root_cause = root_cause

    def __str__(self):
        return self.message
