int sensor = A0;   
int valor = 0;  

int ledON = 11;
int ledOFF = 12;
int led_estado = false;


void setup() {
  pinMode(2, OUTPUT); 
  Serial.begin(9600); 

  pinMode(11, OUTPUT);
  
}

void loop() {
  valor = analogRead(sensor);    
  Serial.println(valor); 

  if(Serial.available()>0) {
    int v = Serial.readString().toInt();

    if (v==ledON){
      digitalWrite(11, true);
    }

    if (v==ledOFF){
      digitalWrite(11, false);
    }

  }

  
  delay(1000);
}