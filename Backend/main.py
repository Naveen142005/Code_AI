from fastapi.middleware.cors import CORSMiddleware
from dark_swag import FastAPI
from api.setup_routers import router

app = FastAPI()
app.include_router(router, tags=['SetUp Router'])



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)