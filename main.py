from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router

app = FastAPI(title="TDS Virtual TA API")

# Allow all CORS origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "TDS Virtual TA API is running."}

def main():
    print("Hello from tds-proj!")


if __name__ == "__main__":
    main()
