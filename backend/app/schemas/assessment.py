from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from app.models.assessment import DifficultyLevel, AssessmentCategory


class QuestionBase(BaseModel):
    question_text: str
    context: Optional[str] = None
    constraints: Optional[str] = None
    expected_skills: Optional[str] = None
    order_index: int = 0
    max_score: float = 100.0


class QuestionCreate(QuestionBase):
    pass


class QuestionOut(QuestionBase):
    id: int
    assessment_id: int

    model_config = ConfigDict(from_attributes=True)


class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: AssessmentCategory = AssessmentCategory.TECHNICAL
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    estimated_minutes: int = 30


class AssessmentCreate(AssessmentBase):
    questions: Optional[List[QuestionCreate]] = []


class AssessmentOut(AssessmentBase):
    id: int
    is_active: bool
    created_at: datetime
    questions: List[QuestionOut] = []

    model_config = ConfigDict(from_attributes=True)


class AssessmentListItem(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: AssessmentCategory
    difficulty: DifficultyLevel
    estimated_minutes: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class StartAssessmentRequest(BaseModel):
    assessment_id: int


class StartAssessmentResponse(BaseModel):
    session_id: str
    assessment: AssessmentOut
    message: str = "Assessment started successfully"


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: int
    answer_text: str = Field(..., min_length=10)
    time_spent_seconds: int = Field(..., ge=0)
    word_count: int = Field(..., ge=0)


class SubmitAnswerResponse(BaseModel):
    response_id: int
    message: str = "Answer submitted"
    content_score: Optional[float] = None
    process_score: Optional[float] = None
    final_score: Optional[float] = None
