export class Message {
  message: string;
  request: boolean;
  constructor(message: string, request: boolean) {
    this.message = message;
    this.request = request;
  }
}
