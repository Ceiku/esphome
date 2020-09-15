import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import sensor
from esphome.const import CONF_PIN, CONF_DELAY, ICON_FLASH, UNIT_VOLT, CONF_ID
from . import ADCPComponent, adcp_ns


DEPENDENCIES = ['adcp']

ADCPSensor = adcp_ns.class_('ADCPSensor', sensor.Sensor, cg.PollingComponent)

CONF_ADCP_ID = 'adcp_id'

CONFIG_SCHEMA = sensor.sensor_schema(UNIT_VOLT, ICON_FLASH, 3).extend({
    cv.GenerateID(): cv.declare_id(ADCPSensor),
    cv.GenerateID(CONF_ADCP_ID): cv.use_id(ADCPComponent),
    cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
    cv.Optional(CONF_DELAY, default='100ms'): cv.positive_time_period_milliseconds,
}).extend(cv.polling_component_schema('60s'))


def to_code(config):
    paren = yield cg.get_variable(config[CONF_ADCP_ID])
    var = cg.new_Pvariable(config[CONF_ID], paren)
    yield cg.register_component(var, config)
    yield sensor.register_sensor(var, config)

    power_pin = yield cg.gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_power_pin(power_pin))

    cg.add(var.set_delay(config[CONF_DELAY]))
