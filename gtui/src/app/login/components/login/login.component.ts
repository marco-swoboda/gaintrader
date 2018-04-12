import { Component, OnInit } from '@angular/core';
import { Credentials } from '../../models/credentials';
import { LoginService } from '../../services/login.service';
import { SecurityService } from '../../../shared/services/security.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  model: Credentials = new Credentials('', '');
  submitted = false;

  constructor(
    private loginService: LoginService,
    private securityService: SecurityService,
    private router: Router
  ) { }

  ngOnInit() {
  }

  onSubmit() {
    this.submitted = true;
    console.log('submitted: ', this.model);
    this.loginService.login(this.model).subscribe(
      token => {
        this.securityService.setToken(token.token);
        this.router.navigate(['/home']);
      },
      error => console.log('ERROR::', error)
    );
  }

  // TODO: Remove this when we're done
  get diagnostic() { return JSON.stringify(this.model); }
}


