from typing import Dict, List, Optional
import os
import aiohttp
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.client_id = os.getenv('SLACK_CLIENT_ID')
        self.client_secret = os.getenv('SLACK_CLIENT_SECRET')
        self.channel = os.getenv('SLACK_CHANNEL', 'navadaopportunities')
        self.access_token = None
        
    async def authenticate(self):
        """Authenticate with Slack using OAuth"""
        if not self.client_id or not self.client_secret:
            raise ValueError("Slack client credentials not configured")
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://slack.com/api/oauth.v2.access',
                    data={
                        'client_id': self.client_id,
                        'client_secret': self.client_secret,
                        'grant_type': 'client_credentials'
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.access_token = data.get('access_token')
                        if not self.access_token:
                            raise ValueError("No access token in response")
                        logger.info("Successfully authenticated with Slack")
                    else:
                        raise ValueError(f"Authentication failed: {await response.text()}")
        except Exception as e:
            logger.error(f"Slack authentication error: {str(e)}")
            raise
    async def send_pr_notification(self, pr: Dict) -> bool:
        """Send PR notification to Slack channel via OAuth API"""
        try:
            if not self.access_token:
                await self.authenticate()
                
            message = self.format_pr_notification(pr)
            
            payload = {
                "channel": self.channel,
                "text": message,
                "username": "NAVADA Bot",
                "icon_emoji": ":robot_face:"
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://slack.com/api/chat.postMessage',
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('ok'):
                            logger.info(f"Successfully sent PR notification for {pr.get('title')}")
                            return True
                        else:
                            logger.error(f"Slack API error: {data.get('error')}")
                            return False
                    else:
                        logger.error(f"Failed to send PR notification: {await response.text()}")
                        return False
                        
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
        """Send job notification to Slack channel via OAuth API"""
        try:
            if not self.access_token:
                await self.authenticate()
                
            message = self.format_job_notification(job)
            
            payload = {
                "channel": self.channel,
                "text": message,
                "username": "NAVADA Job Finder",
                "icon_emoji": ":briefcase:"
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://slack.com/api/chat.postMessage',
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('ok'):
                            logger.info(f"Successfully sent job notification for {job.get('title')}")
                            return True
                        else:
                            logger.error(f"Slack API error: {data.get('error')}")
                            return False
                    else:
                        logger.error(f"Failed to send job notification: {await response.text()}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending job notification: {str(e)}")
            return False
            
    async def send_batch_job_notifications(self, jobs: List[Dict]) -> Dict[str, int]:
        """Send notifications for multiple jobs via OAuth API"""
        success_count = 0
        failed_count = 0
        
        try:
            if not self.access_token:
                await self.authenticate()
                
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Group jobs into blocks of 5 to avoid message length limits
            for i in range(0, len(jobs), 5):
                job_batch = jobs[i:i+5]
                messages = []
                for job in job_batch:
                    message = self.format_job_notification(job)
                    messages.append(message)
                
                payload = {
                    "channel": self.channel,
                    "text": f"🔍 New Job Matches Found ({len(job_batch)} positions)\n\n" + 
                           "\n\n---\n\n".join(messages),
                    "username": "NAVADA Job Finder",
                    "icon_emoji": ":briefcase:"
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        'https://slack.com/api/chat.postMessage',
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get('ok'):
                                success_count += len(job_batch)
                                logger.info(f"Successfully sent notifications for {len(job_batch)} jobs")
                            else:
                                failed_count += len(job_batch)
                                logger.error(f"Slack API error: {data.get('error')}")
                        else:
                            failed_count += len(job_batch)
                            logger.error(f"Failed to send notifications: {await response.text()}")
                            
        except Exception as e:
            logger.error(f"Error sending batch notifications: {str(e)}")
            failed_count = len(jobs) - success_count
                
        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(jobs)
        }
