#include <LiquidCrystal.h>
#include <AccelStepper.h>

#define HALFSTEP   8 // Halfstep (4096 Steps per output shaft revolution)
#define motorPin1  5 // Motor Pin 1
#define motorPin2  4 // Motor Pin 2
#define motorPin3  3 // Motor Pin 3
#define motorPin4  2 // Motor Pin 4
#define lgr 7     // Led Green 
#define lro 8     // Led Red
#define B_up 10   // Button Up 
#define B_down 11 // Button Down
#define B_ent 13  // Enter Button

int steps = 16; 
int pos = 0;    // Position 
int run = 0;     // Cycle is running when 1
int E_val= 0;    // Entered Value of Steps
int step_nr = 0; // The number of the actual processing Step


LiquidCrystal lcd(42, 44, 46, 48, 50, 52);
AccelStepper stepper(HALFSTEP, motorPin1, motorPin3, motorPin2, motorPin4);

void setup() 
{   
    pinMode(B_up, INPUT_PULLUP);
    pinMode(B_down, INPUT_PULLUP);
    pinMode(B_ent, INPUT_PULLUP);
    pinMode(lgr, OUTPUT);
    pinMode(lro, OUTPUT);
    stepper.setMaxSpeed(1200.0);    //Stepper Maxspeed
    stepper.setAcceleration(200.0); //Stepper Acceleration
    stepper.setSpeed(800);          // Stepper Speed
    lcd.begin(16, 2);               
    lcd.setCursor(4,0);
    lcd.print ("3D Scan");
    lcd.setCursor(4,1);
    lcd.print("Stefano P.");
    delay(3000);
    lcd.clear();
    lcd.print ("Number of Steps:");
    lcd.noCursor();
}

void loop() 
{ 
  if (digitalRead(B_ent) == 0) // Start
  {
      run = 1 ;
  }
  
  if(digitalRead(B_up) == LOW && steps < 64 && run == 0) // up button
    {
      steps = steps * 2; 
        
  while (digitalRead(B_up) == LOW); 
    }
    
  if(digitalRead(B_down) == LOW && steps > 15 && run == 0)  // down button
    {  
      steps = steps / 2;
      
    while (digitalRead(B_down) == LOW);
    }
    
  if (run == 1)                                      // LCD Progress of the steps
  {
    lcd.setCursor(5,1);
    lcd.print(step_nr);
    lcd.print("/"); 
    lcd.print(steps);
  }
    else                                            // LCD choice of how many Steps
    {
     lcd.setCursor(7,1);
     lcd.print(steps);
     lcd.print(" ");
    }
  if (stepper.currentPosition() < 4095 && run == 1)
  {
    stepper.runToNewPosition(pos);                
    delay(1000);
    
    Serial.begin(9600);
    Serial.println("CAPTURE");                      //Signal raspberry to take a picture
    delay(2000);
    E_val = (4096 / steps);                         // Calculation to know how many steps the stepper has to make
    pos = pos + E_val;                              // Calculation to know the new position for the next step
    step_nr = step_nr +1;                           // How many steps were made
   
  }
  if (stepper.currentPosition() >= 4096)            // Resetting the parameters for a new cycle
  {
    run = 0;
    pos = 0;
    stepper.setCurrentPosition(0);
    step_nr = 0;
    lcd.clear();
    lcd.setCursor(6,0);
    lcd.print("DONE");
    delay(2000);
    lcd.clear();
    lcd.home();
    lcd.print ("Number of Steps:");
  }
  if (run == 0)                                     //Ready LED
  {
    digitalWrite(lgr, HIGH);
    digitalWrite(lro, LOW);
    step_nr == 0;
  }
  if (run == 1)                     //In Progress LED
  {
    digitalWrite(lro, HIGH);
    digitalWrite(lgr, LOW);
  }
  
      
}


