#include <Arduino.h>
#include <mtdrvlib.h>
#include <msgprc.h>
#include <STM32Encoder.h>

const int TIM4CH1 = PB6;
const int TIM4CH1N = PB13;
const int TIM4CH2 = PB7;
const int TIM4CH2N = PB14;
const int TIM4CH3 = PB8;
const int TIM4CH4 = PB9;

const int TIM1CH1 = PA8;
const int TIM1CH2 = PA9;
const int TIM2CH1 = PA0;
const int TIM2CH2 = PA1;
const int TIM3CH1 = PA6; 
const int TIM3CH2 = PA7;


STM32Encoder enc1(TIMER1, COUNT_BOTH_CHANNELS, 0, 56505);
STM32Encoder enc2(TIMER2, COUNT_BOTH_CHANNELS, 0, 56505);
STM32Encoder enc3(TIMER3, COUNT_BOTH_CHANNELS, 0, 56505);

HardwareTimer timer(4);

mtdrv mtdrv1(TIM4CH1, TIM4CH1N, &enc1);
mtdrv mtdrv2(TIM4CH2, TIM4CH2N, &enc2);
mtdrv mtdrv3(TIM4CH3, TIM4CH4, &enc3);
msgprc message(&mtdrv1, &mtdrv2, &mtdrv3);

void countTurns1()
{
  if (enc1.getDirection() == 1)
    enc1.tworevs--;
  else
    enc1.tworevs++;
  //Serial.println(enc1.tworevs);
}

void countTurns2()
{
  if (enc2.getDirection() == 1)
    enc2.tworevs--;
  else
    enc2.tworevs++;
  //Serial.println(enc2.tworevs);
}

void countTurns3()
{
  if (enc3.getDirection() == 1)
    enc3.tworevs--;
  else
    enc3.tworevs++;
  //Serial.println(enc3.tworevs);
}

void positionctrl(mtdrv *mtdrvarg)
{
  mtdrvarg->error = (mtdrvarg->target_pulse - (mtdrvarg->enc->tworevs * 56505 + mtdrvarg->enc->value()));
  mtdrvarg->pid_p = mtdrvarg->error * kp;
  mtdrvarg->pid_d = (mtdrvarg->error - mtdrvarg->cacheerror) / dt * kd;
  if ((-100 < mtdrvarg->error) && (mtdrvarg->error < 100))
  {
    mtdrvarg->pid_i += ki * mtdrvarg->error;
  }
  mtdrvarg->pwm = constrain((mtdrvarg->pid_p + mtdrvarg->pid_i + mtdrvarg->pid_d), -4095 * speed_ind, 4095 * speed_ind);
  if (mtdrvarg->pwm > 0)
  {
    mtdrvarg->forward(mtdrvarg->pwm);
  }
  else
  {
    mtdrvarg->backward(-mtdrvarg->pwm);
  }
  mtdrvarg->cacheerror = mtdrvarg->error;
}

void positionctrlN(mtdrv *mtdrvarg)
{
  mtdrvarg->error = (mtdrvarg->target_pulse - (mtdrvarg->enc->tworevs * 56505 + mtdrvarg->enc->value()));
  mtdrvarg->pid_p = mtdrvarg->error * kp;
  mtdrvarg->pid_d = (mtdrvarg->error - mtdrvarg->cacheerror) / dt * kd;
  if ((-100 < mtdrvarg->error) && (mtdrvarg->error < 100))
  {
    mtdrvarg->pid_i += ki * mtdrvarg->error;
  }
  mtdrvarg->pwm = constrain((mtdrvarg->pid_p + mtdrvarg->pid_i + mtdrvarg->pid_d), -4095 * speed_ind, 4095 * speed_ind);
  if (mtdrvarg->pwm > 0)
  {
    mtdrvarg->forwardN(mtdrvarg->pwm);
  }
  else
  {
    mtdrvarg->backwardN(-mtdrvarg->pwm);
  }
  mtdrvarg->cacheerror = mtdrvarg->error;
}

void positionctrl_isr()
{
  positionctrl(&mtdrv1);
  positionctrl(&mtdrv2);
  positionctrlN(&mtdrv3);
}

void setup()
{
  Serial.begin(115200);

  timer.setPrescaleFactor(1);
  timer.setOverflow(4096);
  timer.refresh();

  mtdrv1.init();
  mtdrv2.init();
  mtdrv3.initN();

  pinMode(TIM1CH1, INPUT);
  pinMode(TIM1CH2, INPUT);
  pinMode(TIM2CH1, INPUT);
  pinMode(TIM2CH2, INPUT);
  pinMode(TIM3CH1, INPUT);
  pinMode(TIM3CH2, INPUT);
  
  enc1.attachInterrupt(countTurns1);
  enc2.attachInterrupt(countTurns2);
  enc3.attachInterrupt(countTurns3);
  systick_attach_callback(positionctrl_isr);
}

void loop()
{
  message.receive_auto();
}


