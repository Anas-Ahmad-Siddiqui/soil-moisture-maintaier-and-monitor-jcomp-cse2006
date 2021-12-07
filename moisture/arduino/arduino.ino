int sensor_pin = A0;
int solenoid = 4;

int output_value ;
int data;

void setup() {
   pinMode(solenoid, OUTPUT);
   Serial.begin(9600);
   delay(1000);
   }

void loop() {

   output_value= analogRead(sensor_pin);
   data = map(output_value, 511, 445, 5, 75);
   Serial.print(data);
   //Serial.print("20");
   Serial.print("\n");

  if(output_value < 30){
    digitalWrite(solenoid, HIGH);
  }
  else{
    digitalWrite(solenoid, LOW);
  }
  delay(1000);
}
