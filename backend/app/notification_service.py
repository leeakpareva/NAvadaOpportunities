import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import os
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.slack_email = "navadaopportunities-aaaapb3zmuwocgmz3g6s2oq2pm@navadagroup.slack.com"
        
    def format_job_notification(self, job: Dict) -> str:
        """Format job details for notification"""
        return f"""
New Job Match Found!

Title: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Type: {job.get('employment_type')}
Salary Range: {self._format_salary(job.get('salary_range', {}))}

Description:
{job.get('description', 'No description available')}

Apply here: {job.get('url', 'No URL available')}
        """
        
    def _format_salary(self, salary_range: Dict) -> str:
        """Format salary range for display"""
        min_salary = salary_range.get('min', 'Not specified')
        max_salary = salary_range.get('max', 'Not specified')
        if min_salary == 'Not specified' and max_salary == 'Not specified':
            return 'Salary not specified'
        elif max_salary == 'Not specified':
            return f'£{min_salary:,}+'
        else:
            return f'£{min_salary:,} - £{max_salary:,}'
            
    async def send_job_notification(self, job: Dict) -> bool:
        """Send job notification to Slack channel via email"""
        try:
            message = self.format_job_notification(job)
            
            # For now, just print the notification (we'll implement actual email sending later)
            print(f"Would send notification to {self.slack_email}:")
            print(message)
            
            return True
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False
            
    async def send_batch_job_notifications(self, jobs: List[Dict]) -> Dict[str, int]:
        """Send notifications for multiple jobs"""
        success_count = 0
        failed_count = 0
        
        for job in jobs:
            success = await self.send_job_notification(job)
            if success:
                success_count += 1
            else:
                failed_count += 1
                
        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(jobs)
        }
