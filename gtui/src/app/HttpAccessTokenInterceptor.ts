import {Injectable} from '@angular/core';
import {HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import { SecurityService } from './shared/services/security.service';

@Injectable()
export class HttpAccessTokenInterceptor implements HttpInterceptor {

  constructor(private security: SecurityService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    // const apiReq = req.clone({ url: `https://localhost:5000${req.url}` });
    const token = this.security.getJwtToken();
    let httpOptions = {headers: new HttpHeaders({})};
    if (token) {
      httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
          'x-access-token': token
        })
      };
    }
    const apiReq = req.clone(httpOptions);
    return next.handle(apiReq);
  }
}
