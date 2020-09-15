#pragma once

#include "esphome/core/component.h"
#include "esphome/core/esphal.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/voltage_sampler/voltage_sampler.h"

namespace esphome {
namespace adcp {

class ADCPSensor;

class ADCPComponent : public Component {
 public:
  void dump_config() override;

  void set_source(voltage_sampler::VoltageSampler *source) { source_ = source; }
  voltage_sampler::VoltageSampler* get_source() { return this->source_; }

  float get_setup_priority() const override { return setup_priority::DATA; }

 protected:
  voltage_sampler::VoltageSampler *source_;
};

class ADCPSensor : public sensor::Sensor, public PollingComponent {
 public:
  ADCPSensor(ADCPComponent *parent) : parent_(parent) {}
  void set_power_pin(GPIOPin *power_pin) { this->power_pin_ = power_pin; }
  void set_delay(uint8_t delay) { this->delay_ = delay; }

  uint8_t get_delay() const { return this->delay_; }

  void update() override;

 protected:
  ADCPComponent *parent_;
  GPIOPin *power_pin_;
  uint8_t delay_;
};


}  // namespace adcp
}  // namespace esphome
