import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginInfo } from '../models/login-info';
import { Credentials } from '../models/credentials';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class LoginService {

  constructor(private http: HttpClient) { }

  login(credentials: Credentials): Observable<LoginInfo> {
    const url = environment.apiUrl + '/login';
    console.log('URL:', url);
    return this.http.post<LoginInfo>(url, credentials);
  }

}
