import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SecurityService } from './services/security.service';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [],
  providers: [SecurityService],
  exports: []
})
export class SharedModule { }
