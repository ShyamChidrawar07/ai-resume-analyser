from pydantic import BaseModel, Field

from resume_analyzer.services.skill_matcher import MatchResult

class AnalysisResponse(BaseModel):
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    match_percentage: float = Field(ge=0.0, le=100.0)

    @classmethod
    def from_match_result(cls, match_result: MatchResult) -> "AnalysisResponse":
        return cls(
            required_skills=match_result.job_skills,
            matched_skills=match_result.matched_skills,
            missing_skills=match_result.missing_skills,
            match_percentage=match_result.match_percentage,
        )
