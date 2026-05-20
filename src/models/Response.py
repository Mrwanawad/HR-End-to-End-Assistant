from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, List, Optional


class CandidateOverview(BaseModel):
    name: Optional[str] = Field(None, description="Full name extracted from CV")
    current_title: Optional[str] = Field(None, description="Most recent job title")
    total_years_experience: Optional[float] = Field(None, description="Total years of professional experience")
    education: Optional[str] = Field(None, description="Highest relevant degree summary")
    location: Optional[str] = Field(None, description="Candidate's current location")
    cv_language: Optional[str] = Field(None, description="Primary language of the CV")

    @field_validator("cv_language", mode="before")
    @classmethod
    def coerce_cv_language(cls, v):
        if not v or not isinstance(v, str):
            return "Unknown"
        return v
    open_to_relocation: Literal["Yes", "No", "Unknown"] = Field("Unknown")
    work_preference: Literal["Remote", "Hybrid", "On-Site", "Unknown"] = Field("Unknown")

    @field_validator("open_to_relocation", mode="before")
    @classmethod
    def coerce_relocation(cls, v):
        return v if v in {"Yes", "No", "Unknown"} else "Unknown"

    @field_validator("work_preference", mode="before")
    @classmethod
    def coerce_work_preference(cls, v):
        return v if v in {"Remote", "Hybrid", "On-Site", "Unknown"} else "Unknown"


class SeniorityAssessment(BaseModel):
    level: Literal["Junior", "Mid-Level", "Senior", "Lead", "Principal", "Executive"]
    confidence: Literal["High", "Medium", "Low"]
    justification: str = Field(..., description="2-3 sentence rationale based on CV evidence")

    @field_validator("level", mode="before")
    @classmethod
    def coerce_level(cls, v):
        return v if v in {"Junior", "Mid-Level", "Senior", "Lead", "Principal", "Executive"} else "Junior"

    @field_validator("confidence", mode="before")
    @classmethod
    def coerce_confidence(cls, v):
        return v if v in {"High", "Medium", "Low"} else "Low"


class SkillBreakdownItem(BaseModel):
    required_skill: str
    candidate_status: Literal["Matched", "Partial", "Missing"]
    evidence: Optional[str] = Field(None, description="Quote or reference from CV")

    @field_validator("candidate_status", mode="before")
    @classmethod
    def coerce_candidate_status(cls, v):
        return v if v in {"Matched", "Partial", "Missing"} else "Missing"

    @model_validator(mode="before")
    @classmethod
    def coerce_from_string(cls, v):
        """If the LLM returns a plain string instead of a dict, wrap it gracefully."""
        if isinstance(v, str):
            return {"required_skill": v, "candidate_status": "Missing", "evidence": None}
        return v


class StackCompatibility(BaseModel):
    overall_compatibility_score: int = Field(..., ge=0, le=100)
    breakdown: List[SkillBreakdownItem]

    @field_validator("overall_compatibility_score", mode="before")
    @classmethod
    def coerce_score(cls, v):
        try:
            return max(0, min(100, int(v)))
        except (TypeError, ValueError):
            return 0


class CareerTrajectory(BaseModel):
    trend: Literal["Ascending", "Stable", "Declining", "Pivoting"]
    avg_tenure_months: Optional[float] = Field(None, description="Average months spent per role")
    job_hopper_flag: bool = Field(False, description="True if 2+ consecutive roles under 12 months")
    industries_worked_in: List[str] = Field(default_factory=list)
    industry_match_score: int = Field(..., ge=0, le=100, description="How well industries align with role")

    @field_validator("trend", mode="before")
    @classmethod
    def coerce_trend(cls, v):
        return v if v in {"Ascending", "Stable", "Declining", "Pivoting"} else "Stable"

    @field_validator("industry_match_score", mode="before")
    @classmethod
    def coerce_industry_match_score(cls, v):
        try:
            return max(0, min(100, int(v)))
        except (TypeError, ValueError):
            return 0

    @field_validator("industries_worked_in", mode="before")
    @classmethod
    def coerce_industries(cls, v):
        if not isinstance(v, list):
            return []
        return [str(i) for i in v if i]


class CompensationSignal(BaseModel):
    estimated_min: Optional[float] = Field(None, description="Estimated minimum salary expectation")
    estimated_max: Optional[float] = Field(None, description="Estimated maximum salary expectation")
    currency: str = Field("USD")
    likely_above_budget: bool = Field(False, description="Flag if candidate likely expects above budget")

    @field_validator("estimated_min", "estimated_max", mode="before")
    @classmethod
    def coerce_salary(cls, v):
        if v is None or v == "" or str(v).lower() in {"not provided", "unknown", "n/a"}:
            return None
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    @field_validator("likely_above_budget", mode="before")
    @classmethod
    def coerce_budget_flag(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in {"true", "yes", "1"}
        return False


class CommunicationSignal(BaseModel):
    cv_quality_score: int = Field(..., ge=0, le=100, description="Overall CV clarity and professionalism")
    communication_signal: Literal["Strong", "Average", "Weak"]

    @field_validator("communication_signal", mode="before")
    @classmethod
    def coerce_communication_signal(cls, v):
        return v if v in {"Strong", "Average", "Weak"} else "Average"

    @field_validator("cv_quality_score", mode="before")
    @classmethod
    def coerce_cv_quality_score(cls, v):
        try:
            return max(0, min(100, int(v)))
        except (TypeError, ValueError):
            return 0


class FullEvaluation(BaseModel):
    strengths: List[str]
    gaps: List[str]
    red_flags: List[str]
    notable_achievements: List[str]
    cultural_fit_indicators: Optional[str] = Field(None)

    @field_validator("cultural_fit_indicators", mode="before")
    @classmethod
    def coerce_cultural_fit(cls, v):
        if not v or not isinstance(v, str):
            return "Not assessed."
        return v
    hiring_recommendation: Literal["Strong Hire", "Hire", "Conditional Hire", "No Hire"]
    recommendation_rationale: str = Field(..., description="3-4 sentence professional summary")
    final_fit_score: int = Field(..., ge=0, le=100)

    @field_validator("hiring_recommendation", mode="before")
    @classmethod
    def coerce_hiring_recommendation(cls, v):
        return v if v in {"Strong Hire", "Hire", "Conditional Hire", "No Hire"} else "Conditional Hire"

    @field_validator("final_fit_score", mode="before")
    @classmethod
    def coerce_final_fit_score(cls, v):
        try:
            return max(0, min(100, int(v)))
        except (TypeError, ValueError):
            return 0

    @field_validator("strengths", "gaps", "red_flags", "notable_achievements", mode="before")
    @classmethod
    def coerce_str_lists(cls, v):
        if not isinstance(v, list):
            return []
        return [str(i) for i in v if i]


# ── Global sanitizer ─────────────────────────────────────────────────────────
# Walks the raw dict from the LLM and coerces None / wrong-type values to safe
# defaults BEFORE any sub-model validator runs. Add entries here if new fields
# fail in future runs — no need to touch individual models.

_STR_DEFAULTS: dict[tuple[str, ...], str] = {
    ("candidate_overview",  "cv_language"):                  "Unknown",
    ("seniority_assessment","justification"):                "No justification provided.",
    ("career_trajectory",   "trend"):                        "Stable",
    ("full_evaluation",     "cultural_fit_indicators"):      "Not assessed.",
    ("full_evaluation",     "hiring_recommendation"):        "Conditional Hire",
    ("full_evaluation",     "recommendation_rationale"):     "No rationale provided.",
    ("communication_signal","communication_signal"):         "Average",
    ("screening_verdict",):                                  "Borderline",
    ("one_line_summary",):                                   "No summary provided.",
}

_BOOL_DEFAULTS: dict[tuple[str, ...], bool] = {
    ("career_trajectory",   "job_hopper_flag"):   False,
    ("compensation_signal", "likely_above_budget"): False,
}

_INT_DEFAULTS: dict[tuple[str, ...], int] = {
    ("stack_compatibility", "overall_compatibility_score"): 0,
    ("career_trajectory",   "industry_match_score"):        0,
    ("communication_signal","cv_quality_score"):            0,
    ("full_evaluation",     "final_fit_score"):             0,
}


def _sanitize_raw(raw: dict) -> dict:
    """Coerce None / wrong-type values across the nested LLM response dict."""
    def _get(d: dict, keys: tuple):
        if len(keys) == 1:
            return d
        sub = d.get(keys[0])
        if isinstance(sub, dict):
            return sub
        return None

    def _set(d: dict, keys: tuple, value):
        if len(keys) == 1:
            if d.get(keys[0]) is None:
                d[keys[0]] = value
        else:
            sub = d.setdefault(keys[0], {})
            if isinstance(sub, dict) and sub.get(keys[1]) is None:
                sub[keys[1]] = value

    for keys, default in _STR_DEFAULTS.items():
        _set(raw, keys, default)

    for keys, default in _BOOL_DEFAULTS.items():
        _set(raw, keys, default)

    for keys, default in _INT_DEFAULTS.items():
        _set(raw, keys, default)

    return raw


class LLMCandidateResponse(BaseModel):

    screening_verdict: Literal["Fast-Track", "Standard", "Borderline", "Reject"]
    one_line_summary: str = Field(..., description="One punchy sentence: title, exp, highlight, verdict")

    candidate_overview: CandidateOverview
    seniority_assessment: SeniorityAssessment
    stack_compatibility: StackCompatibility
    career_trajectory: CareerTrajectory
    compensation_signal: CompensationSignal
    communication_signal: CommunicationSignal
    full_evaluation: FullEvaluation

    @model_validator(mode="before")
    @classmethod
    def sanitize_all(cls, values):
        if isinstance(values, dict):
            values = _sanitize_raw(values)
        return values

    @field_validator("screening_verdict", mode="before")
    @classmethod
    def coerce_screening_verdict(cls, v):
        return v if v in {"Fast-Track", "Standard", "Borderline", "Reject"} else "Borderline"


if __name__ == "__main__":
    print(f"Model Schema:\n{LLMCandidateResponse.model_json_schema()}")