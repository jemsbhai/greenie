#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <dht.h>
LiquidCrystal_I2C lcd (0x27,16,2); // set the LCD address to 0x27 for a16 chars and 2 line display



dht DHT;

#define DHT11_PIN 8


int LED = 11; // Set LED pin at D11
int val = 0; // Read the voltage value of the photodiode




void setup ()
{
pinMode (LED, OUTPUT);
 Serial.begin(115200);
lcd.init (); // initialize the lcd
lcd.init (); // Print a message to the LCD.
lcd.backlight ();
lcd.setCursor (3,0);
lcd.print ("Greenie!"); // LED print name!
lcd.setCursor (2,1);
lcd.print ("Room 200"); // LED print room num!
}

void dhtcheck(){
           val = analogRead (A1); // Read the voltage value of A1 Pin
       
       if (val >600)
       {//  LED light is off
       digitalWrite (LED, LOW);
       } 
       else 
       {// Otherwise, the LED lights up
       digitalWrite (LED, HIGH);
       }
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("##");
  Serial.print(DHT.temperature);
  Serial.print(" : ");
  Serial.print(DHT.humidity);
  Serial.print(" : ");
  Serial.print (val); // Serial port to view the change of voltage value of light sensor
  Serial.println("$$");
  lcd.setCursor (0,0);
  lcd.print (DHT.temperature); // LED print name!
  lcd.setCursor (0,1);
  lcd.print (DHT.humidity); // LED print room num!
  delay(1000);
}

void lcdclear() {
  lcd.setCursor (0,0);
lcd.print ("Greenie! - hackathon"); // LED print name!
lcd.setCursor (0,1);
lcd.print ("Room 200 - CEWIT"); // LED print room num!
}

void lcdblank() {
  lcd.setCursor (0,0);
lcd.print ("                "); // LED print name!
lcd.setCursor (0,1);
lcd.print ("                "); // LED print room num!
}

void loop ()
{



  dhtcheck();
  delay(1000);
  lcdclear();
  delay(1000);
  lcdblank();
  
}
