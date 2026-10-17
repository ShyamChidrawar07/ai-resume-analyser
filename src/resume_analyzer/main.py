from fastapi import FastAPI
from resume_analyzer.controllers.analysis_controller import router
# import uvicorn

app = FastAPI(title="AI Resume Analyzer & Job Matcher")

app.include_router(router)


# For Maually setting configuration of backend
# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True
#     )    
