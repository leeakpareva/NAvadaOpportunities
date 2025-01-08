import { WebhookTrigger } from '../triggers/webhook.trigger';

export interface JobNotification {
  channel_id?: string;
  job_title: string;
  company: string;
  location: string;
  employment_type: string;
  description: string;
  url: string;
}

export class JobNotificationWorkflow {
  private webhookTrigger: WebhookTrigger;

  constructor(webhookUrl: string, defaultChannel: string = 'navadaopportunities') {
    this.webhookTrigger = new WebhookTrigger(webhookUrl, defaultChannel);
  }

  async notify(notification: JobNotification): Promise<boolean> {
    try {
      return await this.webhookTrigger.trigger({
        channel_id: notification.channel_id,
        job_title: notification.job_title,
        company: notification.company,
        location: notification.location,
        employment_type: notification.employment_type,
        description: notification.description,
        url: notification.url
      });
    } catch (error) {
      console.error('Error sending job notification:', error);
      return false;
    }
  }
}
