#include "tfmicro.h"
#include "esphome/core/log.h"

namespace esphome {
namespace tfmicro {

static const char *TAG = "TFMICRO";

void TFMicroSensor::setup() { this->ml->begin(this->model_); }

void TFMicroSensor::update() {
  float predicted = this->ml.predict({ this->sensor_->sample() });
  this->publish_state(predicted);
}

}  // namespace tfmicro
}  // namespace esphome
