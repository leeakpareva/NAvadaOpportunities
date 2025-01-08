import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import os
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.slack_email = os.getenv('SLACK_NOTIFICATION_EMAIL', 
            'navadaopportunities-aaaapb3zmuwocgmz3g6s2oq2pm@navadagroup.slack.com')
        
    async def send_pr_notification(self, pr: Dict) -> bool:
        """Send PR notification to Slack channel via email"""
        try:
            message = self.format_pr_notification(pr)
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = os.getenv('SMTP_FROM', 'navada@opportunities.com')
            msg['To'] = self.slack_email
            msg['Subject'] = f"PR Update: {pr.get('title')}"
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(
                    os.getenv('SMTP_USER', ''),
                    os.getenv('SMTP_PASSWORD', '')
                )
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending PR notification: {str(e)}")
            return False
        
    def format_job_notification(self, job: Dict) -> str:
        """Format job details for notification"""
        tech_score = job.get('score_details', {}).get('category_scores', {}).get('technical', 0)
        artistic_score = job.get('score_details', {}).get('category_scores', {}).get('artistic', 0)
        
        return f"""
🔍 New Job Match Found!

🏢 {job.get('title')}
🏪 {job.get('company')}
📍 {job.get('location')}
💼 {job.get('employment_type')}
💰 {self._format_salary(job.get('salary_range', {}))}

Match Scores:
📊 Technical: {tech_score * 100:.1f}%
🎨 Artistic: {artistic_score * 100:.1f}%

📝 Description:
{job.get('description', 'No description available')}

🔗 Apply here: {job.get('url', 'No URL available')}
        """
        
    def format_pr_notification(self, pr: Dict) -> str:
        """Format PR notification"""
        return f"""
🔄 New Pull Request Update!

📦 {pr.get('title')}
👤 Author: {pr.get('author')}
📊 Status: {pr.get('status')}
🔗 URL: {pr.get('url')}

💡 Description:
{pr.get('description', 'No description available')}
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
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = os.getenv('SMTP_USER', 'navada@opportunities.com')
            msg['To'] = self.slack_email
            msg['Subject'] = f"New Job Match: {job.get('title')} at {job.get('company')}"
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(
                    os.getenv('SMTP_USER', ''),
                    os.getenv('SMTP_PASSWORD', '')
                )
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False
            
    async def send_batch_job_notifications(self, jobs: List[Dict]) -> Dict[str, int]:
        """Send notifications for multiple jobs"""
        success_count = 0
        failed_count = 0
        
        # Group jobs into a single email
        all_messages = []
        for job in jobs:
            message = self.format_job_notification(job)
            all_messages.append(message)
            
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = os.getenv('SMTP_USER', 'navada@opportunities.com')
            msg['To'] = self.slack_email
            msg['Subject'] = f"New Job Matches Found ({len(jobs)} positions)"
            
            # Add all job notifications to email body
            body = "\n\n---\n\n".join(all_messages)
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(
                    os.getenv('SMTP_USER', ''),
                    os.getenv('SMTP_PASSWORD', '')
                )
                server.send_message(msg)
                
            success_count = len(jobs)
        except Exception as e:
            print(f"Error sending batch notifications: {str(e)}")
            failed_count = len(jobs)
                
        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(jobs)
        }
