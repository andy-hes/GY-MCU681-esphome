import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, sensor
from esphome.const import CONF_ID

DEPENDENCIES = ["uart"]

mcu680_ns = cg.esphome_ns.namespace("mcu680")
MCU680Component = mcu680_ns.class_("MCU680Component", cg.Component, uart.UARTDevice)

CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"
CONF_PRESSURE = "pressure"
CONF_IAQ = "iaq"
CONF_IAQ_ACCURACY = "iaq_accuracy"
CONF_GAS = "gas_resistance"
CONF_ALTITUDE = "altitude"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MCU680Component),

        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement="°C",
            accuracy_decimals=1,
            device_class="temperature",
            state_class="measurement",
        ),
        cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
            unit_of_measurement="%",
            accuracy_decimals=1,
            device_class="humidity",
            state_class="measurement",
        ),
        cv.Optional(CONF_PRESSURE): sensor.sensor_schema(
            unit_of_measurement="hPa",
            accuracy_decimals=2,
            device_class="pressure",
            state_class="measurement",
        ),
        cv.Optional(CONF_IAQ): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class="measurement",
        ),
        cv.Optional(CONF_IAQ_ACCURACY): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class="measurement",
        ),
        cv.Optional(CONF_GAS): sensor.sensor_schema(
            unit_of_measurement="kΩ",
            accuracy_decimals=1,
            state_class="measurement",
        ),
        cv.Optional(CONF_ALTITUDE): sensor.sensor_schema(
            unit_of_measurement="m",
            accuracy_decimals=0,
            state_class="measurement",
        ),
    }
).extend(uart.UART_DEVICE_SCHEMA).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))

    if CONF_HUMIDITY in config:
        sens = await sensor.new_sensor(config[CONF_HUMIDITY])
        cg.add(var.set_humidity_sensor(sens))

    if CONF_PRESSURE in config:
        sens = await sensor.new_sensor(config[CONF_PRESSURE])
        cg.add(var.set_pressure_sensor(sens))

    if CONF_IAQ in config:
        sens = await sensor.new_sensor(config[CONF_IAQ])
        cg.add(var.set_iaq_sensor(sens))

    if CONF_IAQ_ACCURACY in config:
        sens = await sensor.new_sensor(config[CONF_IAQ_ACCURACY])
        cg.add(var.set_iaq_accuracy_sensor(sens))

    if CONF_GAS in config:
        sens = await sensor.new_sensor(config[CONF_GAS])
        cg.add(var.set_gas_sensor(sens))

    if CONF_ALTITUDE in config:
        sens = await sensor.new_sensor(config[CONF_ALTITUDE])
        cg.add(var.set_altitude_sensor(sens))
