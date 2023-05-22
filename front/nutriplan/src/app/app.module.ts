import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

import { NgIconsModule } from '@ng-icons/core';
import { matRamenDiningOutline }from '@ng-icons/material-icons/outline'
import { heroHome, heroBars4, heroUser, heroMagnifyingGlass, heroXMark } from '@ng-icons/heroicons/outline';
import { typContacts } from '@ng-icons/typicons'
import { NavbarComponent } from './navbar/navbar.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NoopAnimationsModule,
    NgIconsModule.withIcons({ heroHome, heroBars4, heroMagnifyingGlass, matRamenDiningOutline, heroXMark, typContacts, heroUser }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
