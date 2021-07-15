# ChatdollKit Server SDK for Python

ChatdollKitのスキルをサーバーで実行するためのSDKです。 See also 👉 [ChatdollKit](https://github.com/uezo/ChatdollKit)

[🇬🇧README in English](https://github.com/uezo/chatdollkit-dialog-python/blob/master/README.md)

# インストール

```bash
$ pip install chatdollkit
```

あわせてアプリケーションサーバもインストールします。[Flask](https://flask.palletsprojects.com/) と [FastAPI](https://fastapi.tiangolo.com/) をサポート。

```bash
$ pip install flask
```

または

```bash
$ pip install fastapi uvicorn
```


# クイックスタート

## サーバー側

Exampleに含まれるユーザーの発話内容をおうむ返しするAPIサーバを起動します。

```bash
$ python run_flask.py
```

または

```bash
$ uvicorn run_fastapi:app --port 12345 --reload
```

## クライアント側

[ChatdollKitのマニュアル](https://github.com/uezo/ChatdollKit/blob/master/manual.ja.md#クライアントの準備)を参照ください。ChatdollKitに同梱されているSkillServerのサンプルの利用手順です。

スキルサーバーをlocalhost以外で動かす場合は、`HttpSkillRouter`と`HttpPrompter`のインスペクター上で各種URLを設定してください。

サーバー・クライアント双方の設定が完了したら、最後にChatdollアプリを起動して対話を開始してみましょう。3Dモデルがあなたの発話内容をおうむ返ししてくれるはずです。


# スキルサーバーの作り方

基本的には、スキル、サーバーアプリケーション本体、エントリーポイントを実装していくことで独自のスキルサーバーを作ることができます。

まずは `allinone.py` を作成し、以下の通り必要なライブラリーをインポートしましょう。

```python
from flask import Flask
from chatdollkit.app import SkillBase, AppBase
from chatdollkit.models import (
    Request, Response, State, IntentExtractionResult, Intent
)
from chatdollkit.controllers.flask_controller import bp as api_bp
```

## 1. スキル

`SkillBase` を継承した `EchoSkill` クラスを作成し、 `process` メソッドを実装します。例ではText-to-Speechのボイスを含むレスポンスを返しています。

```python
class EchoSkill(SkillBase):
    topic = "echo"

    def process(self, request: Request, state: State) -> Response:
        # Just echo
        resp = Response(Id=request.Id)
        resp.AddVoiceTTS(request.Text)
        return resp
```

## 2. サーバーアプリケーション

`AppBase` を継承する `MyApp` クラスを作成し、 ユーザーに発話を要求する `get_prompt` メソッドと `EchoSkill` へのルーティングに必要な情報を返す `extract_intent` メソッドを実装します。

```python
class MyApp(AppBase):
    # Register skill(s)
    skills = [EchoSkill]

    def get_prompt(self, request: Request, state: State) -> Response:
        # Return prompt message
        resp = Response(Id="_" if request is None else request.Id)
        resp.AddVoiceTTS("This prompt is from server. Please say something.")
        return resp

    def extract_intent(self, request: Request, state: State) -> IntentExtractionResult:
        # Always extract Echo intent
        return IntentExtractionResult(Intent=Intent(Name=EchoSkill.topic))
```

## 3. アプリケーションエントリーポイント

最後に、作成した `MyApp` のインスタンスをFlaskアプリケーションに生やした上でAPIコントローラーを登録します。

```python
# Create Flask app
app = Flask(__name__)
# Create ChatdollKit server app and set it to Flask application
app.chatdoll_app = MyApp(app.logger, True)
# Register API controller
app.register_blueprint(api_bp)

if __name__ == "__main__":
    # Start API
    app.run(port="12345", debug=True)
```

FastAPIベースのスキルサーバーを作るにはExampleの内容をご確認ください。


# 他のアプリケーションサーバーを利用する方法

FlaskまたはFastAPI以外のアプリケーションサーバーを利用するには、ChatdollKitクライアントからのHTTPリクエストのハンドラーを自身で作成してください。スキル、サーバーアプリケーション、モデルはそのまま利用可能です。ハンドルすべきエンドポイント等はサンプルの`chatdollkit.controllers.flask_controller.py`または`fastapi_controller.py`を参照してください。前者が同期、後者が非同期です。
