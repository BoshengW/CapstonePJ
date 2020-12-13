import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { User } from '../model/user';
import { LogIn } from '../model/login';
import { Observable } from 'rxjs';
import { UrlSerializer } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class LoginvalidService {

  constructor(private httpClient: HttpClient) { 

  }

  getloginInfo(user: User): Observable<any>{

    console.log(user.username);
    // params: url; json body; httpOptions
    const _url = 'http://192.168.99.100:5001/loginInfo';
    // return this.httpClient.post<User>(_url, JSON.stringify(userBody));
    return this.httpClient.post<any>(_url, user)
  } 
}
