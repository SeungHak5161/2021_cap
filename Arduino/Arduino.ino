#include <SPI.h>
#include <Wire.h>
#include <SoftwareSerial.h>
int red_led=4;
int green_led=5;
int blue_led=6;
int flame_pin=7;
int buzzer_pin=8;
unsigned long starttime;
unsigned long duration;
unsigned long cur_time;
unsigned long pre_time;
unsigned long sampletime_ms=10500;//10초마다 울림
unsigned int flame;

unsigned long hi;
unsigned long lo;
unsigned long CO2;
unsigned int ch;
SoftwareSerial mySerial(10, 11); // RX, TX
unsigned char hexdata[9] = {0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79}; //Read the gas density command /Don't change the order
void setup() {
  Serial.begin(9600);
  pinMode(buzzer_pin,OUTPUT);
  pinMode(flame_pin,INPUT);
  pinMode(red_led,OUTPUT);
  pinMode(blue_led,OUTPUT);
  pinMode(green_led,OUTPUT);
  
  while(!Serial) {}
  mySerial.begin(9600);
  starttime=millis();
  pre_time=millis();
  duration=millis();
  digitalWrite(blue_led,1);
}
void loop() {
  for(int i=0; i<9; i++) {
     mySerial.write(hexdata,9);
    if(mySerial.available()>0) {
       ch = mySerial.read();
      if(i==2) { hi=ch; }   //High concentration
      if(i==3) { lo=ch; }   //Low concentration
      if(i==8) {
        CO2 = hi * 256 + lo;  //CO2 concentration
        //Serial.print("CO2 concentration: ");
        //Serial.print(CO2);
        //Serial.println("ppm");      
      }
    }   
  } 
  if((millis()-duration)>8000){//5초마다 부저 울림
    duration=millis();
     if(CO2>=3000 || digitalRead(flame_pin)==0){
      tone(buzzer_pin,100,3000);
      }
  }
  delay(500);
  if((millis()-starttime)>sampletime_ms){//10초마다 데이터 전송 &&화재 알림
      Serial.println(String(CO2));
      starttime=millis();
      if(CO2<=1000){
          digitalWrite(green_led,0);
          digitalWrite(red_led,0);
          digitalWrite(blue_led,1);
      }
      else if(CO2>1000 && CO2<=3000){
        digitalWrite(blue_led,0);
        digitalWrite(red_led,0);
        digitalWrite(green_led,1);
      }
      else{
        digitalWrite(blue_led,0);
        digitalWrite(green_led,0);
        digitalWrite(red_led,1);
      }
    }
   // Serial.println(String(CO2));
}
