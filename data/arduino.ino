#include "DHT.h"
#define DHTPIN 2     
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {

  delay(2000); // requires 2000 milliseconds
  float humid = dht.readHumidity();
  float fahren = dht.readTemperature(true); // Fahrenheit 

  // error reading
  if (isnan(humid) || isnan(fahren)) {
    Serial.println("Cannot read from DHT sensor");
    return;
  }

  float heatindex = dht.computeHeatIndex(fahren, humid); 
  Serial.println(heatindex);
  
}