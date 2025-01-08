"""
Job Matcher module for scoring and matching jobs based on tech-artistic criteria.
Implements CV-based scoring and compliance-focused job matching.
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TechArtisticScorer:
    """Scores jobs based on tech and artistic criteria, including CV data"""
    
    TECH_CATEGORIES = {
        'digital_art': ['digital art', 'creative technology', 'digital design', '3d modeling', 'animation'],
        'ai_creative_tools': ['ai', 'machine learning', 'creative ai', 'generative ai', 'computer vision'],
        'blockchain_creative': ['blockchain', 'web3', 'nft', 'smart contract', 'defi'],
        'digital_assistance': ['automation', 'digital transformation', 'process optimization', 'workflow'],
        'tech_innovation': ['innovation', 'emerging technology', 'digital strategy', 'technology leadership']
    }
    
    def __init__(self, cv_data: Dict[str, List[str]]):
        self.cv_data = cv_data
        self._process_cv_data()
    
    def _process_cv_data(self) -> None:
        """
        Process CV data to extract relevant keywords and experience.
        Initializes cv_keywords set with processed terms from skills,
        experience, and certifications sections.
        """
        self.cv_keywords = set()
        # Extract keywords from skills
        for skill in self.cv_data.get('skills', []):
            self.cv_keywords.update(skill.lower().split())
        
        # Extract keywords from experience
        for exp in self.cv_data.get('experience', []):
            self.cv_keywords.update(exp.lower().split())
        
        # Extract keywords from certifications
        for cert in self.cv_data.get('certifications', []):
            self.cv_keywords.update(cert.lower().split())
    
    def _score_category(self, job_description: str, category: str, keywords: List[str]) -> int:
        """Score a job for a specific category"""
        description_lower = job_description.lower()
        
        # Base score from job description
        base_score = sum(1 for keyword in keywords if keyword in description_lower)
        
        # Bonus points for CV matches
        cv_bonus = sum(1 for keyword in keywords 
                      if keyword in self.cv_keywords and keyword in description_lower)
        
        # Category-specific scoring rules
        if category == 'tech_innovation' and any(cert for cert in self.cv_data.get('certifications', [])
                                               if 'innovation' in cert.lower()):
            cv_bonus += 2
            
        if category == 'blockchain_creative' and any(cert for cert in self.cv_data.get('certifications', [])
                                                   if 'blockchain' in cert.lower()):
            cv_bonus += 2
        
        return min(4, base_score + cv_bonus)  # Cap at 4 points per category
    
    def score_job(self, job: Dict) -> Dict:
        """
        Score a job based on tech-artistic criteria and CV match
        
        Returns:
            Dict containing score details and matched categories
        """
        description = f"{job.get('title', '')} {job.get('description', '')}"
        scores = {}
        matched_keywords = set()
        
        # Score each category
        for category, keywords in self.TECH_CATEGORIES.items():
            score = self._score_category(description, category, keywords)
            if score > 0:
                scores[category] = score
                matched_keywords.update(kw for kw in keywords if kw in description.lower())
        
        # Calculate total score
        total_score = sum(scores.values())
        
        # Add CV-specific bonus points
        cv_relevance = self._calculate_cv_relevance(description)
        total_score += cv_relevance
        
        return {
            'total_score': total_score,
            'category_scores': scores,
            'matched_keywords': list(matched_keywords),
            'cv_relevance': cv_relevance,
            'high_priority': total_score >= 15
        }
    
    def _calculate_cv_relevance(self, job_description: str) -> int:
        """Calculate how relevant a job is based on CV content"""
        description_lower = job_description.lower()
        relevance_score = 0
        
        # Check skills matches
        skill_matches = sum(1 for skill in self.cv_data.get('skills', [])
                          if skill.lower() in description_lower)
        relevance_score += min(3, skill_matches)
        
        # Check certification relevance
        cert_matches = sum(1 for cert in self.cv_data.get('certifications', [])
                         if any(word.lower() in description_lower 
                               for word in cert.split() if len(word) > 3))
        relevance_score += min(2, cert_matches)
        
        # Check experience relevance
        exp_matches = sum(1 for exp in self.cv_data.get('experience', [])
                        if any(word.lower() in description_lower 
                              for word in exp.split() if len(word) > 3))
        relevance_score += min(3, exp_matches)
        
        return relevance_score

class JobMatcher:
    """Matches jobs with user profiles using tech-artistic scoring and tracks application status"""
    
    # Valid job application status options
    STATUS_OPTIONS = [
        'new',              # Just matched/found
        'reviewing',        # Under consideration
        'applied',          # Application submitted
        'interview_scheduled',  # Interview process
        'offer_received',   # Received job offer
        'rejected'         # Application rejected
    ]
    
    def __init__(self, profile_data: Dict):
        self.profile = profile_data
        self.scorer = TechArtisticScorer(profile_data['cv_data'])
        self.preferences = profile_data.get('preferences', {})
    
    def _meets_basic_criteria(self, job: Dict) -> bool:
        """
        Check if job meets basic criteria (salary, location, etc.)
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            bool: True if job meets criteria, False otherwise
        """
        min_salary = self.preferences.get('min_salary', 0)
        currency = self.preferences.get('currency', 'GBP')
        job_types = self.preferences.get('job_types', [])
        
        # Salary check
        if 'salary' in job:
            if isinstance(job['salary'], (int, float)):
                if job['salary'] < min_salary:
                    return False
            elif isinstance(job['salary'], str):
                # Try to extract numeric salary from string
                import re
                salary_numbers = re.findall(r'\d+', job['salary'])
                if salary_numbers and int(salary_numbers[0]) < min_salary:
                    return False
        
        # Remote work check
        if 'remote' in job_types:
            location = job.get('location', '').lower()
            if not any(term in location for term in ['remote', 'work from home', 'wfh']):
                return False
        
        return True
    
    def match_job(self, job: Dict, current_status: str = 'new') -> Optional[Dict]:
        """
        Match a job with the user profile and track application status
        
        Args:
            job: Job listing data
            current_status: Current application status (default: 'new')
            
        Returns:
            Dict with match details if job is suitable, None otherwise
        """
        if current_status not in self.STATUS_OPTIONS:
            raise ValueError("Invalid status. Must be one of: %s" % ', '.join(self.STATUS_OPTIONS))
        if not self._meets_basic_criteria(job):
            return None
        
        # Score the job
        score_details = self.scorer.score_job(job)
        
        # Only return matches that meet minimum score threshold
        if score_details['total_score'] >= 8:  # Minimum threshold for matches
            return {
                'job': job,
                'score_details': score_details,
                'status': current_status,
                'status_history': [{
                    'status': current_status,
                    'timestamp': datetime.utcnow().isoformat(),
                    'notes': None
                }],
                'timestamp': datetime.utcnow().isoformat()
            }
        
        return None

    def update_job_status(self, job_id: str, new_status: str, notes: Optional[str] = None) -> Dict:
        """
        Update the status of a job application
        
        Args:
            job_id: Unique identifier for the job
            new_status: New status to set
            notes: Optional notes about the status change
            
        Returns:
            Updated job match data
        """
        if new_status not in self.STATUS_OPTIONS:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(self.STATUS_OPTIONS)}")
        
        # In a real implementation, this would update a database
        # For now, we'll just return the updated structure
        return {
            'job_id': job_id,
            'status': new_status,
            'status_update': {
                'status': new_status,
                'timestamp': datetime.utcnow().isoformat(),
                'notes': notes
            }
        }

if __name__ == "__main__":
    try:
        # Load profile data
        from profile_manager import ProfileManager
        profile_manager = ProfileManager()
        profile = profile_manager.get_profile("leslie_001")
        
        if not profile:
            raise ValueError("Profile not found")
        
        # Initialize job matcher
        matcher = JobMatcher(profile.to_dict())
        
        # Test with sample jobs
        test_jobs = [
            {
                'id': 'job1',
                'title': 'Blockchain Program Manager',
                'company': 'Tech Corp',
                'location': 'Remote',
                'salary': '120000',
                'description': 'Leading blockchain initiatives and digital transformation projects...'
            },
            {
                'id': 'job2',
                'title': 'Digital Art Director',
                'company': 'Creative Studio',
                'location': 'London (Remote Available)',
                'salary': '95000',
                'description': 'Managing digital art projects and creative technology initiatives...'
            }
        ]
        
        print("\nJob Matching Results:")
        print("=" * 50)
        
        # Test status tracking
        print("\nTesting Status Updates:")
        print("=" * 50)
        
        for job in test_jobs:
            result = matcher.match_job(job)
            if result:
                print("\nJob: %s" % job['title'])
                print("Score: %d" % result['score_details']['total_score'])
                print("Categories: %s" % result['score_details']['category_scores'])
                print("CV Relevance: %d" % result['score_details']['cv_relevance'])
                print("Keywords: %s" % ', '.join(result['score_details']['matched_keywords']))
                print("High Priority: %s" % result['score_details']['high_priority'])
                print("Status: %s" % result['status'])
                print("-" * 30)
                
                # Test status update
                if result['score_details']['high_priority']:
                    status_update = matcher.update_job_status(
                        job_id=job['id'],
                        new_status='reviewing',
                        notes='High priority match based on CV and tech-artistic score'
                    )
                    print(f"\nStatus Update for {job['title']}:")
                    print(f"New Status: {status_update['status']}")
                    print(f"Notes: {status_update['status_update']['notes']}")
                    print("-" * 30)
        
    except Exception as e:
        logger.error("Error in job matcher demo: %s", str(e))
