from typing import Dict, List
import os
import aiohttp
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.channel = os.getenv('SLACK_CHANNEL', 'navadaopportunities')
        if not self.webhook_url:
            logger.warning("Slack webhook URL not configured")
        
    async def send_webhook_notification(self, message: str) -> bool:
        """Send notification to Slack via webhook"""
        if not self.webhook_url:
            logger.error("Slack webhook URL not configured")
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json={"text": message}
                ) as response:
                    if response.status == 200:
                        logger.info("Successfully sent webhook notification")
                        return True
                    else:
                        logger.error(f"Failed to send webhook notification: {await response.text()}")
                        return False
        except Exception as e:
            logger.error(f"Error sending webhook notification: {str(e)}")
            return False
    async def send_pr_notification(self, pr: Dict) -> bool:
        """Send PR notification to Slack channel via webhook"""
        try:
            message = self.format_pr_notification(pr)
            return await self.send_webhook_notification(message)
        except Exception as e:
            logger.error(f"Error sending PR notification: {str(e)}")
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
        """Send job notification to Slack channel via webhook"""
        try:
            message = self.format_job_notification(job)
            return await self.send_webhook_notification(message)
        except Exception as e:
            logger.error(f"Error sending job notification: {str(e)}")
            return False
            
    async def send_batch_job_notifications(self, jobs: List[Dict]) -> Dict[str, int]:
        """Send notifications for multiple jobs via webhook"""
        success_count = 0
        failed_count = 0
        
        try:
            # Group jobs into blocks of 5 to avoid message length limits
            for i in range(0, len(jobs), 5):
                job_batch = jobs[i:i+5]
                messages = []
                for job in job_batch:
                    message = self.format_job_notification(job)
                    messages.append(message)
                
                batch_message = f"🔍 New Job Matches Found ({len(job_batch)} positions)\n\n" + \
                              "\n\n---\n\n".join(messages)
                
                if await self.send_webhook_notification(batch_message):
                    success_count += len(job_batch)
                    logger.info(f"Successfully sent notifications for {len(job_batch)} jobs")
                else:
                    failed_count += len(job_batch)
                    logger.error("Failed to send batch notifications")
                            
        except Exception as e:
            logger.error(f"Error sending batch notifications: {str(e)}")
            failed_count = len(jobs) - success_count
                
        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(jobs)
        }
