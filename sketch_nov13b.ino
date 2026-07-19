#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

MPU6050 mpu;

#define INTERRUPT_PIN 2
#define r1 3
#define r2 5
#define l1 6
#define l2 9
int spl = 150;
int spr = 0.975*spl;
//93
const char* inputString = "a920a920a920a920"; //will be changed by python program
int index = 0; 
bool neg = false;

bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// CRUCIAL orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };
volatile bool mpu_interrupt = false;   

bool mpu_active = false;
float target_yaw = 0;

bool wait = false;
const int IN1 = 13;
const int IN2 = 12;
const int ENA = 11;


void dmpDataReady() {
  mpu_interrupt = true;
}

void setup() {
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
      Wire.setClock(400000); 
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
  #endif

  Serial.begin(115200);
  while (!Serial);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  

  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(l1, OUTPUT);
  pinMode(l2, OUTPUT);
  analogWrite(r1, 0);
  analogWrite(r2, 0);
  analogWrite(l1, 0);
  analogWrite(l2, 0);
  pinMode(INTERRUPT_PIN, INPUT);
  delay(5000);
}
void process_commands(){
  char c = inputString[index++];
    if (c == '\0') return;

    bool negative = false;
    if (inputString[index] == '-') { 
      negative = true; 
      index++; 
      }
    long value = 0;
    while (isdigit(inputString[index])) {
        value = value * 10 + (inputString[index++] - '0');
    }
    if (negative) value = -value;

    switch (c) {
        case 'f':
            delay(100);
            analogWrite(r1, 0);
            analogWrite(r2, spr);
            analogWrite(l1, 0);
            analogWrite(l2, spl);
            delay(value);
            analogWrite(r1, 0);
            analogWrite(r2, 0);
            analogWrite(l1, 0);
            analogWrite(l2, 0);
            delay(50);
            break;
        case 'w':
            delay(100);
            digitalWrite(IN1, HIGH);
            digitalWrite(IN2, LOW);
            analogWrite(ENA, 125);
            delay(value/5);
            digitalWrite(IN1, HIGH);
            digitalWrite(IN2, LOW);
            analogWrite(ENA, 125);
            delay(50);
            break;
        case 'b':
            delay(100);
            analogWrite(r1, spr);
            analogWrite(r2, 0);
            analogWrite(l1, spl);
            analogWrite(l2, 0);
            delay(value);
            analogWrite(r1, 0);
            analogWrite(r2, 0);
            analogWrite(l1, 0);
            analogWrite(l2, 0);
            delay(50);
            break;
        case 'a':
            delay(100);
            target_yaw = value/10;
            neg = (value < 0);  
            startMPU();
            wait = true;
            break;
    }
}
void loop() {
  if (mpu_active && dmpReady) {
    if (mpu_interrupt) {
      mpu_interrupt = false;
      if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
        mpu.dmpGetQuaternion(&q, fifoBuffer);
        mpu.dmpGetGravity(&gravity, &q);
        mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
        float yaw = ypr[0] * 180.0 / M_PI;
        Serial.print(F("Yaw: "));
        Serial.println(yaw);
        if (neg){ 
          analogWrite(r1, 0);
          analogWrite(r2, spr);
          analogWrite(l1, spl);
          analogWrite(l2, 0);
        }
        else{
          analogWrite(r1, spr);
          analogWrite(r2, 0);
          analogWrite(l1, 0);
          analogWrite(l2, spl);
        }
        
        if (abs(target_yaw-yaw) <= 1) {
          analogWrite(r1, 0);
          analogWrite(r2, 0);
          analogWrite(l1, 0);
          analogWrite(l2, 0);
          stopMPU();
          wait = false;
        }
      }
    }
    return; 
  }

  if (inputString[index] != '\0') {
    process_commands();
  } 
  else {
      Serial.println(F("done"));
      while (1);
  }
}

void startMPU() {
  mpu_interrupt = false;
  mpu.initialize();
  devStatus = mpu.dmpInitialize();

  mpu.setXGyroOffset(220);
  mpu.setYGyroOffset(76);
  mpu.setZGyroOffset(-85);
  mpu.setZAccelOffset(1788); 

  if (devStatus == 0) {
      mpu.CalibrateAccel(6);
      mpu.CalibrateGyro(6);
      mpu.PrintActiveOffsets();

      Serial.println(F("Enabling DMP..."));
      mpu.setDMPEnabled(true);

      Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
      Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
      Serial.println(F(")..."));
      attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
      mpuIntStatus = mpu.getIntStatus();

      Serial.println(F("DMP ready! Waiting for first interrupt..."));
      dmpReady = true;

      packetSize = mpu.dmpGetFIFOPacketSize();
      mpu_active = true;
  }
}

void stopMPU() {
  detachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN));
  mpu.setDMPEnabled(false);  
  mpu.resetFIFO();         
  mpu.reset();               
  delay(100);                   
  Serial.println("MPU is stopped!!\n");
  mpu_active = false;
}
