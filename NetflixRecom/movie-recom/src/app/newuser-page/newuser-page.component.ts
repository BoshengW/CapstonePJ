import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { DataService } from '../services/data.service';
import { NgForm, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Movie } from '../model/movie';
import { StarRatingComponent } from 'ng-starrating';

import {FormControl} from '@angular/forms';
import {MatAutocompleteSelectedEvent, MatAutocomplete} from '@angular/material/autocomplete';
import {MatChipInputEvent} from '@angular/material/chips';
import { MatDialog } from '@angular/material';
import { DialogMovieComponent } from '../dialog-movie/dialog-movie.component';


/////////
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {ElementRef, ViewChild} from '@angular/core';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';

@Component({
  selector: 'app-newuser-page',
  templateUrl: './newuser-page.component.html',
  styleUrls: ['./newuser-page.component.css']
})
export class NewuserPageComponent implements OnInit {

  newUser_rating_dict = {};
  // userRatingList: Movie[] = [];
  popularMovieDict: any;
  selectMovieList: any={};
  generalMovieList: any = [];
  genreslist: any = [];

  // autocomplete chip
  visible = true;
  selectable = true;
  removable = true;
  separatorKeysCodes: number[] = [ENTER, COMMA];
  genreCtrl = new FormControl();
  filteredGenres: Observable<string[]>;
  genres_selected: string[] = [];

  @ViewChild('fruitInput', { static: true }) fruitInput: ElementRef;
  ///

  // load user info from login page
  currentUser = {};

  constructor(private httpClient: HttpClient, private _data: DataService, private router: Router,public dialog: MatDialog) { }

  ngOnInit() {


    this.currentUser = this._data.getUserLogin();

    if(Object.keys(this.currentUser).length==0) {
      // need to modify with Oanth in future
      this.router.navigate(['login']);
    }

    this._data.newUserRatingQuestion().subscribe( data=> {
      this.popularMovieDict = data;
      this.generalMovieList = this.popularMovieDict['Comedy']
      this.genreslist = this.popularMovieDict['GenresList']
      delete this.popularMovieDict.GenresList;

    });

    this.filteredGenres = this.genreCtrl.valueChanges.pipe(
      startWith(null),
      map((genre: string | null) => genre ? this._filter(genre) : this.genreslist.slice()));

  }

  /// chip operation 
  add(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    // Add our genre
    if ((value || '').trim()) {
      this.genres_selected.push(value.trim());
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }

    this.genreCtrl.setValue(null);
  }

  remove(genre: string): void {
    const index = this.genres_selected.indexOf(genre);

    if (index >= 0) {
      this.genres_selected.splice(index, 1);
    }
    console.log(this.genres_selected);
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    this.genres_selected.push(event.option.viewValue);
    this.fruitInput.nativeElement.value = '';
    this.genreCtrl.setValue(null);
    console.log(this.genres_selected);
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.genreslist.filter(genre => genre.toLowerCase().indexOf(filterValue) === 0);
  }

  ///

  showUserFavrite() {

    // update select Movielist based on user option
    for(var _selectGenre of this.genres_selected) {
      this.selectMovieList[_selectGenre] = this.popularMovieDict[_selectGenre];
    }

    console.log(this.selectMovieList);
  }

  openMovieDialog(movie) {
    this.dialog.open(DialogMovieComponent, {
      width: '600px',
      height: '350px',
      data: movie
    });

  }

  onRate($event:{oldValue:number, newValue:number, starRating:StarRatingComponent}, moviename: string, movieId: number) {
    
    this.newUser_rating_dict[movieId] = $event.newValue;
    console.log('movieId: ' + movieId + " rating: " + $event.newValue);

  }

  submitRate() {
    let _length = this.popularMovieDict.length;
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
