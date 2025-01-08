import { DefineWorkflow, Schema } from "deno-slack-sdk/mod.ts";

/**
 * Workflow definition for job notifications
 * This workflow handles formatting and sending job notifications to Slack
 */
const JobNotificationWorkflow = DefineWorkflow({
  callback_id: "job_notification",
  title: "Job Notification Workflow",
  description: "Sends formatted job notifications to Slack",
  input_parameters: {
    properties: {
      channel: {
        type: Schema.slack.types.channel_id,
        description: "The channel to send the notification to",
      },
      message: {
        type: Schema.types.string,
        description: "The notification message",
      },
      jobTitle: {
        type: Schema.types.string,
        description: "Job title",
      },
      company: {
        type: Schema.types.string,
        description: "Company name",
      },
      location: {
        type: Schema.types.string,
        description: "Job location",
      },
      employmentType: {
        type: Schema.types.string,
        description: "Type of employment",
      },
      description: {
        type: Schema.types.string,
        description: "Job description",
      },
      url: {
        type: Schema.types.string,
        description: "Job posting URL",
      },
    },
    required: ["channel", "jobTitle", "company"],
  },
});

// Format and send the job notification
JobNotificationWorkflow.addStep(Schema.slack.functions.SendMessage, {
  channel_id: JobNotificationWorkflow.inputs.channel,
  message: `🔍 *New Job Opportunity*\n\n` +
           `🏢 *${JobNotificationWorkflow.inputs.jobTitle}*\n` +
           `🏪 ${JobNotificationWorkflow.inputs.company}\n` +
           `📍 ${JobNotificationWorkflow.inputs.location}\n` +
           `💼 ${JobNotificationWorkflow.inputs.employmentType}\n\n` +
           `📝 *Description:*\n${JobNotificationWorkflow.inputs.description}\n\n` +
           `🔗 *Apply here:* ${JobNotificationWorkflow.inputs.url}`,
});

export default JobNotificationWorkflow;
