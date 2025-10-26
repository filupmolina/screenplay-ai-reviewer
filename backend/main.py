"""
FastAPI server for Screenplay AI Reviewer
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from services.parser import FountainParser
from services.feedback_engine import FeedbackEngine, ReviewSession
from services.ai_provider import AnthropicProvider
from models.reviewer import REVIEWER_PROFILES
from models.entity import EntityTracker

app = FastAPI(title="Screenplay AI Reviewer API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    """Request to analyze a screenplay"""
    reviewer_ids: List[str]


class SceneFeedbackResponse(BaseModel):
    """Feedback for a single scene from one reviewer"""
    scene_number: int
    reviewer_id: str
    reviewer_name: str
    feedback: str
    emotional_state: dict
    scene_rating: Optional[float] = None


class AnalysisResponse(BaseModel):
    """Response with full analysis"""
    screenplay_title: Optional[str]
    total_scenes: int
    total_pages: Optional[int]
    reviewers: List[str]
    feedback: List[SceneFeedbackResponse]
    overall_stats: dict


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Screenplay AI Reviewer API",
        "available_reviewers": len(REVIEWER_PROFILES),
    }


@app.get("/reviewers")
async def get_reviewers():
    """Get list of available reviewer personas"""
    reviewers = []
    for reviewer_id, profile in REVIEWER_PROFILES.items():
        reviewers.append({
            "id": reviewer_id,
            "name": profile.name,
            "type": profile.reviewer_type.value,
            "description": profile.description,
        })
    return {"reviewers": reviewers}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_screenplay(
    file: UploadFile = File(...),
    reviewer_ids: str = "jordan_peele,sam_raimi",  # Comma-separated
):
    """
    Analyze a screenplay with selected reviewers

    - **file**: PDF or Fountain file
    - **reviewer_ids**: Comma-separated list of reviewer IDs
    """
    # Validate file type
    if not file.filename.endswith(('.pdf', '.fountain')):
        raise HTTPException(
            status_code=400,
            detail="File must be .pdf or .fountain format"
        )

    # Parse reviewer IDs
    selected_reviewers = [rid.strip() for rid in reviewer_ids.split(',')]

    # Validate reviewers
    invalid_reviewers = [rid for rid in selected_reviewers if rid not in REVIEWER_PROFILES]
    if invalid_reviewers:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid reviewer IDs: {', '.join(invalid_reviewers)}"
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Parse screenplay
        parser = FountainParser()
        screenplay = parser.parse_file(tmp_file_path)

        # Initialize AI provider
        try:
            ai_provider = AnthropicProvider()
        except ValueError as e:
            raise HTTPException(
                status_code=500,
                detail=f"AI configuration error: {str(e)}. Please set ANTHROPIC_API_KEY environment variable."
            )

        # Initialize entity tracker
        entity_tracker = EntityTracker()
        for scene in screenplay.scenes:
            for entity_name in scene.characters_present:
                entity = entity_tracker.get_or_create_character(entity_name, scene.scene_number)
                entity.add_appearance(scene.scene_number)

        # Initialize feedback engine with AI provider
        engine = FeedbackEngine(
            ai_providers={"anthropic": ai_provider},
            reviewer_configs=[
                {"profile": reviewer_id, "ai_provider": "anthropic"}
                for reviewer_id in selected_reviewers
            ]
        )

        # Process screenplay (this will take a while with AI calls)
        session = engine.review_screenplay(screenplay, entity_tracker)

        # Format response
        feedback_list = []
        for scene_feedback in session.all_feedback:
            feedback_list.append({
                "scene_number": scene_feedback.scene_number,
                "reviewer_id": scene_feedback.reviewer_id,
                "reviewer_name": scene_feedback.reviewer_name,
                "feedback": scene_feedback.feedback,
                "emotional_state": {
                    "engagement": scene_feedback.emotional_state.engagement_level,
                    "enjoyment": scene_feedback.emotional_state.enjoyment,
                    "confusion": scene_feedback.emotional_state.confusion,
                    "suspense": scene_feedback.emotional_state.suspense,
                    "excitement": scene_feedback.emotional_state.excitement,
                },
                "scene_rating": scene_feedback.scene_rating,
            })

        # Calculate overall stats
        overall_stats = {
            "avg_engagement": sum(f["emotional_state"]["engagement"] for f in feedback_list) / len(feedback_list) if feedback_list else 0,
            "avg_enjoyment": sum(f["emotional_state"]["enjoyment"] for f in feedback_list) / len(feedback_list) if feedback_list else 0,
            "avg_suspense": sum(f["emotional_state"]["suspense"] for f in feedback_list) / len(feedback_list) if feedback_list else 0,
            "avg_confusion": sum(f["emotional_state"]["confusion"] for f in feedback_list) / len(feedback_list) if feedback_list else 0,
        }

        return {
            "screenplay_title": screenplay.title,
            "total_scenes": screenplay.total_scenes,
            "total_pages": screenplay.total_pages,
            "reviewers": selected_reviewers,
            "feedback": feedback_list,
            "overall_stats": overall_stats,
        }

    finally:
        # Clean up temp file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
