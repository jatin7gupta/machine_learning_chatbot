import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Message} from './models/Message';
import {WebService} from './services/web.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'chatbot-ui';
  messages: Message[];
  chat = false;
  chatForm: FormGroup = new FormGroup({
    message: new FormControl('', [Validators.required]),
  });
  signup: FormGroup = new FormGroup({
    message: new FormControl('', [Validators.required]),
  });
  constructor(private webService: WebService) { }
  ngOnInit(): void {
    this.messages = new Array<Message>();
  }
  request(): void {
    this.messages.push(new Message(this.chatForm.value.message, true));
    this.webService.request(this.chatForm.value.message).subscribe(success => {
      this.messages.push(new Message(success.answer, false));
    }, err => {
      console.log(err);
    });
    this.chatForm.reset();
  }
  signupEvent(): void {
    console.log(this.signup.value.message);
    sessionStorage.setItem('currentUser', this.signup.value.message);
    this.chat = true;
  }
}
