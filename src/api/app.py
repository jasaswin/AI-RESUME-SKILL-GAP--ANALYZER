

# from fastapi import FastAPI
# from src.api.routes import router

# app = FastAPI(
#     title="AI Resume Skill Gap Analyzer",
#     description="ML-powered resume–JD skill gap analysis API",
#     version="1.0"
# )

# app.include_router(router)


# from fastapi import FastAPI
# from src.api.routes import router

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # for development
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app = FastAPI(title="AI Resume Skill Gap Analyzer")

# @app.get("/")
# def root():
#     return {"message": "API is running"}

# app.include_router(router)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "src.api.app:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True
#     )


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

# ✅ Step 1: Create app FIRST
app = FastAPI(title="AI Resume Skill Gap Analyzer")

# ✅ Step 2: Add CORS AFTER app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Step 3: Test route
@app.get("/")
def root():
    return {"message": "API is running"}

# ✅ Step 4: Include routes
app.include_router(router)

# ✅ Step 5: Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )