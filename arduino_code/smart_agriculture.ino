#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN,DHTTYPE);

int soilPin = 34;
int relayPin = 2;

void setup()
{
  Serial.begin(115200);

  pinMode(relayPin,OUTPUT);

  dht.begin();
}

void loop()
{
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  int soil = analogRead(soilPin);

  Serial.print("Temperature: ");
  Serial.println(temp);

  Serial.print("Humidity: ");
  Serial.println(hum);

  Serial.print("Soil: ");
  Serial.println(soil);

  if(soil < 1500)
  {
      digitalWrite(relayPin,HIGH);
      Serial.println("Pump ON");
  }
  else
  {
      digitalWrite(relayPin,LOW);
      Serial.println("Pump OFF");
  }

  delay(2000);
}