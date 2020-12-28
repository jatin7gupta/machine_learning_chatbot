import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class WebService {
  API_URL =  'http://127.0.0.1:5000/v1/';
  constructor(private http: HttpClient) { }
  request(message: string): Observable<any> {
    console.log(message);
    const chatURL = this.API_URL + 'chat';
    const messageParam = {
      expression: message,
      user: sessionStorage.getItem('currentUser')
    };
    return this.http.get(chatURL, {params: messageParam});
  }
}
