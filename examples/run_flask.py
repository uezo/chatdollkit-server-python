from flask import Flask
from chatdollkit.controllers.flask_controller import bp as api_bp
from .myapp import MyApp

# Create Flask app
app = Flask(__name__)

# Create ChatdollKit server app and set it to Flask application
app.chatdoll_app = MyApp(app.logger, True)

# Register API controller
app.register_blueprint(api_bp)


if __name__ == "__main__":
    # Start API
    app.run(port="12345", debug=True)
