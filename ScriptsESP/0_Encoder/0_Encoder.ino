#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

// Configuración pines motor derecho
const int    C1R = 39;    // Entrada de la señal A del encoder C1(cable amarillo)
const int    C2R = 36;    // Entrada de la señal B del encoder C2(cable verde)

// Configuración pines Encoder
volatile int nR = 0;
volatile int antR      = 0;
volatile int actR      = 0;


// Configuración pines motor de izquierdo
const int    C1L = 35;                  // Entrada de la señal A del encoder.
const int    C2L = 34;                  // Entrada de la señal B del encoder.

// Configuración pines Encoder
volatile int nL = 0;
volatile int antL      = 0;
volatile int actL      = 0; 

//Variables de tiempo de muestreo
unsigned long lastTime = 0, sampleTime = 100;

//Interrupcion encoders
void IRAM_ATTR encoderR()
{
  antR=actR;
               
  if(digitalRead(C2R)) bitSet(actR,0); else bitClear(actR,0);
  if(digitalRead(C1R)) bitSet(actR,1); else bitClear(actR,1);
    

  if(antR == 2 && actR ==0) nR--;
  if(antR == 0 && actR ==1) nR--;
  if(antR == 3 && actR ==2) nR--;
  if(antR == 1 && actR ==3) nR--;
  
  if(antR == 1 && actR ==0) nR++;
  if(antR == 3 && actR ==1) nR++;
  if(antR == 0 && actR ==2) nR++;
  if(antR == 2 && actR ==3) nR++;   

}
void IRAM_ATTR encoderL()
{
  antL=actL;
               
  if(digitalRead(C2L)) bitSet(actL,0); else bitClear(actL,0);
  if(digitalRead(C1L)) bitSet(actL,1); else bitClear(actL,1);
  
  
  if(antL == 2 && actL ==0) nL++;
  if(antL == 0 && actL ==1) nL++;
  if(antL == 3 && actL ==2) nL++;
  if(antL == 1 && actL ==3) nL++;
  
  if(antL == 1 && actL ==0) nL--;
  if(antL == 3 && actL ==1) nL--;
  if(antL == 0 && actL ==2) nL--;
  if(antL == 2 && actL ==3) nL--;     
}

void setup()
{
  SerialBT.begin("My_Robot"); 

  // Configuracion de los pines
  pinMode(C1R, INPUT);
  pinMode(C2R, INPUT);
  pinMode(C1L, INPUT);
  pinMode(C2L, INPUT);

  // Interrupciones

  attachInterrupt(C1R, encoderR, CHANGE);
  attachInterrupt(C2R, encoderR, CHANGE);

  attachInterrupt(C1L, encoderL, CHANGE);
  attachInterrupt(C2L, encoderL, CHANGE);             

  lastTime = millis();
     
}
void loop() 
{
 
  if(millis()-lastTime >= sampleTime)
  {
    lastTime = millis();
    SerialBT.print("Derecha :");SerialBT.print(nR);SerialBT.print(", ");
    SerialBT.print("Izquierda :");SerialBT.println(nL);  
  }
  
}
