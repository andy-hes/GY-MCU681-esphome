import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    CONF_TEMPERATURE,
    CONF_HUMIDITY,
    CONF_PRESSURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_HECTOPASCAL,
    UNIT_PERCENT,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ATMOSPHERIC_PRESSURE,
)

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor"]

CONF_IAQ = "iaq"
CONF_IAQ_ACCURACY = "iaq_accuracy"
CONF_GAS_RESISTANCE = "gas_resistance"
CONF_ALTITUDE = "altitude"

mcu680_ns = cg.esphome_ns.namespace("mcu680")
MCU680Component = mcu680_ns.class_("MCU680Component", cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MCU680Component),
        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_HUMIDITY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_PRESSURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_HECTOPASCAL,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_ATMOSPHERIC_PRESSURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_IAQ): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_IAQ_ACCURACY): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
            entity_category="diagnostic",
        ),
        cv.Optional(CONF_GAS_RESISTANCE): sensor.sensor_schema(
            unit_of_measurement="kΩ",
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ALTITUDE): sensor.sensor_schema(
            unit_of_measurement="m",
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if conf := config.get(CONF_TEMPERATURE):
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_temperature_sensor(sens))

    if conf := config.get(CONF_HUMIDITY):
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_humidity_sensor(sens))

    if conf := config.get(CONF_PRESSURE):
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_pressure_sensor(sens))

    if conf := config.get(CONF_IAQ):
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_iaq_sensor(sens))

    if conf := config.get(CONF_IAQ_ACCURACY):
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_iaq_accuracy_sensor(sens))

    if conf := config.get(CONF_GAS_RESISTANCE):
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_gas_resistance_sensor(sens))

    if conf := config.get(CONF_ALTITUDE):
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_altitude_sensor(sens))
