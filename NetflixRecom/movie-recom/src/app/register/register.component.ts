import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { User} from '../model/user';
import {RegisterService } from '../services/register.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  newUser: any = {};
  registerUser = new User("","","");
  registerFlag = false;
  clickFlag = false;

  constructor(private _register: RegisterService, private router: Router) { }

  ngOnInit() {
  }

  onSubmit(registerForm: NgForm) {

    console.log(registerForm.value);
    const registerUser = new User(registerForm.value.username, registerForm.value.password,
                                  registerForm.value.email);
    
    this._register.submitUserForm(registerUser)      
      .subscribe(
        response => {
          let _res_statusCode = response;
          this.validateResponseStatus(_res_statusCode.status);
    })
    
  }

  validateResponseStatus(status: number){
    if(status==200) {
      //insertion success navigate to login page
      this.registerFlag = true;
      this.clickFlag = true;
      this.router.navigate(['login']);
    } else {
      this.registerFlag = false;
      this.clickFlag = true;
    }
  }

}
