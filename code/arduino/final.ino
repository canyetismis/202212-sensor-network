#include <SoftwareSerial.h>
SoftwareSerial HC05(10, 11); //HC06-TX Pin 10, HC06-RX to Arduino Pin 11

int LED_G = 12; //Use whatever pins you want
int LED_R = 13; //Use whatever pins you want 

void setup() {
  HC05.begin(9600); //Baudrate 9600 , Choose your own baudrate 
  pinMode(LED_G, OUTPUT);
  pinMode(LED_R, OUTPUT);
}

void loop() {
  if(HC05.available() > 0) //When HC06 receive something
  {
    char receive = HC05.read(); //Read from Serial Communication
    if(receive == '1') //If received data is 1, turn on the LED and send back the sensor data
    {
      digitalWrite(LED_G, LOW);
      digitalWrite(LED_R, HIGH); 
      delay(100);                   
      digitalWrite(LED_R, LOW);
      delay(100);
      digitalWrite(LED_R, HIGH); 
      delay(100);                      
      digitalWrite(LED_R, LOW);
       
      HC05.println("NOTICE: Alarm is on!");
    }
    else
    {
      digitalWrite(LED_G, HIGH);//If received other data, turn off LED
    }
  }


}
