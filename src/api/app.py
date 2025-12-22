

# from fastapi import FastAPI
# from src.api.routes import router

# app = FastAPI(
#     title="AI Resume Skill Gap Analyzer",
#     description="ML-powered resume–JD skill gap analysis API",
#     version="1.0"
# )

# app.include_router(router)


from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="AI Resume Skill Gap Analyzer")

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(router)
