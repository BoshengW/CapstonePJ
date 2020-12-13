import { Component, OnInit, Input } from '@angular/core';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-recom-result',
  templateUrl: './recom-result.component.html',
  styleUrls: ['./recom-result.component.css']
})
export class RecomResultComponent implements OnInit {
  
  recom_movielist: any = [];

  constructor(private _data: DataService) { }


  ngOnInit() {
    
    this.recom_movielist = this._data.getRecomMovieList();
    console.log(this.recom_movielist);
    
  }

  submit() {
    this.recom_movielist = this._data.getRecomMovieList();
    console.log(this.recom_movielist);


  }

}
