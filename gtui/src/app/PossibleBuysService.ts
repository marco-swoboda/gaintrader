import { Injectable } from '@angular/core';
import { } from '@angular/core/';

import { HttpClient } from '@angular/common/http';

@Injectable()
export class PossibleBuysService {

  constructor(private http: HttpClient) { }

  possibleBuysUrl = '/possibleBuys';

  getPossibleBuys() {
    console.log("dksaldlaklsall");

    return this.http.get(this.possibleBuysUrl);
  }

}
