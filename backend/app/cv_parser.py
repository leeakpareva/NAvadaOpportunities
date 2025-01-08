"""
CV Parser module for extracting structured data from CV documents.
Supports PDF and DOCX formats with section-based parsing.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import docx
import PyPDF2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CVParseError(Exception):
    """Custom exception for CV parsing errors"""

class CVParser:
    """Parser for extracting structured data from CV documents"""
    SECTION_KEYWORDS = {
        'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
        'experience': ['experience', 'work experience', 'employment history', 'work history'],
        'education': ['education', 'academic background', 'qualifications', 'academic qualifications'],
        'projects': ['projects', 'personal projects', 'portfolio'],
        'certifications': ['certifications', 'certificates', 'professional certifications']
    }
    
    def __init__(self):
        self.current_section = None
        self.parsed_data = {
            'skills': [],
            'experience': [],
            'education': [],
            'projects': [],
            'certifications': [],
            'raw_text': []
        }
    
    def _detect_section(self, text: str) -> Optional[str]:
        """Detect which section a text belongs to based on keywords"""
        text_lower = text.lower().strip()
        for section, keywords in self.SECTION_KEYWORDS.items():
            if any(keyword == text_lower for keyword in keywords):
                return section
        return None
    
    def _parse_docx(self, file_path: Path) -> None:
        """Parse DOCX file and extract structured data"""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue
                self.parsed_data['raw_text'].append(text)
                # Check if this is a section header
                section = self._detect_section(text)
                if section:
                    self.current_section = section
                    continue
                # Add content to current section if we're in one
                if self.current_section and text:
                    self.parsed_data[self.current_section].append(text)
        except Exception as e:
            raise CVParseError(f"Error parsing DOCX file: {str(e)}") from e
    
    def _parse_pdf(self, file_path: Path) -> None:
        """Parse PDF file and extract structured data"""
        try:
            with open(file_path, 'rb', encoding=None) as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if not text:
                        continue
                    # Split text into lines and process each line
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        self.parsed_data['raw_text'].append(line)
                        # Check if this is a section header
                        section = self._detect_section(line)
                        if section:
                            self.current_section = section
                            continue
                        # Add content to current section if we're in one
                        if self.current_section and line:
                            self.parsed_data[self.current_section].append(line)
        except Exception as e:
            raise CVParseError(f"Error parsing PDF file: {str(e)}") from e
    
    def parse_cv(self, file_path: Union[str, Path]) -> Dict[str, List[str]]:
        """
        Parse a CV file (PDF or DOCX) and return structured data
        
        Args:
            file_path: Path to the CV file
            
        Returns:
            Dictionary containing structured CV data
            
        Raises:
            CVParseError: If there's an error parsing the CV
        """
        try:
            file_path = Path(file_path).expanduser()
            if not file_path.exists():
                raise CVParseError(f"File not found: {file_path}")
            
            # Reset parsed data
            self.current_section = None
            self.parsed_data = {
                'skills': [],
                'experience': [],
                'education': [],
                'projects': [],
                'certifications': [],
                'raw_text': []
            }
            
            logger.info("Parsing CV file: %s", file_path)
            
            if file_path.suffix.lower() == '.docx':
                self._parse_docx(file_path)
            elif file_path.suffix.lower() == '.pdf':
                self._parse_pdf(file_path)
            else:
                raise CVParseError("Unsupported file format: %s" % file_path.suffix)
            
            logger.info("Successfully parsed CV")
            return self.parsed_data
            
        except CVParseError:
            raise
        except Exception as e:
            raise CVParseError(f"Unexpected error parsing CV: {str(e)}") from e

def parse_cv(file_path: Union[str, Path]) -> Dict[str, List[str]]:
    """Convenience function to parse a CV file"""
    parser = CVParser()
    return parser.parse_cv(file_path)

if __name__ == "__main__":
    try:
        # Example usage
        cv_path = Path("~/attachments/ed89217a-79ca-439b-8696-4a1ec3409dcb/LESLIE_AKPAREVA_CV.pdf").expanduser()
        result = parse_cv(cv_path)
        
        # Print structured data
        print("\nParsed CV Data:")
        print("=" * 50)
        print(json.dumps(result, indent=2))
        
    except CVParseError as e:
        logger.error("Failed to parse CV: %s", str(e))
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
