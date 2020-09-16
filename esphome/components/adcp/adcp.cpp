#include "adcp.h"
#include "esphome/core/log.h"

namespace esphome {
namespace adcp {

static const char *TAG = "ADCP";

void ADCPComponent::dump_config() { ESP_LOGCONFIG(TAG, "Setting up ADCP..."); }

void ADCPSensor::update() {
  this->power_pin_->digital_write(true);
  this->set_timeout("sensor_power_on", this->delay_, this->complete_update);
}

void ADCPSensor::complete_update() {
  float state = this->parent_->get_source()->sample();
  this->power_pin_->digital_write(false);
  this->publish_state(state);
}

}  // namespace adcp
}  // namespace esphome
