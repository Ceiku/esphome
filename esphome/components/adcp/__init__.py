import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import voltage_sampler
from esphome.const import CONF_SENSOR, CONF_ID


AUTO_LOAD = ['voltage_sampler']
MULTI_CONF = True

adcp_ns = cg.esphome_ns.namespace('adcp')
ADCPComponent = adcp_ns.class_('ADCPComponent', cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(ADCPComponent),
    cv.Required(CONF_SENSOR): cv.use_id(voltage_sampler.VoltageSampler),
}).extend(cv.COMPONENT_SCHEMA)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)

    sens = yield cg.get_variable(config[CONF_SENSOR])
    cg.add(var.set_source(sens))
