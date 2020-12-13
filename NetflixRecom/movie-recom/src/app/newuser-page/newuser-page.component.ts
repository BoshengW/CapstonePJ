import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { DataService } from '../services/data.service';
import { NgForm, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Movie } from '../model/movie';
import { StarRatingComponent } from 'ng-starrating';

@Component({
  selector: 'app-newuser-page',
  templateUrl: './newuser-page.component.html',
  styleUrls: ['./newuser-page.component.css']
})
export class NewuserPageComponent implements OnInit {

  newUser_rating_dict = {};
  // userRatingList: Movie[] = [];
  movies_chooseFromServer: any = [];

  // load user info from login page
  currentUser = {};

  constructor(private httpClient: HttpClient, private _data: DataService, private router: Router) { }

  ngOnInit() {

    this._data.newUserRatingQuestion().subscribe( data=> {
      this.movies_chooseFromServer = data;
      console.log(this.movies_chooseFromServer);
    });

    this.currentUser = this._data.getUserLogin();

    if(Object.keys(this.currentUser).length==0) {
      // need to modify with Oanth in future
      this.router.navigate(['login']);
    }


  }


  onRate($event:{oldValue:number, newValue:number, starRating:StarRatingComponent}, moviename: string, movieId: number) {
    
    this.newUser_rating_dict[movieId] = $event.newValue;
    console.log('movieId: ' + movieId + " rating: " + $event.newValue);

  }

  submitRate() {
    let _length = this.movies_chooseFromServer.length;
    // console.log(_length);
    console.log(this.newUser_rating_dict)

    if(Object.keys(this.newUser_rating_dict).length==_length) {
      // if all movies have been rated then send ratings back to server and navigate to home page
      let _userInfoAndMovieRating = {};
      
      _userInfoAndMovieRating['userInfo'] = this.currentUser;
      _userInfoAndMovieRating['movieRating'] = this.newUser_rating_dict;

      
      this._data.sendNewUserRatingList(_userInfoAndMovieRating);
      // to solve async process issue most easy way is to setTimeout for delay
      setTimeout(() => {
    
        if(this._data.finishFlag) {
          this.router.navigate(["home"]);
  
        } else {
          alert("recommend process failed");
        }
      }, 2000);
     

    } else {
      // if un-rating movies exist, alert and stay in this page
      alert(`Please rate all movies in the list!`);
    }
  }



}
