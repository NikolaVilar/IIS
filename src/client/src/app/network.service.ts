import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { DatePipe } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class NetworkService {
  constructor(private datePipe: DatePipe) {}

  getForecast(): Observable<any> {
    // const url = 'http://localhost:5000/mbajk/predict';
    const url = 'http://172.28.1.2:5000/mbajk/predict';
    return new Observable<any>((observer) => {
      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok.');
          }
          return response.json();
        })
        .then((temp) => {
          const data = [];
          for (let i = 0; i < temp.available_bike_stands.length; i++) {
            const record = {
              day: this.datePipe.transform(temp.hours[i], 'EEEE'),
              hour: temp.hours[i],
              bikeStands: temp.available_bike_stands[i],
              temp: temp.temperature[i],
              hum: temp.relative_humidity[i],
              dew: temp.dew_point[i],
            };
            data.push(record);
          }
          observer.next(data);
          observer.complete();
        })
        .catch((error) => {
          alert('Network error');
          console.error(error);
          observer.error({ error: error });
        });
    }).pipe(
      catchError((error): any => {
        alert('Network error');
        console.log(error);
        return { error: error };
      })
    );
  }
}
