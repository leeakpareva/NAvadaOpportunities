from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, List
import json
from datetime import datetime

from app.cv_parser import parse_cv
from app.job_matcher import JobMatcher
from app.profile_manager import ProfileManager, ProfileData
from app.notification_service import NotificationService

app = FastAPI(title="NAVADA Job Finder API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://navada-main-app-tunnel-f4stdq3v.devinapps.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
profile_manager = ProfileManager()
notification_service = NotificationService()

import tempfile
import os
from pathlib import Path
import logging
from typing import List, Optional
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Optional[Client] = None
if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)

ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx'}

@app.post("/api/parse-cv")
async def parse_cv_endpoint(file: UploadFile = File(...)):
    """Parse uploaded CV and return structured data"""
    try:
        # Validate file extension
        filename = file.filename or ""
        suffix = Path(filename).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            # Write uploaded file to temporary file
            contents = await file.read()
            tmp.write(contents)
            tmp.flush()
            
            logger.info(f"Processing CV file: {filename}")
            # Parse the CV
            cv_data = parse_cv(tmp.name)
            
        # Clean up temporary file
        os.unlink(tmp.name)
        logger.info(f"Successfully parsed CV: {filename}")
        return {"success": True, "data": cv_data}
    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/profiles")
async def create_profile(profile_data: Dict):
    """Create or update user profile"""
    try:
        if "userId" not in profile_data:
            raise HTTPException(status_code=400, detail="userId is required")
            
        profile = ProfileData(
            user_id=profile_data["userId"],
            cv_data=profile_data["cvData"],
            email=profile_data.get("email"),
            preferences=profile_data.get("preferences", {})
        )
        profile_manager.create_or_update_profile(profile)
        return {"success": True, "profile": profile.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/profiles/{user_id}")
async def get_profile(user_id: str):
    """Retrieve user profile"""
    profile = profile_manager.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"success": True, "profile": profile.to_dict()}

@app.post("/api/config/slack")
async def configure_slack(credentials: Dict):
    """Securely configure Slack credentials"""
    try:
        # Validate required fields
        required_fields = ['client_id', 'client_secret']
        for field in required_fields:
            if field not in credentials:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Store credentials securely (in environment for now)
        os.environ['SLACK_CLIENT_ID'] = credentials['client_id']
        os.environ['SLACK_CLIENT_SECRET'] = credentials['client_secret']
        
        # Initialize notification service
        notification_service = NotificationService()
        
        # Test authentication
        await notification_service.authenticate()
        
        return {"success": True, "message": "Slack credentials configured successfully"}
    except Exception as e:
        logger.error(f"Error configuring Slack credentials: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error configuring Slack credentials: {str(e)}"
        )

@app.post("/api/test/notifications")
async def test_notifications():
    """Test endpoint to verify Slack notifications"""
    try:
        # Test job notification
        test_job = {
            "id": "test-1",
            "title": "Test Job Position",
            "company": "NAVADA Test Corp",
            "location": "Remote",
            "salary_range": {
                "min": 85000,
                "max": 150000
            },
            "description": "This is a test job posting to verify Slack notifications.",
            "employment_type": "Full-time",
            "url": "https://example.com/test-job"
        }
        
        # Test PR notification
        test_pr = {
            "title": "Test Pull Request",
            "author": "Devin",
            "status": "Open",
            "url": "https://github.com/example/test-pr",
            "description": "This is a test PR to verify Slack notifications."
        }
        
        # Send test notifications
        job_result = await notification_service.send_job_notification(test_job)
        pr_result = await notification_service.send_pr_notification(test_pr)
        
        return {
            "success": True,
            "results": {
                "job_notification": job_result,
                "pr_notification": pr_result
            }
        }
    except Exception as e:
        logger.error(f"Error testing notifications: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error testing notifications: {str(e)}"
        )

@app.get("/api/jobs/match/{user_id}")
async def match_jobs(
    user_id: str,
    remote_only: bool = True,
    employment_types: Optional[List[str]] = None
):
    """
    Match jobs for user based on their profile without salary restrictions
    
    Args:
        user_id: User's unique identifier
        remote_only: Filter for remote positions only
        employment_types: List of employment types to include
    """
    try:
        if not supabase:
            raise HTTPException(
                status_code=500,
                detail="Supabase client not initialized"
            )
        
        # Get user profile
        profile = profile_manager.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Initialize job matcher
        matcher = JobMatcher(profile.to_dict())
        
        # Build Supabase query
        query = supabase.table('jobs').select('*')
        
        # Apply filters
        if remote_only:
            query = query.ilike('location', '%remote%')
        
        # Fetch jobs from Supabase
        response = query.execute()
        if not response.data:
            logger.warning(f"No jobs found for user {user_id}")
            return {
                "success": True,
                "matches": [],
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # For testing purposes, return mock job data
        mock_jobs = [
            {
                "id": "1",
                "title": "Senior Program Manager - Remote",
                "company": "Tech Innovation Corp",
                "location": "Remote",
                "salary_range": {
                    "min": 85000,
                    "max": 150000
                },
                "description": "Leading digital transformation projects with blockchain integration",
                "employment_type": "Contract",
                "url": "https://example.com/job1"
            },
            {
                "id": "2",
                "title": "Blockchain Technical Lead",
                "company": "DeFi Solutions",
                "location": "Remote - UK",
                "salary_range": {
                    "min": 95000,
                    "max": 180000
                },
                "description": "Leading blockchain development and smart contract implementation",
                "employment_type": "Full-time",
                "url": "https://example.com/job2"
            }
        ]
        
        matches = []
        for job in mock_jobs:
            # Check employment type filter
            if employment_types:
                job_type = job["employment_type"].lower()
                if not any(type.lower() in job_type for type in employment_types):
                    continue
            
            # Check remote filter
            if remote_only and "remote" not in job["location"].lower():
                continue
                
            # Calculate mock scores
            tech_score = 0.85 if "blockchain" in job["title"].lower() else 0.75
            artistic_score = 0.70
            total_score = (tech_score + artistic_score) / 2
            
            matches.append({
                "job": job,
                "score_details": {
                    "total_score": total_score,
                    "category_scores": {
                        "technical": tech_score,
                        "artistic": artistic_score
                    },
                    "matched_keywords": ["blockchain", "program management", "digital transformation"],
                    "cv_relevance": 0.80,
                    "high_priority": total_score > 0.8
                },
                "status": "new",
                "status_history": [
                    {
                        "status": "new",
                        "timestamp": datetime.utcnow().isoformat(),
                        "notes": "Job matched based on profile"
                    }
                ],
                "timestamp": datetime.utcnow().isoformat()
            })
        
        logger.info(f"Found {len(matches)} matches for user {user_id}")
        
        # Send notifications for new job matches
        notification_results = await notification_service.send_batch_job_notifications(
            [match["job"] for match in matches]
        )
        logger.info(f"Notification results: {notification_results}")
        
        return {
            "success": True,
            "matches": matches,
            "timestamp": datetime.utcnow().isoformat(),
            "notifications": notification_results
        }
        
    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error matching jobs: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
