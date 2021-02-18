import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { LoginvalidService } from '../services/loginvalid.service';
import { DataService } from '../services/data.service';
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
  // username = ""; // don't do that make a global variable with username & password will make two-way binding which is un-safe
  // password = "";
  userModel = new User("","","");
  loginFlag = false;
  userInputFlag = false;
  userFromDB: any = {};

  constructor(private httpClient: HttpClient, private _login: LoginvalidService,
    private router: Router, private _data: DataService) { }

  ngOnInit() {
    this.loginFlag = false;
    this.userInputFlag = false;
  }

  login(userLogin: NgForm) {

    this.userModel.username = userLogin.value.username;
    this.userModel.password = userLogin.value.password;
    console.log(this.userModel.username);
    console.log(this.userModel.password);

    this._login.getloginInfo(this.userModel).subscribe(
      data => {
        this.validate(data);
    }
      )
  
  }

  validate(response: any) {

      let _user = response;
      let _username = _user.username;
      let _password = _user.password;
      console.log(_user);
      //First---check if username exist in DB
      if(_user.userExist) {
        // if username exist then check password
        if(this.userModel.username==_username && this.userModel.password==_password) {
            console.log(_username);
            console.log(_password);
            // login and UserInput successfully
            this.loginFlag = true;
            this.userInputFlag = true;

            // Second---check if user is new user or not
            if(_user.newUser) {
              // user is new user
              // communicate user-login info into data service
              this._data.setUserLogin(_username,_user.userId,_user.newUser);
              this.router.navigate(['newuser']);


            } else {
              // user is old user
              this._data.setUserLogin(_username,_user.userId,_user.newUser);
              // get the recommendlist before load in home page
               // user is old user
              console.log("this is old user");
              this._data.getOldUserRecomMovieList(this._data.getUserLogin()).subscribe( data=> {
                // this.recomMovieListbyUserSim = data;
                this._data.setRecomMovieObject(data);
                console.log(this._data.recomMovieObject);}, 
                err=>console.log("Failed to get Recommend for this old user"));
              
              //delay waiting for response
              setTimeout(() => {
                this.router.navigate(['home']);
              },6000);

            }


        } else {
            // User input successfully, but login not match with database
            this.loginFlag = false;
            this.userInputFlag = true;
        }

      } else {
          // user not exist in DB,
          this.loginFlag = false;
          this.userInputFlag = true;
      }
      return;

  }

}
