#include <STM32Encoder.h>

const float diameter = 55.0; //mm
const float mm2pulse = 8993.050059 / diameter;
const float kp = 25.5;
const float ki = 1;
const float kd = 300;
const float speed_ind = 1;
const uint8_t dt = 1; //ms

class mtdrv
{
public:
  mtdrv(const int _TIMXCHX, const int _TIMXCHXN, STM32Encoder *encarg);

  void forward(uint16_t dutycycle);
  void backward(uint16_t dutycycle);
  void forwardN(uint16_t dutycycle);
  void backwardN(uint16_t dutycycle);
  void init();
  void initN();
  void mmtopulse();

  long target_mm = 0;
  long target_pulse = 0;
  float pwm;
  float cacheerror = 0;
  float pid_p, pid_d, error;
  float pid_i = 0;
  STM32Encoder *enc;

private:
  uint8_t TIMXCHX;
  uint8_t TIMXCHXN;
};

mtdrv::mtdrv(const int _TIMXCHX,const int _TIMXCHXN, STM32Encoder *encarg)
{
  TIMXCHX = _TIMXCHX;
  TIMXCHXN = _TIMXCHXN;
  enc = encarg;
}

void mtdrv::init()
{
  pinMode(TIMXCHX, PWM);
  pinMode(TIMXCHXN, OUTPUT);
}

void mtdrv::initN()
{
  pinMode(TIMXCHX, PWM);
  pinMode(TIMXCHXN, PWM);
}

void mtdrv::forward(uint16_t dutycycle)
{
  pwmWrite(TIMXCHX, dutycycle);
  digitalWrite(TIMXCHXN, LOW);
}

void mtdrv::backward(uint16_t dutycycle)
{
  pwmWrite(TIMXCHX, dutycycle);
  digitalWrite(TIMXCHXN, HIGH);
}

void mtdrv::forwardN(uint16_t dutycycle)
{
  pwmWrite(TIMXCHX, dutycycle);
  pwmWrite(TIMXCHXN, 0);
}

void mtdrv::backwardN(uint16_t dutycycle)
{
  pwmWrite(TIMXCHXN, dutycycle);
  pwmWrite(TIMXCHX, 0);
}

void mtdrv::mmtopulse()
{
  this->target_pulse = (this->target_mm * mm2pulse);
}