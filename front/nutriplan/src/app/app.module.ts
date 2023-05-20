import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

import { NgIconsModule } from '@ng-icons/core';
import { matRamenDiningOutline }from '@ng-icons/material-icons/outline'
import { heroHome, heroBars4, heroMagnifyingGlass } from '@ng-icons/heroicons/outline';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NoopAnimationsModule,
    NgIconsModule.withIcons({ heroHome, heroBars4, heroMagnifyingGlass, matRamenDiningOutline }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
