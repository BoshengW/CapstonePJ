import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders} from '@angular/common/http';
import { User } from '../model/user'; 


@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  server_url = "http://127.0.0.1:5000/";

  constructor(private httpClient: HttpClient) { }

  submitUserForm(newUser: User) {
    const _url = this.server_url + "register";
    console.log(newUser);

    return this.httpClient.post(_url, newUser, {observe: 'response' as 'response'});
  }
}
