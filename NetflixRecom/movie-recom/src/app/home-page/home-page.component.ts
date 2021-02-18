import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { DataService } from '../services/data.service';
import { NgForm, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Movie } from '../model/movie';
import { StarRatingComponent } from 'ng-starrating';
import _ from "loadsh";
import { MatDialog } from '@angular/material';
import { DialogMovieComponent } from '../dialog-movie/dialog-movie.component';


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


  constructor(private httpClient: HttpClient, private _data: DataService, private router: Router, public dialog: MatDialog) { }

  ngOnInit() {

    this.currentUser = this._data.getUserLogin();

    if(this.currentUser["newUserFlag"]) {

      // if user is new user
      this.recomMovieListbyMovieSim = this._data.recomMovieObject["MovieSim"];
      this.recomMovieListbyUserSim = this._data.recomMovieObject["UserSim"];
      console.log(this.recomMovieListbyMovieSim);

    } else {

      // if user is old user
      this.recomMovieListbyMovieSim = _.sampleSize(this._data.recomMovieObject["MovieSim"], 10);
      this.recomMovieListbyUserSim = _.sampleSize(this._data.recomMovieObject["UserSim"], 10);
      console.log("Inside Old USer ");
      console.log(this.recomMovieListbyMovieSim);
 
      
    }

    if(Object.keys(this.currentUser).length==0) {
      // need to modify with Oanth in future
      this.router.navigate(['login']);
    }


  }

  openMovieDialog(movie) {
    this.dialog.open(DialogMovieComponent, {
      width: '600px',
      height: '350px',
      data: movie
    });

  }

  loadEachMovieRate(group: FormGroup) {

    Object.keys(group.controls).forEach((key: string) => {
      const _movieRate = group.get(key);
      const _movie = new Movie(key, _movieRate.value);
      this.userRatingList.push(_movie)

    })

  }

  refreshMovieSimMovieList() {
    this.recomMovieListbyMovieSim = _.sampleSize(this._data.recomMovieObject["MovieSim"], 10);
  }


  refreshUserSimMovieList() {
    this.recomMovieListbyUserSim = _.sampleSize(this._data.recomMovieObject["UserSim"], 10);
  }

  onRate($event:{oldValue:number, newValue:number, starRating:StarRatingComponent}, moviename: string) {
    alert(`Old Value:${$event.oldValue}, 
      New Value: ${$event.newValue}, 
      Checked Color: ${$event.starRating.checkedcolor}, 
      Unchecked Color: ${$event.starRating.uncheckedcolor}
      name: ${moviename}`);
  }

}
