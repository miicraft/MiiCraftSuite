/*
    NVP Control Program 2012/07/31
    
    Copyright (C) 2012  Paul Kang, Benson Hong, Young Optics

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/* stepping motor motion table */
#include <D:\N_50.h>
#include <D:\N_100.h>
#include <D:\S_50.h>
#include <D:\S_100.h>
#include <MsTimer2.h>

/* stepping motor control pins */
int DirPin   = 6;                   // for Direction
int PulsePin = 7;                   // for Pulse (low active)
int ENAPin   = 8;                   // Enable (high active)

/* indicator LED control pins */
int ledPin1 = 50;                    // indicator LED
int ledPin2 = 51;
int ledPin3 = 52;
int ledPin4 = 53;

/* Resin pump control pins */
int Resin_motor_en = 10;              //resin motor enable
int Resin_motor_ph = 11;              //resin motor phase
int Resin_motor_mode1 = 12;           //resin motor mode1
int Resin_motor_mode2 = 13;           //resin motor mode2

/* Pico projector control pins */
int selio = 44;                      //select trigger or cpu bus
int LE = 46;                         //pico projector on/off
int UV_led = 45;                     //UV led on/off

/* Post Curing control pins */
int UV_motor = 4;                    //fluorescent UV motor
int UV_flu = 38;                     //for fluorescent UV

/*input switch digital */
int count_SW = 2;                  //for UV motor ; interrupt 0
int UV_door = 3;                    //UV door open ; interrupt 1

/*input switch analog */
int resin_empty = A0;                  //resin_empty
int Sample_door = A1;                  //Sample door open
int top = A2;                        //stepping motor top
int bottom = A3;                     //stepping motor bottom

int incomingByte = 0;	   // for incoming serial data

int light_state;             // for UV light state
int origin;                  // for UV motor position
int post_module_state;       // check post module yes/no

void setup()
{
/* Serial */  
  Serial.begin(9600);
  Serial.println("2012-07-31a");

/* PinMode  */      
  pinMode(DirPin,   OUTPUT);      // sets the Direction pin as output
  pinMode(PulsePin, OUTPUT);      // sets the Pulse pin as output
  pinMode(ENAPin,   OUTPUT);      // sets the Enable pin as output
 
  pinMode(Resin_motor_en, OUTPUT);  
  pinMode(Resin_motor_ph, OUTPUT);
  
  pinMode(selio, OUTPUT);
  pinMode(LE, OUTPUT);
  pinMode(UV_led, OUTPUT);  
  
  pinMode(UV_motor, OUTPUT); 
  pinMode(UV_flu, OUTPUT);

  pinMode(resin_empty, INPUT);  
  pinMode(UV_door, INPUT);     
  pinMode(count_SW, INPUT);      
  pinMode(top, INPUT);         
  pinMode(bottom, INPUT);      
     
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT); 

/* Stepping motor  */   
  digitalWrite(ENAPin, LOW);             // sets the Enable HIGH (enabled)  
  digitalWrite(DirPin, HIGH);           // sets the Direction HIGH
  digitalWrite(PulsePin, HIGH);           // sets the Pulse HIGH (inactive) 
  
/* Resin motor */ 
  digitalWrite(Resin_motor_en,LOW);      //motor off
  digitalWrite(Resin_motor_ph,LOW);
  
/* Post Curing */   
  digitalWrite(UV_motor,LOW);            // set fluorescent motor off
  digitalWrite(UV_flu,LOW);              // set fluorescent UV off
  attachInterrupt(1,UV_door_open,CHANGE);  // door open
  attachInterrupt(0,platform_position,CHANGE);  // position detect

/* Pico projector */
  digitalWrite(selio,HIGH);           //select trigger
  digitalWrite(LE,HIGH);              //Light engine enable
  digitalWrite(UV_led,LOW);           //Light engine UV LED off

/* others */  
  digitalWrite(ledPin1, HIGH);      //LED on
  digitalWrite(ledPin2, LOW);      //LED off
  digitalWrite(ledPin3, LOW);      //LED off
  digitalWrite(ledPin4, LOW);      //LED off
  
  MsTimer2::set(800, flash);
  
  light_state = 0;
  origin = 0;
  post_module_state = 0;
}


void loop()
{    

delayMicroseconds(500); 

if (Serial.available() > 0) {
	// read the incoming byte:
	incomingByte = Serial.read();
	//Serial.println(incomingByte, BYTE);
	Serial.write(incomingByte);
	Serial.write(" ");

  switch (incomingByte) {
     case 'a':                             //Z_table_up
       step_up();
       break;

     case 'b':                             //Z_table_down
       step_down();
       break;
       
     case 'u':                             //Z_table_check
       step_up_pause();       
       break;       

     case 'c':                             //micro step
       step_micro_e1();
       break;
       
     case 'd':                             //micro step
       step_micro_e2();
       break;
       
     case 'e':                             //micro step
       step_micro_e3();
       break;
      
     case 'f':                             //micro step
       step_micro_e4();
       break;
       
     case 'g': 
       resin_motor_i();                    //pumping resin
       break;
       
     case 'h': 
       digitalWrite(Resin_motor_en,LOW);   //stop pumping (for test)
       break;
       
     case 'i':    
       resin_motor_o();                    //redraw resin
       break;
             
     case 'k':                             //UV motor on
       UV_motor_on();
       break;
       
     case 'l':                              
       digitalWrite(UV_motor,LOW);         //UV motor off (for test)
       break;
       
     case 'm':
       digitalWrite(LE,HIGH);              //pico projector on (for test)
       break;
       
     case 'n':                              
       digitalWrite(LE,LOW);               //pico projector on (for test)
       break;
       
     case 'p':                             //fluorescent UV on
       light_state = 1;
       if (digitalRead(UV_door)==LOW){
          digitalWrite(UV_flu,LOW);
          }
       else{
          digitalWrite(UV_flu,HIGH);
       }                 
       Serial.println("OK");
       break;  
       
     case 'q':                             //fluorescent UV off
       light_state = 0;     
       digitalWrite(UV_flu,LOW); 
       Serial.println("OK");  
       break;         
       
     case 'r':                         
       digitalWrite(UV_led,HIGH);          //LED UV on
       Serial.println("OK");   
       break;  
       
     case 's':                            
       digitalWrite(UV_led,LOW);           //LED UV off
       Serial.println("OK");
       break;

     default:
       break;
// note: 't'==> stop all motor!!!      
   }     
 }
  //Serial.flush();                              //clear serial receiver buffer
}                                                //end of program

void flash()
{
  static boolean output = HIGH;

  digitalWrite(ledPin1, output);
  output = !output;
}

/*  command 'A' */
void step_up()                             //800 pps
{
       digitalWrite(ENAPin, HIGH);         // sets the Enable HIGH (enabled)  
       digitalWrite(DirPin, HIGH);         // sets the Direction up
       while (analogRead(top) < 500){

//         if (digitalRead(power) == LOW)              //24V power off
//           break;           

	 if (Serial.available() > 0) {
	   incomingByte = Serial.read();
	   if (incomingByte == 't') break;   
	 }   
	       
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delayMicroseconds(800);           // pauses for 800 microseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin on
         delayMicroseconds(800);           // pauses for 800 microseconds  
       }
       delay(50);
       if (analogRead(top) > 500){
       Serial.println("OK");
       }
       else {
       Serial.println("NG");
       }
       MsTimer2::stop();
       digitalWrite(ledPin1, HIGH);

}
/*  command 'B' */                         //800~100pps
void step_down()
{
       digitalWrite(ENAPin, HIGH);         // sets the Enable HIGH (enabled)  
       digitalWrite(DirPin, LOW);          // sets the Direction down
       int i = -4999;
       int j = 32000;
       int fast = 800;
       int slow = 12000;
       int pause;
          while (i>-5000){
           if(analogRead(bottom) > 500) 
              break;  
//           if(digitalRead(power) == LOW)      //24V power off
//              break;
           if( i<=j){ pause = fast; }
             else { pause = slow;
          i--; }                             //keep i value in constant avoid over 
             
           if (Serial.available() > 0) {
             incomingByte = Serial.read();
             if (incomingByte == 't')
             break;
	   }            
           digitalWrite(PulsePin, LOW);    // sets the pin off
           delayMicroseconds(pause);         // pauses for microseconds     
           digitalWrite(PulsePin, HIGH);   // sets the pin on
           delayMicroseconds(pause);         // pauses for microseconds     
           i++;
           //Serial.println(i);
           }
       delay(50);
       if (analogRead(bottom) > 500){
       Serial.println("OK");
       }
       else {
       Serial.println("NG");
       }    

}

/* command 'U' */
void step_up_pause()
{
  int n=0;  
       digitalWrite(ENAPin, HIGH);         // sets the Enable HIGH (enabled)  
       digitalWrite(DirPin, HIGH);       // sets the Direction up
       
       for (int m=0;m<200;m++){
         if (analogRead(top) > 500){
           break;
         }
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(30);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(30);           // pauses for k miniseconds
         n=m+1;         
       }
       int i = 10200-n;
         while (i != 0){
           if (analogRead(top) > 500) 
              break;  
//           if (digitalRead(power) == LOW)              //24V power off
//              break;  
           digitalWrite(PulsePin, LOW);    // sets the pin off
           delayMicroseconds(1000);         // pauses for 1000 microseconds     
           digitalWrite(PulsePin, HIGH);   // sets the pin on
           delayMicroseconds(1000);         // pauses for 1000 microseconds     
           i--;         
         }
       Serial.println("OK");
//       Serial.println(i);
         int k =0;
         while (k==0){
          if (Serial.available() > 0)
          incomingByte = Serial.read();
          if (incomingByte == 'v')
          k=1;
          if (incomingByte == 't')
          return;
          delay(100);
         }
       Serial.write(incomingByte);
       digitalWrite(DirPin, LOW);         // sets the Direction down
       int j = i;                      
         while (j != 10200){ 
//           if (digitalRead(power) == LOW)              //24V power off
//              break;  
           digitalWrite(PulsePin, LOW);    // sets the pin off
           delayMicroseconds(1000);         // pauses for 1000 microseconds     
           digitalWrite(PulsePin, HIGH);   // sets the pin on
           delayMicroseconds(1000);         // pauses for 1000 microseconds     
           j++;     
         }         
       Serial.println("OK");         
}

/* command 'C' */
void step_micro_e1()
{
       int j = 0;
       int k = 0;
       /* step up */
       digitalWrite(ENAPin, HIGH);         // sets the Enable enable 
       digitalWrite(DirPin, HIGH);         // sets the Direction up
       for (int i=0;i<200;i++){
         if (analogRead(top) > 500) 
            break; 
         k = nhalf[j];
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds  
         j++;
       }        
       delay(100);
       /* step down */
       digitalWrite(DirPin, LOW);          // sets the Direction down
       for (int i=0;i<190;i++){
         if (analogRead(top) > 500) 
            break;
         k = nhalf[j];           
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds 
         j++;
       } 
       Serial.println("OK");       
} 

/* command 'D' */
void step_micro_e2()
{
       int j = 0;
       int k = 0;
       /* step up */
       digitalWrite(ENAPin, HIGH);         // sets the Enable enable 
       digitalWrite(DirPin, HIGH);         // sets the Direction up
       for (int i=0;i<200;i++){
         if (analogRead(top) > 500) 
            break; 
         k = nfull[j];
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds  
         j++;
       }        
       delay(100);
       /* step down */
       digitalWrite(DirPin, LOW);          // sets the Direction down
       for (int i=0;i<180;i++){
         if (analogRead(top) > 500) 
            break;
         k = nfull[j];           
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds 
         j++;
       } 
       Serial.println("OK");       
} 

/* command 'E' */
void step_micro_e3()
{
       int j = 0;
       int k = 0;
       /* step up */
       digitalWrite(ENAPin, HIGH);         // sets the Enable enable 
       digitalWrite(DirPin, HIGH);         // sets the Direction up
       for (int i=0;i<200;i++){
         if (analogRead(top) > 500) 
            break; 
         k = shalf[j];
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds  
         j++;
       }        
       delay(100);
       /* step down */
       digitalWrite(DirPin, LOW);          // sets the Direction down
       for (int i=0;i<190;i++){
         if (analogRead(top) > 500) 
            break;
         k = shalf[j];           
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds 
         j++;
       } 
       Serial.println("OK");       
} 

/* command 'F' */
void step_micro_e4()
{
       int j = 0;
       int k = 0;
       /* step up */
       digitalWrite(ENAPin, HIGH);         // sets the Enable enable 
       digitalWrite(DirPin, HIGH);         // sets the Direction up
       for (int i=0;i<200;i++){
         if (analogRead(top) > 500) 
            break; 
         k = sfull[j];
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds
         j++;
       }        
       delay(100);
       /* step down */
       digitalWrite(DirPin, LOW);          // sets the Direction down
       for (int i=0;i<180;i++){
         if (analogRead(top) > 500) 
            break;
         k = sfull[j];           
         digitalWrite(PulsePin, LOW);      // sets the pin off
         delay(k);           // pauses for k miniseconds     
         digitalWrite(PulsePin, HIGH);     // sets the pin off
         delay(k);           // pauses for k miniseconds 
         j++;
       } 
       Serial.println("OK");       
} 

/* command 'G' */
void resin_motor_i()
{
  MsTimer2::start();
  delay(50);

  int resin_type = 0;
  digitalWrite(Resin_motor_ph,LOW);          //Raising resin motor enable
  
  for (int i=0;i<15;i++){
    Serial.println("g");
    if (analogRead(resin_empty) > 150){
      digitalWrite(Resin_motor_en,LOW);
      resin_type = 1;
      break;
    }
    digitalWrite(Resin_motor_en,HIGH);          //Raising resin motor enable
    delay(2000);
  }   
  
  digitalWrite(Resin_motor_en,LOW);
  if (resin_type == 1){
    Serial.println("OK");
  }
  else{
    Serial.println("NG");
  }
}

/*  command 'I' */
void resin_motor_o()  
{
  MsTimer2::start();
  digitalWrite(Resin_motor_ph,HIGH);          //Raising resin motor enable
  digitalWrite(Resin_motor_en,HIGH);          //Raising resin motor enable
  for (int i=0;i<50;i++){
  delay(100);
  }
  digitalWrite(Resin_motor_en,LOW);
  Serial.println("OK");
  MsTimer2::stop();
  digitalWrite(ledPin1, HIGH);
}

/* command 'K' */
void UV_motor_on()
{
  int i=1;
  post_module_state =0;
  digitalWrite(UV_motor,HIGH);
  while(i==1){
    delay(200);
    if (Serial.available() > 0) {
      incomingByte = Serial.read();
      if (incomingByte == 't')break;
    }
  }
  origin = 1;
  
  for (int i=0;i<50;i++){      //dealy for platform turn around
    delay(100);
    if (post_module_state == 1){
      break;
    }
  }
  
  for (int i=0;i<24;i++){      //dealy for correct platform position
    delay(100);
  }

  digitalWrite(UV_motor,LOW);     // if the sensor NG, motor could be stopped
  Serial.println("OK");
  origin = 0;  
}

void UV_door_open()
{
  if (light_state == 1){
    if (digitalRead(UV_door)==LOW){
      digitalWrite(UV_flu,LOW);
    }
    else{
      digitalWrite(UV_flu,HIGH);
    }
  }
}

void platform_position()
{
  if (origin == 1){
    post_module_state = 1;
    origin = 0;
  }
}
