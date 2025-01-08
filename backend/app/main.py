from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, List
import json
from datetime import datetime

from app.cv_parser import parse_cv
from app.job_matcher import JobMatcher
from app.profile_manager import ProfileManager, ProfileData

app = FastAPI(title="NAVADA Job Finder API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
profile_manager = ProfileManager()

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
        profile = ProfileData(
            user_id=profile_data["user_id"],
            cv_data=profile_data["cv_data"],
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

@app.get("/api/jobs/match/{user_id}")
async def match_jobs(
    user_id: str,
    remote_only: bool = True,
    min_salary: int = 100000,
    employment_types: Optional[List[str]] = None
):
    """
    Match jobs for user based on their profile
    
    Args:
        user_id: User's unique identifier
        remote_only: Filter for remote positions only
        min_salary: Minimum salary requirement (default: 100000)
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
        
        # Process and match jobs
        matches = []
        for job in response.data:
            # Check salary requirement
            salary_range = job.get('salary_range', {})
            min_job_salary = salary_range.get('min', 0)
            if min_job_salary < min_salary:
                continue
            
            # Check employment type
            if employment_types:
                job_type = job.get('employment_type', '').lower()
                if not any(type.lower() in job_type for type in employment_types):
                    continue
            
            # Match job using tech-artistic scoring
            match = matcher.match_job(job)
            if match:
                matches.append(match)
        
        logger.info(f"Found {len(matches)} matches for user {user_id}")
        return {
            "success": True,
            "matches": matches,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error matching jobs: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
