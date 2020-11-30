import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { LoginvalidService } from '../services/loginvalid.service';
import { User } from '../model/user';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { delay } from 'rxjs/internal/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  userloginForm: any = {};

  username = "";
  password = "";
  userModel = new User("","","");
  loginFlag = false;
  userInputFlag = false;
  userFromDB: any = {};

  constructor(private httpClient: HttpClient, private _login: LoginvalidService,
    private router: Router) { }

  ngOnInit() {

    // this._login.getloginInfo(this.userModel).subscribe(data => {
    //   this.userFromDB = data;
    //   console.log('load response: ' + this.userFromDB);
    // })

    
    
  }

  login(userLogin: NgForm) {

    this.userModel.username = userLogin.value.username;
    this.userModel.password = userLogin.value.password;
    console.log(this.userModel.username);
    console.log(this.userModel.password);

    this._login.getloginInfo(this.userModel).subscribe(
      data => {
        this.username = data.username;
        this.password = data.password;  
        // since subscribe operation is async, rather than out side function is sync. need to run related function inside subscribe.
        this.validate(this.username, this.password);
    }
      )
    
    // this.validate(this.username, this.password);
    
  
  }

  validate(username:string, password: string) {
      // there is a bug here, if username & password not match, cannot fetch data from MongoDB, in this case frontend will have error.
      // console.log(username);
      if(username==null || password==null) {
        this.loginFlag = false;
        this.userInputFlag = true;
      } else if(this.userModel.username==this.username && this.userModel.password==this.password) {

        console.log(this.username);
        console.log(this.password);
        // login and UserInput successfully
        this.loginFlag = true;
        this.userInputFlag = true;
        this.router.navigate(['home']);
        this.loginFlag = false;
  
  
      } else {
  
        // User input successfully, but login not match with database
        this.loginFlag = false;
        this.userInputFlag = true;
      }
      return;
  }

}
