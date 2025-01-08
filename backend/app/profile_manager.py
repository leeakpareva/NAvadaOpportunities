"""
Profile Manager module for handling user profiles and CV data storage.
Provides secure storage and retrieval of user preferences and CV information.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProfileData:
    """Class to represent a user's profile data including CV information"""
    
    def __init__(
        self,
        user_id: str,
        cv_data: Dict[str, List[str]],
        email: Optional[str] = None,
        preferences: Optional[Dict] = None
    ):
        self.user_id = user_id
        self.cv_data = cv_data
        self.email = email
        self.preferences = preferences or {}
        self.last_updated = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert profile data to dictionary format"""
        return {
            "user_id": self.user_id,
            "cv_data": self.cv_data,
            "email": self.email,
            "preferences": self.preferences,
            "last_updated": self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProfileData':
        """Create ProfileData instance from dictionary"""
        return cls(
            user_id=data["user_id"],
            cv_data=data["cv_data"],
            email=data.get("email"),
            preferences=data.get("preferences", {})
        )

class ProfileManager:
    """Manager class for handling profile data storage and retrieval"""
    
    def __init__(self, storage_dir: str = "~/profile_data"):
        self.storage_dir = Path(storage_dir).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.profiles_file = self.storage_dir / "profiles.json"
        self._load_profiles()
    
    def _load_profiles(self) -> None:
        """Load profiles from storage"""
        try:
            if self.profiles_file.exists():
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    self.profiles = json.load(f)
            else:
                self.profiles = {}
        except Exception as e:
            logger.error("Error loading profiles: %s", str(e))
            self.profiles = {}
    
    def _save_profiles(self) -> None:
        """Save profiles to storage"""
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2)
        except Exception as e:
            logger.error("Error saving profiles: %s", str(e))
            raise
    
    def create_or_update_profile(self, profile: ProfileData) -> None:
        """Create or update a user profile"""
        try:
            self.profiles[profile.user_id] = profile.to_dict()
            self._save_profiles()
            logger.info("Profile updated for user %s", profile.user_id)
        except Exception as e:
            logger.error("Error updating profile: %s", str(e))
            raise
    
    def get_profile(self, user_id: str) -> Optional[ProfileData]:
        """Retrieve a user profile"""
        try:
            if user_id in self.profiles:
                return ProfileData.from_dict(self.profiles[user_id])
            return None
        except Exception as e:
            logger.error("Error retrieving profile: %s", str(e))
            return None
    
    def delete_profile(self, user_id: str) -> bool:
        """Delete a user profile"""
        try:
            if user_id in self.profiles:
                del self.profiles[user_id]
                self._save_profiles()
                logger.info("Profile deleted for user %s", user_id)
                return True
            return False
        except Exception as e:
            logger.error("Error deleting profile: %s", str(e))
            return False

if __name__ == "__main__":
    # Example usage
    try:
        # Initialize profile manager
        profile_manager = ProfileManager()
        
        # Create a profile with parsed CV data
        from cv_parser import parse_cv
        cv_path = Path("~/attachments/ed89217a-79ca-439b-8696-4a1ec3409dcb/LESLIE_AKPAREVA_CV.pdf").expanduser()
        cv_data = parse_cv(cv_path)
        
        # Create profile
        profile = ProfileData(
            user_id="leslie_001",
            cv_data=cv_data,
            email="leeakpareva@hotmail.com",
            preferences={
                "job_types": ["remote"],
                "min_salary": 100000,
                "currency": "GBP",
                "notifications": {
                    "email": True,
                    "daily_summary": True
                }
            }
        )
        
        # Save profile
        profile_manager.create_or_update_profile(profile)
        
        # Verify saved data
        saved_profile = profile_manager.get_profile("leslie_001")
        if saved_profile:
            print("\nSaved Profile Data:")
            print("=" * 50)
            print(json.dumps(saved_profile.to_dict(), indent=2))
        
    except Exception as e:
        logger.error("Error in profile manager demo: %s", str(e))
