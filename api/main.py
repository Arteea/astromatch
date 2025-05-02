from fastapi import FastAPI

app = FastAPI()



@app.post('register',)
async def register_user(user: dict):
    pass