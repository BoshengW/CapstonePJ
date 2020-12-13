import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { DataService } from '../services/data.service';
import { NgForm, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Movie } from '../model/movie';
import { StarRatingComponent } from 'ng-starrating';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {

  movies: any = []
  userRatingList: Movie[] = []
  recomMovieListbyMovieSim: any = []
  recomMovieListbyUserSim: any = []
  
  currentUser = {};


  constructor(private httpClient: HttpClient, private _data: DataService, private router: Router) { }

  ngOnInit() {

    this.currentUser = this._data.getUserLogin();

    if(this.currentUser["newUserFlag"]) {

      // if user is new user
      this.recomMovieListbyMovieSim = this._data.recomMovieObject["MovieSim"];
      this.recomMovieListbyUserSim = this._data.recomMovieObject["UserSim"];
      console.log(this.recomMovieListbyMovieSim);

    } else {

      // // user is old user
      // console.log("this is old user");
      // this._data.getOldUserRecomMovieList(this.currentUser).subscribe( data=> {
      //   // this.recomMovieListbyUserSim = data;
      //   this._data.setRecomMovieObject(data);
      this.recomMovieListbyMovieSim = this._data.recomMovieObject["MovieSim"];
      this.recomMovieListbyUserSim = this._data.recomMovieObject["UserSim"];
      console.log("Inside Old USer ");
      console.log(this.recomMovieListbyMovieSim);
      //   console.log(this._data.recomMovieObject);}, 
      //   err=>console.log("Failed to get Recommend for this old user"));
      
    }

  }

  loadEachMovieRate(group: FormGroup) {

    Object.keys(group.controls).forEach((key: string) => {
      const _movieRate = group.get(key);
      const _movie = new Movie(key, _movieRate.value);
      this.userRatingList.push(_movie)

    })

  }
  onRate($event:{oldValue:number, newValue:number, starRating:StarRatingComponent}, moviename: string) {
    alert(`Old Value:${$event.oldValue}, 
      New Value: ${$event.newValue}, 
      Checked Color: ${$event.starRating.checkedcolor}, 
      Unchecked Color: ${$event.starRating.uncheckedcolor}
      name: ${moviename}`);
  }


}
