from fastapi import FastAPI
from api import router as api_router

app = FastAPI(title="TDS Virtual TA API")

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "TDS Virtual TA API is running."}

def main():
    print("Hello from tds-proj!")


if __name__ == "__main__":
    main()
