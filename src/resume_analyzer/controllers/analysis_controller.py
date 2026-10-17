from fastapi import APIRouter, File, Form, HTTPException, Path, Query, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path as FilePath

from resume_analyzer.schemas.analysis import AnalysisResponse
from resume_analyzer.services.pdf_reader import (
    NoExtractableTextError,
    PdfReadError,
    PdfTextExtractor,
)
from resume_analyzer.services.skill_matcher import SkillMatcher


router = APIRouter()
skill_matcher = SkillMatcher()
pdf_extractor = PdfTextExtractor()


TEMPLATE_PATH = FilePath(__file__).resolve().parent.parent / "views" / "templates" / "index.html"

@router.get("/", include_in_schema=False)
async def home():
    return FileResponse(TEMPLATE_PATH)

@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}



@router.get("/greet/{name}")
def greet(candidate_name: str = Path(..., alias="name")):
    return f"Hello, {candidate_name}! Welcome to the AI Resume Analyzer & Job Matcher API."

@router.get("/hello")
def greet(candidate_name: str = Query(..., alias="name")):
    return f"Hello, {candidate_name}! Welcome to the AI Resume Analyzer & Job Matcher API."


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(..., alias="resume"),
    job_description: str = Form(..., alias="job_description"),
) -> AnalysisResponse:
    try:
        job_description_text = job_description.strip()
        if not job_description_text:
            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty.",
            )

        filename = (resume.filename or "").lower()
        if not filename.endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        pdf_bytes = await resume.read()
        if not pdf_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF file is empty.",
            )
        if b"%PDF-" not in pdf_bytes[:1024]:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file does not have a valid PDF header.",
            )

        resume_text = pdf_extractor.extract_text(pdf_bytes)

    except NoExtractableTextError as exc:
        raise HTTPException(
            status_code=422,
            detail="No extractable text found. Image-only PDFs require OCR.",
        ) from exc
    except PdfReadError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
    finally:
        await resume.close()

    result = skill_matcher.analyze(resume_text, job_description_text)
    return AnalysisResponse.from_match_result(result)
