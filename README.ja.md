# ChatdollKit Server SDK for Python

SDK to create backend APIs for ChatdollKit. See also 👉 [ChatdollKit](https://github.com/uezo/ChatdollKit)

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

ユーザーの発話内容をおうむ返しするサンプルAPIサーバを起動します。

```bash
$ python flaskapp.py
```

続いてUnityで3Dモデルに`HttpDialogRouter`と`HttpPrompter`をアタッチして以下のとおり設定します。

- Intent Extractor Uri: `http://localhost:12345/chatdollkit/intent`
- Dialog Processor Uri Base: `http://localhost:12345/chatdollkit/dialog`
- Prompter Uri: `http://localhost:12345/chatdollkit/prompter`
- Ping Uri: `http://localhost:12345/chatdollkit/ping`

※Text-to-Speechを利用しますので、関連する設定も行います

最後にChatdollアプリを起動して対話を開始してみましょう。3Dモデルがあなたの発話内容をおうむ返ししてくれるはずです。


# 対話処理のカスタマイズ

`PrompterBase`、`IntentExtractorBase`、`DialogProcessorBase`を継承したクラスを作って、以下のようにそれぞれのメソッドをオーバーライドして処理を実装します。

```python
class MyPrompter(PrompterBase):
    def get_prompt(self, context, response):
        response.AddVoiceTTS("May I help you?")

class MyIntentExtractor(IntentExtractorBase):
    def extract_intent(self, request, context):
        # define conditions to decide intent
        if ("weather" in request.Text):
            request.Intent = "weather"
        elif ("translation" in request.Text):
            request.Intent = "translation"
        else:
            request.Intent = "chat"
            request.IntentPriority = Priority.Low

class WeatherDialog(DialogProcessorBase):
    def process(self, request, context, response):
        weather = get_weather() # getting weather
        response.AddVoiceTTS(
            f"It's {weather} today.")
```

FastAPIなどの非同期処理をサポートするフレームワークを利用する場合は、上記例のかわりに`get_prompt_async`、`extract_intent_async`、`process_async`をオーバーライドしましょう。

最後に、作ったクラスをアプリケーションに登録すれば利用可能になります。

```python
dialog_classes = {
    "weather": WeatherDialog,
    "translation": TranslationDialog,
    "chat": ChatDialog
}
FlaskConnector.configure_app(
    app, MyIntentExtractor, dialog_classes, MyPrompter, debug=True)
```

# その他のアプリケーションフレームワークの利用

FlaskやFastAPI以外を利用する場合、`ConnectorBase`を継承したコネクタクラスを自作して以下のメソッドを実装してください。

- `parse_request` : HTTPリクエストを内部利用のAPI各種オブジェクトに変換
- `make_response`: 内部利用の各種APIオブジェクトをHTTPレスポンスに変換
- `make_error_response`: 内部利用の各種APIオブジェクトをHTTPレスポンス（エラー情報つき）に変換
