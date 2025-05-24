export interface NotificationPayload {
  chat_id: string;
  text: string;
  parse_mode?: 'Markdown' | 'HTML';
  disable_notification?: boolean;
}

export interface TelegramResponse {
  ok: boolean;
  result: {
    message_id: number;
    date: number;
    text: string;
  };
}
