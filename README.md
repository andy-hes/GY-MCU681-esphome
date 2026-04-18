# MCU680 / MCU681 ESPHome external component

UART external component for GY-MCU680 / GY-MCU681 style modules.

## Install in ESPHome

```yaml
external_components:
  - source: github://andy-hes/GY-MCU681-esphome
    components: [mcu680]

uart:
  id: uart_bus
  tx_pin: GPIO9
  rx_pin: GPIO10
  baud_rate: 9600

mcu680:
  id: air_sensor
  uart_id: uart_bus
  temperature:
    name: "MCU681 Temperatur"
  humidity:
    name: "MCU681 Luftfuktighet"
  pressure:
    name: "MCU681 Trykk"
  iaq:
    name: "MCU681 IAQ"
  iaq_accuracy:
    name: "MCU681 IAQ Accuracy"
  gas_resistance:
    name: "MCU681 Gassmotstand"
  altitude:
    name: "MCU681 Høyde"
```

## Notes

- Temperature and humidity default to 1 decimal.
- Pressure defaults to 2 decimals.
- Gas resistance is published in kΩ.
- Altitude is derived by the module from pressure and can drift.
