#include <ArduinoJson.h>

#define DIR_PIN     3
#define STEP_PIN    4
#define ENABLE_PIN  5
#define MAX_PERIOD  7800 // If the period is any faster, issues occur

#define EMPTY_JSON    "{\"start\": 0,\"steps\": 0,\"period\": 0,\"motor\": 0, \"dir\":0}"
#define ERROR_PERIOD  "{\"start\": 0,\"steps\": 0,\"period\": 999,\"motor\": 0, \"dir\":0}"

long period = 0;
long steps = 0;
volatile long currSteps = 0;
bool start = false;
bool stop = false;
bool motor = false;
bool toggle = false;
bool dir = true;
StaticJsonDocument<96> data;

void parseData(void);
void setupTimerInt(void);
void disableTimerInt(void);
void enableTimerInt(void);
void disableMotor(void);
void enableMotor(void);

void setup() {
  // put your setup code here, to run once:
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  
  digitalWrite(DIR_PIN, LOW);
  digitalWrite(STEP_PIN, LOW);
  disableMotor(); // Default to disabled motor
  
  Serial.begin(115600);
//  Serial.println("Setup Done!");
}

void loop() {
  if(Serial.available())
    parseData();
  
  if(start) {
    start = false;
    currSteps = 0;
    enableMotor();
    enableTimerInt();
  } 
  if(stop) {
    disableTimerInt();
  }
}

/**
 * @brief   Parses JSON data and sets the correct values.
 *          If there is an error in the JSON data then it 
 *          will send an empty JSON string back.
 */
void parseData(void) {
  String JSON = "";
  char temp = '\0';
  
  while(Serial.available()) {
    temp = Serial.read();
    JSON += String(temp);
    delay(1); // Give some time for the entire JSON to come in
  }
  
  DeserializationError error = deserializeJson(data, JSON);
  if(error) {
    Serial.print(EMPTY_JSON); // Send empty JSON to signal that data didn't come accross well
    return;
  }
  
  long tPeriod = data["period"];
  start = data["start"];
  long tSteps = data["steps"];
  motor = data["motor"];
  dir = data["dir"];
  
  // Return an error if ther period received is above the max 
  if(tPeriod > MAX_PERIOD) { 
    Serial.print(ERROR_PERIOD);
    start = false;
  }

  if(tSteps != 0) 
    steps = tSteps;
  if(tPeriod != 0)
    period = tPeriod;

  if(motor)
    enableMotor();
  else
    disableMotor();
    
  stop = !start;
  digitalWrite(DIR_PIN, dir);

  Serial.print(JSON); // Send JSON back to signal that data was received correctly
  setupTimerInt();
}

/**
 * @brief   Sets up the interrupt that will control the 
 *          speed of the stepper motor
 */
void setupTimerInt(void) {
//  Serial.println("Setting up timer");
  if(period == 0) { // If there is no period, then we aren't going to move
    disableTimerInt();
    return;
  }
  
  //set timer1 interrupt at 1Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 15625/period - 1;
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);
}

/** 
 * @brief   Disables timer interrupt causing the motor to stop moving
 */
void disableTimerInt(void) {
//  Serial.println("Disable TIM INT");
  TIMSK1 &= ~(1 << OCIE1A);
}

/** 
 * @brief   Enables timer interrupt causing the motor to start moving
 */
void enableTimerInt(void) {
//  Serial.println("Enable TIM INT");
  TIMSK1 |= (1 << OCIE1A);
}

/**
 * @brief   Disables motor so that it can be moved freely
 */
void disableMotor(void) {
  // Low asserted enable
  digitalWrite(ENABLE_PIN, HIGH);
}

/**
 * @brief   Enables motor locking it in place
 */
void enableMotor(void) {
  // Low asserted enable
  digitalWrite(ENABLE_PIN, LOW);
}

/**
 * @brief   Interrupt that controls the motor and determines 
 *          when it has finished running
 */
ISR(TIMER1_COMPA_vect){
  if(toggle){
    digitalWrite(STEP_PIN, LOW);
    toggle = false;
  } else {
    digitalWrite(STEP_PIN, HIGH);
    toggle = true;
  }
  currSteps++;
  if(currSteps == steps){
    disableTimerInt();
    disableMotor();
    Serial.println("Done");
  }
}
