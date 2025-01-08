import { IncomingWebhook } from '@slack/webhook';

/**
 * Slack webhook notification handler for NAVADA job notifications
 */
export class JobNotificationHandler {
  private webhook: IncomingWebhook;

  constructor(webhookUrl: string) {
    this.webhook = new IncomingWebhook(webhookUrl);
  }

  /**
   * Send a job notification to Slack
   */
  async sendJobNotification(jobData: {
    title: string;
    company: string;
    location: string;
    employmentType: string;
    description: string;
    url: string;
  }) {
    const message = {
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
              text: `*Position:*\n${jobData.title}`
            },
            {
              type: "mrkdwn",
              text: `*Company:*\n${jobData.company}`
            }
          ]
        },
        {
          type: "section",
          fields: [
            {
              type: "mrkdwn",
              text: `*Location:*\n${jobData.location}`
            },
            {
              type: "mrkdwn",
              text: `*Type:*\n${jobData.employmentType}`
            }
          ]
        },
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*Description:*\n${jobData.description}`
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
              url: jobData.url,
              style: "primary"
            }
          ]
        }
      ]
    };

    try {
      await this.webhook.send(message);
      return true;
    } catch (error) {
      console.error('Error sending job notification:', error);
      return false;
    }
  }

  /**
   * Send a PR notification to Slack
   */
  async sendPRNotification(prData: {
    title: string;
    author: string;
    status: string;
    url: string;
    description: string;
  }) {
    const message = {
      blocks: [
        {
          type: "header",
          text: {
            type: "plain_text",
            text: "🔄 Pull Request Update",
            emoji: true
          }
        },
        {
          type: "section",
          fields: [
            {
              type: "mrkdwn",
              text: `*Title:*\n${prData.title}`
            },
            {
              type: "mrkdwn",
              text: `*Author:*\n${prData.author}`
            }
          ]
        },
        {
          type: "section",
          fields: [
            {
              type: "mrkdwn",
              text: `*Status:*\n${prData.status}`
            }
          ]
        },
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*Description:*\n${prData.description}`
          }
        },
        {
          type: "actions",
          elements: [
            {
              type: "button",
              text: {
                type: "plain_text",
                text: "View PR",
                emoji: true
              },
              url: prData.url,
              style: "primary"
            }
          ]
        }
      ]
    };

    try {
      await this.webhook.send(message);
      return true;
    } catch (error) {
      console.error('Error sending PR notification:', error);
      return false;
    }
  }
}

export const createNotificationHandler = (webhookUrl: string) => {
  return new JobNotificationHandler(webhookUrl);
};
