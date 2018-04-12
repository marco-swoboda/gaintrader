import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class SecurityService {

  token: string;

  constructor() { }

  getJwtToken(): string {
    return this.token;
  }

  setToken(token: string) {
    console.log('NEW TOKEN: ', token);
    return  this.token = token;
  }

}



