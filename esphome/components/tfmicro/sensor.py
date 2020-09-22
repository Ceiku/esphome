import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_SENSOR, CONF_ID, UNIT_PERCENT, ICON_BRAIN, ESP_PLATFORM_ESP32

ESP_PLATFORMS = [ESP_PLATFORM_ESP32]

IS_PLATFORM_COMPONENT = True

CONF_INPUT_SIZE = 'input_size'
CONF_OUTPUT_SIZE = 'output_size'
CONF_TENSOR_ARENA_SIZE = 'tensor_arena_size'
CONF_RESOLVERS = 'resolvers'

tfmicro_ns = cg.esphome_ns.namespace('tfmicro')
TFMicroSensor = tfmicro_ns.class_('TFMicroSensor', sensor.Sensor, cg.PollingComponent)

CONFIG_SCHEMA = sensor.sensor_schema(UNIT_PERCENT, ICON_BRAIN, 3).extend({
    cv.GenerateID(): cv.declare_id(TFMicroSensor),
    cv.Required(CONF_SENSOR): cv.use_id(sensor.Sensor),
    cv.Required(CONF_MODEL): cv.ensure_list(cv.hex_uint8_t),
    
    cv.Optional(CONF_RESOLVERS, default=[]): cv.ensure_list(cv.string_strict),
    cv.Optional(CONF_INPUT_SIZE, default=1): cv.positive_not_null_int,
    cv.Optional(CONF_OUTPUT_SIZE, default=1): cv.positive_not_null_int,
    cv.Optional(CONF_TENSOR_ARENA_SIZE, default=2048): cv.positive_not_null_int,
}).extend(cv.polling_component_schema('60s'))

def to_code(config):
  template = cg.TemplateArguments(config[CONF_INPUT_SIZE], config[CONF_OUTPUT_SIZE], config[CONF_TENSOR_ARENA_SIZE])

  tfm_type = TFMicroSensor.template(template)
  rhs = tfm_type.new()

  var = cg.new_Pvariable(config[CONF_ID], rhs, tfm_type)
  yield cg.register_component(var, config)
  yield sensor.register_sensor(var, config)

  sens = yield cg.get_variable(config[CONF_SENSOR])
  resolvers = yield cg.get_variable(config[CONF_RESOLVERS])
  
  cg.add(var.set_sensor(sens))
  cg.add(var.set_resolvers(resolvers))
  cg.add_library('EloquentTinyML', '0.0.2')

    
