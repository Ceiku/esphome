#pragma once

#include <EloquentTinyML.h>
#include "esphome/core/component.h"
#include "esphome/core/esphal.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace tfmicro {

template<size_t inputSize, size_t outputSize, size_t tensorArenaSize>
class TFMicroSensor : public sensor::Sensor, public PollingComponent {
 public:
  template<size_t inputSize, size_t outputSize, size_t tensorArenaSize>
  TFMicroSensor<inputSize, outputSize, tensorArenaSize>::TFMicroSensor() {}
  void set_sensor(sensor::Sensor *sensor) { this->sensor_ = sensor; }
  void set_model(unsigned char *model) { this->model_ = model; }
  void set_resolvers(std::string *resolvers) { this->resolvers_ = resolvers; }

  // void set_ml() { this->ml_ = new Eloquent::TinyML::TfLite<inputSize, outputSize, tensorArenaSize>(); }
  void set_ml(Eloquent::TinyML::TfLite<inputSize, outputSize, tensorArenaSize> *ml) { this->ml_ = ml; }

  void setup() override { 
    // this->ml->begin(this->model_);
  }

  void update() override {
    // auto predicted = this->ml->predict({ this->sensor_->sample() });
    // this->publish_state(predicted);
  }

 protected:
  Eloquent::TinyML::TfLite<inputSize, outputSize, tensorArenaSize> *ml_{nullptr};
  sensor::Sensor *sensor_;
  unsigned char *model_;
  std::string *resolvers_;
};

}  // namespace tfmicro
}  // namespace esphome
