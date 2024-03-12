import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { map } from 'rxjs/operators';
import { DatePipe } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class NetworkService {
  constructor(private httpClient: HttpClient, private datePipe: DatePipe) {}

  getForecast(): Observable<any> {
    const url = 'http://localhost:5000/mbajk/predict';
    return this.httpClient.get<any>(url).pipe(
      map((temp) => {
        const data: {
          day: any;
          hour: any;
          bikeStands: any;
          temp: any;
          hum: any;
          dew: any;
        }[] = [];
        for (let i = 0; i < temp.available_bike_stands.length; i++) {
          const record = {
            day: this.datePipe.transform(temp.hours[i], 'EEEE'),
            hour: temp.hours[i],
            bikeStands: temp.available_bike_stands[i],
            temp: temp.temperature[i],
            hum: temp.relative_humidity[i],
            dew: temp.dew_point[i],
          };
          data.push(
            record as {
              day: any;
              hour: any;
              bikeStands: any;
              temp: any;
              hum: any;
              dew: any;
            }
          );
        }

        return data;
      }),
      catchError((error): any => {
        alert('Network error');
        console.log(error);
        return { error: error };
      })
    );
  }
}
