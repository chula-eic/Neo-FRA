const float pitch_radius = 20; //mm

class msgprc
{
public:
  msgprc(mtdrv *chx, mtdrv *chy, mtdrv *chz);
  String strmsg;
  String sbuffer;
  void receive_auto();
  void receive_manual();
  void showStatus_auto();
  void storeValue_auto();
  void cartesian2omni_t(long *r, long x, long y);
  long cartesian2omni_r(float z);
  short v[2];
  float z;

private:
  mtdrv *mtdrv1;
  mtdrv *mtdrv2;
  mtdrv *mtdrv3;
};
msgprc::msgprc(mtdrv *chX, mtdrv *chY, mtdrv *chZ)
{
  mtdrv1 = chX;
  mtdrv2 = chY;
  mtdrv3 = chZ;
}

void msgprc::receive_auto()
{
  if (Serial.available())
  {
    if (sbuffer[0] != '!')
    {
      sbuffer = "";
    }
    msgprc::sbuffer += static_cast<char>(Serial.read());
    if (sbuffer[0] == '!')
    {
      if (sbuffer.length() == 16)
      {
        this->strmsg = sbuffer;
        msgprc::storeValue_auto();
        msgprc::showStatus_auto();
        sbuffer = "";
      }
    }
  }
}

void msgprc::storeValue_auto()
{
  this->v[0] = this->strmsg.substring(2, 6).toInt();
  this->v[1] = this->strmsg.substring(7, 11).toInt();
  this->z = this->strmsg.substring(12, 16).toFloat();
  if (this->strmsg[1] == '1')
  {
    this->v[0] *= -1;
  }
  if (this->strmsg[6] == '1')
  {
    this->v[1] *= -1;
  }
  if (this->strmsg[11] == '1')
  {
    this->z *= -1;
  }
  long r_t[3];
  this->cartesian2omni_t(r_t, this->v[0], this->v[1]);
  long r_r = this->cartesian2omni_r(this->z);
  this->mtdrv1->target_mm += r_t[0] + r_r;
  this->mtdrv2->target_mm += r_t[1] + r_r;
  this->mtdrv3->target_mm += r_t[2] + r_r;
  this->mtdrv1->mmtopulse();
  this->mtdrv2->mmtopulse();
  this->mtdrv3->mmtopulse();
}

void msgprc::showStatus_auto()
{
  Serial.print("sx = ");
  Serial.println(this->v[0]);
  Serial.print("sy = ");
  Serial.println(this->v[1]);
  Serial.print("sz = ");
  Serial.println(this->z);
  Serial.print("target_mm(1) = ");
  Serial.println(this->mtdrv1->target_mm);
  Serial.print("target_mm(2) = ");
  Serial.println(this->mtdrv2->target_mm);
  Serial.print("target_mm(3) = ");
  Serial.println(this->mtdrv3->target_mm);
}
void msgprc::cartesian2omni_t(long *r, long x, long y)
{
  r[0] = -x;
  r[1] = -static_cast<long>(-0.5 * x - 0.86602540378 * y);
  r[2] = -static_cast<long>(-0.5 * x + 0.86602540378 * y);
}

long msgprc::cartesian2omni_r(float z)
{
  return -static_cast<long>(z * pitch_radius * 6.28318530718);
}
