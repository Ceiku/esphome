import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_SENSOR, CONF_ID, UNIT_PERCENT, ICON_BRAIN, ESP_PLATFORM_ESP32, CONF_MODEL
# from esphome.py_compat import text_type, binary_type, char_to_byte

DEPENDENCIES = ['sensor']
ESP_PLATFORMS = [ESP_PLATFORM_ESP32]

IS_PLATFORM_COMPONENT = True

CONF_INPUT_SIZE = 'input_size'
CONF_OUTPUT_SIZE = 'output_size'
CONF_TENSOR_ARENA_SIZE = 'tensor_arena_size'
CONF_RESOLVERS = 'resolvers'

tfmicro_ns = cg.esphome_ns.namespace('tfmicro')
TFMicroSensor = tfmicro_ns.class_('TFMicroSensor', sensor.Sensor, cg.PollingComponent)


# def validate_data(value):
#     if isinstance(value, text_type):
#         return value.encode('utf-8')
#     if isinstance(value, str):
#         return value
#     if isinstance(value, list):
#         return cv.Schema([cv.char])(value)
#     raise cv.Invalid("data must either be a string wrapped in quotes or a list of bytes")

CONFIG_SCHEMA = sensor.sensor_schema(UNIT_PERCENT, ICON_BRAIN, 3).extend({
    cv.GenerateID(): cv.declare_id(TFMicroSensor),
    cv.Required(CONF_SENSOR): cv.use_id(sensor.Sensor),
    cv.Required(CONF_MODEL):  cv.ensure_list(cv.All(cv.unsigned, cv.char)),
    cv.Optional(CONF_RESOLVERS, default='all'): cv.ensure_list(cv.string_strict),
    cv.Optional(CONF_INPUT_SIZE, default=1): cv.All(cv.uint8_t, cv.positive_not_null_int),
    cv.Optional(CONF_OUTPUT_SIZE, default=1): cv.All(cv.uint8_t, cv.positive_not_null_int),
    cv.Optional(CONF_TENSOR_ARENA_SIZE, default=2048): cv.All(cv.uint8_t, cv.positive_not_null_int),
}).extend(cv.polling_component_schema('60s'))

def to_code(config):
  template = cg.TemplateArguments(config[CONF_INPUT_SIZE], config[CONF_OUTPUT_SIZE], config[CONF_TENSOR_ARENA_SIZE])

  tfm_type = TFMicroSensor.template(template)
  rhs = tfm_type.new()
  var = cg.new_Pvariable(config[CONF_ID], rhs, tfm_type)
  
  yield cg.register_component(var, config)
  yield sensor.register_sensor(var, config)

  sens = yield cg.get_variable(config[CONF_SENSOR])

  model = config[CONF_MODEL]
    # if isinstance(model, binary_type):
    #     data = [HexInt(char_to_byte(x)) for x in data]
    # cg.add(var.set_data(model))
  
  cg.add(var.set_sensor(sens))
  cg.add(var.set_resolvers(config[CONF_RESOLVERS]))
  cg.add_library('EloquentTinyML', '0.0.2')

