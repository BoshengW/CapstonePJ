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
  recomMovieList: any = []
  moviesPoster: any = []
  


  constructor(private httpClient: HttpClient, private _data: DataService, private router: Router) { }

  ngOnInit() {
    // this is the initialization part
    // this._data.getMoiveList().subscribe(
    //   data => { this.movies=data;
    //     console.log(this.movies);
    // })

    this._data.getMovieListAndPoster().subscribe( data=> {
      this.moviesPoster = data;
      console.log(this.moviesPoster);
    })

  }

  recommend(rateList: NgForm) {
    this.loadEachMovieRate(rateList.form);
    this._data.getRecomMovies(this.userRatingList).subscribe(data=> {
      this.recomMovieList = data;
      console.log(this.recomMovieList); // need to use console.log to wait for subscribe finish loading data
    });


    // this.router.navigate(['recomsys']);
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
