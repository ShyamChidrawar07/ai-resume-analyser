
from dataclasses import dataclass
import re

DEFAULT_SKILLS = (
    "python", "java", "sql", "mysql", "django",
    "flask", "rest api", "django rest framework",
    "react", "html", "css", "javascript",
    "git", "docker", "machine learning", "pandas", "numpy",
)


@dataclass
class MatchResult:
    resume_skills: tuple[str, ...]
    job_skills: tuple[str, ...]
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]
    match_percentage: float


class SkillMatcher:
    def __init__(self,
    skills: tuple[str, ...] = DEFAULT_SKILLS ) -> None:
    
        self.skills = tuple(skill.lower() for skill in skills)

    def extract_skills(self, text: str) -> tuple[str, ...]:
        text = text.lower()
        skills_found = set()

        if not text:
            return tuple()

        for skill in self.skills:
            pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
            if re.search(pattern, text):
                skills_found.add(skill)

        return tuple(
            skill for skill in self.skills
            if skill in skills_found
        )

    def analyze(self,resume_text: str,job_description: str ) -> MatchResult:

        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)

        resume_skills_set = set(resume_skills)

        matched_skills = tuple(
            skill for skill in job_skills
            if skill in resume_skills_set
        )

        missing_skills = tuple(
            skill for skill in job_skills
            if skill not in resume_skills_set
        )

        if job_skills:
            percentage = round(
                len(matched_skills) / len(job_skills) * 100, 1)
        else:
            percentage = 0.0

        return MatchResult(
            resume_skills=resume_skills,
            job_skills=job_skills,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            match_percentage=percentage,
        )


if __name__ == "__main__":
    matcher = SkillMatcher()

    resume = "Python, Django, REST API, Git"
    job_description = "Python, Django, MySQL, Docker, Git"
    result = matcher.analyze(resume, job_description)

    print("Resume skills:", result.resume_skills)
    print("Job skills:", result.job_skills)
    print("Matched skills:", result.matched_skills)
    print("Missing skills:", result.missing_skills)
    print("Match percentage:", result.match_percentage, "%")
