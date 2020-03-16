import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TpmsComponent } from './tpms.component';

describe('TpmsComponent', () => {
  let component: TpmsComponent;
  let fixture: ComponentFixture<TpmsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TpmsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TpmsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
