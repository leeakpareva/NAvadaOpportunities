import { IncomingWebhook } from '@slack/webhook';

export interface WebhookPayload {
  channel_id?: string;
  job_title: string;
  company: string;
  location: string;
  employment_type: string;
  description: string;
  url: string;
}

export class WebhookTrigger {
  private webhook: IncomingWebhook;
  private defaultChannel: string;

  constructor(webhookUrl: string, defaultChannel: string = 'navadaopportunities') {
    this.webhook = new IncomingWebhook(webhookUrl);
    this.defaultChannel = defaultChannel;
  }

  async trigger(payload: WebhookPayload): Promise<boolean> {
    try {
      const message = {
        channel: payload.channel_id || this.defaultChannel,
        blocks: [
          {
            type: "header",
            text: {
              type: "plain_text",
              text: "🔍 New Job Opportunity",
              emoji: true
            }
          },
          {
            type: "section",
            fields: [
              {
                type: "mrkdwn",
                text: `*Position:*\n${payload.job_title}`
              },
              {
                type: "mrkdwn",
                text: `*Company:*\n${payload.company}`
              }
            ]
          },
          {
            type: "section",
            fields: [
              {
                type: "mrkdwn",
                text: `*Location:*\n${payload.location}`
              },
              {
                type: "mrkdwn",
                text: `*Type:*\n${payload.employment_type}`
              }
            ]
          },
          {
            type: "section",
            text: {
              type: "mrkdwn",
              text: `*Description:*\n${payload.description}`
            }
          },
          {
            type: "actions",
            elements: [
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "View Job",
                  emoji: true
                },
                url: payload.url,
                style: "primary"
              }
            ]
          }
        ]
      };

      await this.webhook.send(message);
      return true;
    } catch (error) {
      console.error('Error triggering webhook:', error);
      return false;
    }
  }
}

export const createWebhookTrigger = (webhookUrl: string, defaultChannel?: string) => {
  return new WebhookTrigger(webhookUrl, defaultChannel);
};
