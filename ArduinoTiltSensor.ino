// constants won't change. They're used here to set pin numbers:
const int tiltPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int tiltState = 0;         // variable for reading the pushbutton status

void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(tiltPin, INPUT);
  // setup serial library
  Serial.begin(9600);
}

void loop() {

  //reasonable delay
  delay(250);
  
  // read the state of the pushbutton value:
  tiltState = digitalRead(tiltPin);

  if (tiltState == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
  }
}

void serialEvent()
{
   while(Serial.available()) 
   {
     char ch = Serial.read();
     if(ch = ':'){
      Serial.println(tiltState);
     } else {
      Serial.println(-1);
     }
   }
}
