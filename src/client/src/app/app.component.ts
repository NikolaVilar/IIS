import { RouterOutlet } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { NetworkService } from './network.service';
import { lastValueFrom } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  forecast: {
    day: any;
    hour: any;
    bikeStands: any;
    temp: any;
    hum: any;
    dew: any;
  }[] = [];

  constructor(private networkService: NetworkService) {}

  ngOnInit(): void {
    this.getData();
  }

  async getData() {
    this.forecast = await lastValueFrom(this.networkService.getForecast());
  }

  isGoodTime(record: {
    day: any;
    hour: any;
    bikeStands: any;
    temp: any;
    hum: any;
    dew: any;
  }) {
    if (record.bikeStands < 1) return false;
    if (record.temp < 5 || record.temp > 30) return false;
    if (record.hum > 70) return false;
    if (record.dew > 20) return false;
    return true;
  }
}
