import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material';
import {MAT_DIALOG_DATA} from '@angular/material';
import { Inject } from '@angular/core';
import { StarRatingComponent } from 'ng-starrating';

@Component({
  selector: 'app-dialog-movie',
  templateUrl: './dialog-movie.component.html',
  styleUrls: ['./dialog-movie.component.css']
})
export class DialogMovieComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }

  ngOnInit() {
    console.log('in the dialog');
    console.log(this.data);
  }


  onRate($event:{oldValue:number, newValue:number, starRating:StarRatingComponent}, moviename: string) {
    alert('Your Rating has submitted');
  }


}
