import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MovieList } from '../model/movielist';
import { Movie } from '../model/movie';
import { MoviePoster } from '../model/movieposter';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private _http: HttpClient) {

  }

  getMoiveList(): Observable<MovieList[]>{
    const _url = "http://localhost:5000/getMovieList";
    return this._http.get<MovieList[]>(_url);
  }

  getMovieListAndPoster(): Observable<MoviePoster[]>{
    const _url = "../../assets/movie_meta.json";
    return this._http.get<MoviePoster[]>(_url);
  }

  getRecomMovies(movieRateList: Movie[]): Observable<MovieList[]>{
    const _url = "http://localhost:5000/getRecomMovies"
    return this._http.post<MovieList[]>(_url, movieRateList);
  }

}
