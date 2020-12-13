import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { fromEventPattern, Observable } from 'rxjs';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { MovieList } from '../model/movielist';
import { Movie } from '../model/movie';
import { MoviePoster } from '../model/movieposter';

@Injectable({
  providedIn: 'root'
})
export class DataService {


  userLogin = {};
  recomMovieList: any = [];
  recomMovieObject = {};
  finishFlag = false;

  constructor(private _http: HttpClient) {

  }

  // this two set & get is used for sharing login user info to home-page and newuser-page
  setUserLogin(username: string, userId: number, newUserFlag: boolean) {
    this.userLogin['username'] = username;
    this.userLogin['userId'] = userId;
    this.userLogin['newUserFlag'] = newUserFlag;
  }

  getUserLogin() {
    return this.userLogin;
  }


  getOldUserRecomMovieList(userLoginInfo: any): Observable<any>{
    const _url = "http://192.168.99.100:5001/getOldUserRecomMovieList";
    return this._http.post<any>(_url, userLoginInfo);
  }


  newUserRatingQuestion() {
    const _url = "http://192.168.99.100:5001/getMovieList";
    return this._http.get<any>(_url);
  }

  sendNewUserRatingList(userInfoAndMovieRating: any) {
    const _url = "http://192.168.99.100:5001/insertNewUserRating";
    let finishFlag = false;
    // wait for server load these rating data into MongoDB
    this._http.post(_url, userInfoAndMovieRating, {observe: 'response' as 'response'})
        .subscribe(
          response => {
            // check if all rating successfully insert into MongoDB
            this.getNewUserRecomMovieList(response.status, userInfoAndMovieRating);
            console.log("send new user rating to server");
            
        
    });

  }

  getNewUserRecomMovieList(response_status: number, userInfoAndMovieRating: any) {
    
    if(response_status==200) {
      const _url = "http://192.168.99.100:5001/getNewUserRecomMovies";
      // if insert successfully then use user-info to get Recom-MovieList from server 
      console.log("inside recommend part");
      console.log(userInfoAndMovieRating);
      this._http.post<any>(_url, userInfoAndMovieRating)
        .subscribe( data=> {

            this.setRecomMovieObject(data);            
            console.log("above is the RecommendList");
            
        })
        this.finishFlag = true;

    } else {
      // insert not successfully
      console.log('newuser-rating failed');
      this.finishFlag = false;
    }
  }

  setRecomMovieList(_recomMovieList: any) {
    /**
     * add Recom-Movie lists from server
     * RecomMovielist = {"MovieSim": [<list of recom-list by Movie-sim>], "UserSim": [<list of recom-list by User-sim>]}
     */
    this.recomMovieList = _recomMovieList;
  }

  getRecomMovieList() {
    return this.recomMovieList;
  }

  setRecomMovieObject(_recomMovieObj: any) {
    this.recomMovieObject = _recomMovieObj;

  }

  getRecomMovieObject() {
    return this.recomMovieObject;
  }

}
