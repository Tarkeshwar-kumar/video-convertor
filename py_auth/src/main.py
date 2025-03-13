from fastapi import FastAPI
from routers import router


app = FastAPI()

def main():
    print("running main")
    app.include_router(router)


main()