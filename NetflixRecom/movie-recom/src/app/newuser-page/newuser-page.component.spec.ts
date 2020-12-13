import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewuserPageComponent } from './newuser-page.component';

describe('NewuserPageComponent', () => {
  let component: NewuserPageComponent;
  let fixture: ComponentFixture<NewuserPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewuserPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewuserPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
