from fastapi import FastAPI
from chatdollkit.controllers.fastapi_controller import router
from .myapp import MyApp

# Create FastAPI app
app = FastAPI()

# Create ChatdollKit server app and set it to FastAPI application
app.chatdoll_app = MyApp(None, True)

# Register API controller
app.include_router(router)
