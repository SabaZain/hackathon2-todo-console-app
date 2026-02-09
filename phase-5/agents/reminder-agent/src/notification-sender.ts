import { ReminderChannel } from '@prisma/client';
import nodemailer from 'nodemailer';
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
  ],
});

export class NotificationSender {
  private emailTransporter: nodemailer.Transporter;

  constructor() {
    // Configure email transporter
    this.emailTransporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'localhost',
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS,
      },
    });
  }

  async send(
    channel: ReminderChannel,
    user: any,
    task: any,
    reminder: any
  ): Promise<void> {
    switch (channel) {
      case ReminderChannel.EMAIL:
        await this.sendEmail(user, task, reminder);
        break;
      case ReminderChannel.PUSH:
        await this.sendPushNotification(user, task, reminder);
        break;
      case ReminderChannel.IN_APP:
        await this.sendInAppNotification(user, task, reminder);
        break;
      default:
        throw new Error(`Unknown notification channel: ${channel}`);
    }
  }

  private async sendEmail(user: any, task: any, reminder: any): Promise<void> {
    try {
      const mailOptions = {
        from: process.env.SMTP_FROM || 'noreply@phase5.com',
        to: user.email,
        subject: `Reminder: ${task.title}`,
        html: this.generateEmailTemplate(user, task, reminder),
      };

      await this.emailTransporter.sendMail(mailOptions);

      logger.info('Email notification sent:', {
        userId: user.id,
        taskId: task.id,
        reminderId: reminder.id,
        email: user.email,
      });
    } catch (error) {
      logger.error('Failed to send email notification:', error);
      throw error;
    }
  }

  private generateEmailTemplate(user: any, task: any, reminder: any): string {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background-color: #4F46E5; color: white; padding: 20px; text-align: center; }
          .content { background-color: #f9f9f9; padding: 20px; margin-top: 20px; }
          .task-title { font-size: 20px; font-weight: bold; margin-bottom: 10px; }
          .task-details { margin: 15px 0; }
          .priority { display: inline-block; padding: 5px 10px; border-radius: 4px; font-size: 12px; }
          .priority-high { background-color: #EF4444; color: white; }
          .priority-medium { background-color: #F59E0B; color: white; }
          .priority-low { background-color: #10B981; color: white; }
          .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Task Reminder</h1>
          </div>
          <div class="content">
            <p>Hi ${user.name},</p>
            <p>This is a reminder for your task:</p>
            <div class="task-details">
              <div class="task-title">${task.title}</div>
              ${task.description ? `<p>${task.description}</p>` : ''}
              <p>
                <strong>Priority:</strong>
                <span class="priority priority-${task.priority.toLowerCase()}">${task.priority}</span>
              </p>
              ${task.dueDate ? `<p><strong>Due Date:</strong> ${new Date(task.dueDate).toLocaleString()}</p>` : ''}
              ${task.tags && task.tags.length > 0 ? `<p><strong>Tags:</strong> ${task.tags.join(', ')}</p>` : ''}
            </div>
            <p>Don't forget to complete this task!</p>
          </div>
          <div class="footer">
            <p>This is an automated reminder from Phase 5 Task Management System</p>
          </div>
        </div>
      </body>
      </html>
    `;
  }

  private async sendPushNotification(user: any, task: any, reminder: any): Promise<void> {
    try {
      // In a real implementation, this would use a push notification service
      // like Firebase Cloud Messaging (FCM), Apple Push Notification Service (APNS),
      // or a service like OneSignal, Pusher, etc.

      const notification = {
        title: 'Task Reminder',
        body: task.title,
        data: {
          taskId: task.id,
          reminderId: reminder.id,
          type: 'reminder',
        },
      };

      // Placeholder for actual push notification implementation
      logger.info('Push notification would be sent:', {
        userId: user.id,
        taskId: task.id,
        reminderId: reminder.id,
        notification,
      });

      // TODO: Integrate with actual push notification service
      // Example with FCM:
      // await admin.messaging().send({
      //   token: user.fcmToken,
      //   notification: {
      //     title: notification.title,
      //     body: notification.body,
      //   },
      //   data: notification.data,
      // });

      logger.info('Push notification sent (simulated):', {
        userId: user.id,
        taskId: task.id,
        reminderId: reminder.id,
      });
    } catch (error) {
      logger.error('Failed to send push notification:', error);
      throw error;
    }
  }

  private async sendInAppNotification(user: any, task: any, reminder: any): Promise<void> {
    try {
      // In-app notifications would typically be stored in a database
      // and displayed when the user is active in the application
      // This could also publish to a WebSocket for real-time delivery

      const notification = {
        userId: user.id,
        type: 'reminder',
        title: 'Task Reminder',
        message: `Don't forget: ${task.title}`,
        taskId: task.id,
        reminderId: reminder.id,
        createdAt: new Date(),
        read: false,
      };

      // Placeholder for actual in-app notification storage
      logger.info('In-app notification would be created:', {
        userId: user.id,
        taskId: task.id,
        reminderId: reminder.id,
        notification,
      });

      // TODO: Store in database and/or publish via WebSocket
      // Example:
      // await prisma.notification.create({ data: notification });
      // await webSocketService.sendToUser(user.id, notification);

      logger.info('In-app notification sent (simulated):', {
        userId: user.id,
        taskId: task.id,
        reminderId: reminder.id,
      });
    } catch (error) {
      logger.error('Failed to send in-app notification:', error);
      throw error;
    }
  }
}
