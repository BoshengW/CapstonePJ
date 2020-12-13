import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders} from '@angular/common/http';
import { User } from '../model/user'; 


@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  constructor(private httpClient: HttpClient) { }

  submitUserForm(newUser: User) {
    const _url = "http://192.168.99.100:5001/register";
    console.log(newUser);

    return this.httpClient.post(_url, newUser, {observe: 'response' as 'response'});
  }
}
