//This includes 2 LEDs in order to show wich channel is choosen

#define CH1 7   // Connect Digital Pin 7 on Arduino to CH3 on Relay Module
#define CH2 8   // Connect Digital Pin 8 on Arduino to CH1 on Relay Module

#define LEDCH1 11
#define LEDCH2 12

String comando1 = "CLOCK1"; 
String comando2 = "CLOCK2"; 
String comando3 = "AUTO"; 
String channel = "CLOCK1"; 

int led = 13;
int flag = 1;

unsigned long previousMillis = 0;        // will store last time LED was updated
const long interval = 10000;           // interval at which to blink (milliseconds)

void setup(){
  //Setup all the Arduino Pins
  pinMode(CH1, OUTPUT);
  pinMode(CH2, OUTPUT);
  //Turn OFF any power to the Relay channels
  digitalWrite(CH1,LOW);
  digitalWrite(CH2,LOW);

  pinMode(LEDCH1, OUTPUT);
  pinMode(LEDCH2, OUTPUT);
  digitalWrite(LEDCH1,LOW);
  digitalWrite(LEDCH2,LOW);
  

  
  Serial.begin(9600);
  Serial.println("Welcome to MuxRelay_v4 !!!");
  Serial.println("You can send CLOCK1(default) or CLOCK2 to select the Atomic Clock of your convinience. ");
  Serial.println("You can send AUTO and it will select CLOCK1 or CLOCK2 alternatively every 5 seconds. ");
  Serial.println("");
  pinMode(led, OUTPUT);
  delay(2000); //Wait 2 seconds before starting sequence
}


void loop()
{
if(Serial.available())
  {
    String comando = Serial.readString();
    
    if(comando == comando1)
    flag = 1;
    if(comando == comando2)
    flag = 2;
    if(comando == comando3)
    {
      flag = 0;
      Serial.println("AUTO Mode selected");
      previousMillis = 0;  
    }
    
  }

int flag = 0;


if(flag == 1)
  {
   Serial.println("CLOCK1 selected");
   digitalWrite(CH1, LOW);
   digitalWrite(CH2,LOW);
   digitalWrite(LEDCH1,HIGH);
   digitalWrite(LEDCH2,LOW);

   
  }
if(flag == 2)
  {
   Serial.println("CLOCK2 selected");
   digitalWrite(CH1, HIGH);
   digitalWrite(CH2,HIGH);
   digitalWrite(LEDCH1,LOW);
   digitalWrite(LEDCH2,HIGH);
  }
if(flag == 0) // This is the AUTO function
  {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) 
    {
    previousMillis = currentMillis;
    if (channel == "CLOCK1") 
      {
      channel = "CLOCK2";
      Serial.println("AUTO CLOCK1 selected");
      digitalWrite(CH1, LOW);
      digitalWrite(CH2, LOW);
      digitalWrite(LEDCH1,HIGH);
      digitalWrite(LEDCH2,LOW);
      } 
    else
      {
      channel = "CLOCK1";
      Serial.println("AUTO CLOCK2 selected");
      digitalWrite(CH1, HIGH);
      digitalWrite(CH2, HIGH);
      digitalWrite(LEDCH1,LOW);
      digitalWrite(LEDCH2,HIGH);
      }
    }
  }
}
