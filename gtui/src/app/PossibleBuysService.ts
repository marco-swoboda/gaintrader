import { Injectable } from '@angular/core';
import { } from '@angular/core/';

import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

@Injectable()
export class PossibleBuysService {

  constructor(private http: HttpClient) { }

  possibleBuysUrl = '/possibleBuys';

  getPossibleBuys() {
    console.log('dksaldlaklsall');
    const url = environment.apiUrl + '/user';
    return this.http.get(url);
  }

}
