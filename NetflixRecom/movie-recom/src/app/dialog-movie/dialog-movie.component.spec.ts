import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogMovieComponent } from './dialog-movie.component';

describe('DialogMovieComponent', () => {
  let component: DialogMovieComponent;
  let fixture: ComponentFixture<DialogMovieComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DialogMovieComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DialogMovieComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
