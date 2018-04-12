import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';


import { AppComponent } from './app.component';
import { AppRouterModule } from './app.router.module';
import { HomeComponent } from './home/home.component';
import { PossibleBuysService } from './PossibleBuysService';
import { LoginModule } from './login/login.module';
import { SharedModule } from './shared/shared.module';
import { HttpAccessTokenInterceptor } from './HttpAccessTokenInterceptor';


@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    SharedModule,
    LoginModule,
    AppRouterModule
  ],
  declarations: [
    AppComponent,
    HomeComponent
  ],
  providers: [
    // SecurityService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpAccessTokenInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
