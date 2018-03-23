import { Component, OnInit, OnDestroy } from '@angular/core';
import { PossibleBuysService } from '../PossibleBuysService';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  providers: [PossibleBuysService]
})
export class HomeComponent implements OnInit, OnDestroy {

  private intervalId: any;

  constructor(private possibleBuysService: PossibleBuysService) { }

  ngOnInit() {
    this.possibleBuysService.getPossibleBuys().subscribe(data => console.log(data));
    this.intervalId = setInterval(function() {
      console.log("bla");
      //.subscribe(data => this.data = {
      //  list: data['list']
      //});
   }, 1000);
  }

  ngOnDestroy() {
    if(this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

}
