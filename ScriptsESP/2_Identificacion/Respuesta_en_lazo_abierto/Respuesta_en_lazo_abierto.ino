#include "motorControl.h"
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

/////////////////////// TIEMPO DE MUESTREO /////////////////////
unsigned long lastTime = 0, sampleTime = 100;

///////////////////// COMUNICACION SERIAL ////////////////
String inputString = "";
bool stringComplete = false;
const char separator = ',';
const int dataLength = 2;
int datos[dataLength];

//////////////////////MOTOR DERECHO/////////////////////////////// 
motorControl motorR(sampleTime);
const int    C1R = 39;    // Entrada de la señal A del encoder C1(cable amarillo)
const int    C2R = 36;    // Entrada de la señal B del encoder C2(cable verde)

// Encoder
volatile int nR = 0;
volatile int antR      = 0;
volatile int actR      = 0;

// Driver
const int   ENA = 32;  
const int   IN1 = 33; 
const int   IN2 = 25; 

int channelMotorR = 0;

// Variables
int cvR = 0;
double wR = 0;


//////////////////////MOTOR IZQUIERDO///////////////////////////////
motorControl motorL(sampleTime);
const int    C1L = 35;  // Entrada de la señal A del encoder.
const int    C2L = 34;  // Entrada de la señal B del encoder.

// Encoder
volatile int nL = 0;
volatile int antL      = 0;
volatile int actL      = 0; 


// Driver
const int   IN3 = 26;  
const int   IN4 = 27; 
const int   ENB = 14; 

int channelMotorL = 1;

// Variables
int cvL = 0;
double wL = 0;


//////// VARIABLES PARA CALCULAR VELOCIDADES ANGULARES /////////
double constValue = 1.315584713; // (1000*2*pi)/R ---> R = 1496.88 - 350RPM Resolucion encoder cuadruple


// Configuracion de las salidas pwm
const int freq = 10000;
const int resolution = 8;

/////////////////////// INTERRUPCIONES //////////////////////
void IRAM_ATTR encoderR()
{
  antR=actR;
               
  if(digitalRead(C2R)) bitSet(actR,0); else bitClear(actR,0);
  if(digitalRead(C1R)) bitSet(actR,1); else bitClear(actR,1);
  
  
  if(antR == 2 && actR ==0) nR++;
  if(antR == 0 && actR ==1) nR++;
  if(antR == 3 && actR ==2) nR++;
  if(antR == 1 && actR ==3) nR++;
  
  if(antR == 1 && actR ==0) nR--;
  if(antR == 3 && actR ==1) nR--;
  if(antR == 0 && actR ==2) nR--;
  if(antR == 2 && actR ==3) nR--;     

}
void IRAM_ATTR encoderL()
{
  antL=actL;
               
  if(digitalRead(C2L)) bitSet(actL,0); else bitClear(actL,0);
  if(digitalRead(C1L)) bitSet(actL,1); else bitClear(actL,1);
  
  
  if(antL == 2 && actL ==0) nL--;
  if(antL == 0 && actL ==1) nL--;
  if(antL == 3 && actL ==2) nL--;
  if(antL == 1 && actL ==3) nL--;
  
  if(antL == 1 && actL ==0) nL++;
  if(antL == 3 && actL ==1) nL++;
  if(antL == 0 && actL ==2) nL++;
  if(antL == 2 && actL ==3) nL++;    
}

void setup()
{
  SerialBT.begin("Robot_movil_autonomo_esp32"); 

  // Configuracion de los pines
  pinMode(C1R, INPUT);
  pinMode(C2R, INPUT);
  pinMode(C1L, INPUT);
  pinMode(C2L, INPUT);

  
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

   // Driver
  ledcSetup(channelMotorR,freq, resolution);
  ledcAttachPin(ENA,channelMotorR);
  
  ledcSetup(channelMotorL,freq, resolution);
  ledcAttachPin(ENB,channelMotorL);

  parar(IN1,IN2,ENA);
  parar(IN4,IN3,ENB);

  // Interrupciones

  attachInterrupt(C1R, encoderR, CHANGE);
  attachInterrupt(C2R, encoderR, CHANGE);

  attachInterrupt(C1L, encoderL, CHANGE);
  attachInterrupt(C2L, encoderL, CHANGE); 

  ////////////////// Limites de señales //////////////////
  motorR.setCvLimits(255,0);
  motorR.setPvLimits(5,1);
  
  ////////////////// Limites de señales //////////////////
  motorL.setCvLimits(255,0);
  motorL.setPvLimits(5,1);
  
  lastTime = millis();
     
}
void loop() 
{
  if(SerialBT.available()) serialEvent();
  
  ////////// SI RECIBE DATOS /////////////
  if (stringComplete) 
  {
    for (int i = 0; i < dataLength ; i++)
    {
      int index = inputString.indexOf(separator);
      datos[i] = inputString.substring(0, index).toInt();
      inputString = inputString.substring(index + 1);
     }

     cvR = motorR.scaleCv(datos[0]);
     if(cvR > 0) giroHorario(IN1,IN2,channelMotorR,cvR); else if (cvR<0) giroAntihorario(IN1,IN2,channelMotorR,abs(cvR)); else parar(IN1,IN2,channelMotorR);
 
     cvL = motorL.scaleCv(datos[1]);
     if(cvL > 0) giroAntihorario(IN4,IN3,channelMotorL,cvL); else if (cvL<0) giroHorario(IN4,IN3,channelMotorL,abs(cvL)); else parar(IN4,IN3,channelMotorL);
 
     
     inputString = "";
     stringComplete = false;
  }
 
  if(millis()-lastTime >= sampleTime)
  {
    
    wR = constValue*nR/(millis()-lastTime); // Velocidad angular del lado derecho [rad/s]
    wL = constValue*nL/(millis()-lastTime); // Velocidad angular del lado izquierdo [rad/s]
    lastTime = millis();

    wR = motorR.scalePv(wR);
    wL = motorL.scalePv(wL);
    
    nR = 0;
    nL = 0;
    
    SerialBT.println("E");
    SerialBT.println(wR);
    SerialBT.println(wL);
 
  }
  
}

/////////////// RECEPCION DE DATOS /////////////////////
void serialEvent() {
  while (SerialBT.available()) {
    char inChar = (char)SerialBT.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void parar(int _in1,int _in2,int _en)
{
  digitalWrite(_in1,HIGH);
  digitalWrite(_in2,HIGH);
  digitalWrite(_en,HIGH);
}

void giroAntihorario(int _in1,int _in2, int _en, int cv)
{
    
  digitalWrite(_in1,HIGH);
  digitalWrite(_in2,LOW);
  ledcWrite(_en,cv);
  
}

void giroHorario(int _in1,int _in2, int _en, int cv)
{
    
  digitalWrite(_in1,LOW);
  digitalWrite(_in2,HIGH);
  ledcWrite(_en,cv);

}
