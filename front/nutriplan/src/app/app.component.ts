import { Component } from '@angular/core';
import { faHand } from '@fortawesome/free-regular-svg-icons';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'nutriplan';
  fasHand = faHand;
}
