import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-recom-result',
  templateUrl: './recom-result.component.html',
  styleUrls: ['./recom-result.component.css']
})
export class RecomResultComponent implements OnInit {
  @Input() message: string

  constructor() { }

  ngOnInit() {
    
  }

}
