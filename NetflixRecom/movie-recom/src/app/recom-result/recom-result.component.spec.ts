import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecomResultComponent } from './recom-result.component';

describe('RecomResultComponent', () => {
  let component: RecomResultComponent;
  let fixture: ComponentFixture<RecomResultComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecomResultComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecomResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
