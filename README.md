### GY-MCU680 / MCU681 ESPHome External Component
ESPHome external component for GY-MCU680 / MCU681 air quality sensors using UART.

## Why this exists
The GY-MCU680 / MCU681 modules expose environmental data over UART, but there is currently no official ESPHome integration for these devices.

This component was created to:

Enable direct integration of MCU680/681 modules with ESPHome
Decode the UART protocol used by the onboard MCU
Expose sensor values cleanly to Home Assistant
Provide a reusable and maintainable solution instead of YAML-based parsing

## Features
The component provides the following sensors:

Temperature (°C)
Humidity (%)
Pressure (hPa)
IAQ (Indoor Air Quality)
IAQ Accuracy
Gas resistance (kΩ)
Altitude (calculated from pressure)

## How it works
The MCU680/681 module outputs a fixed-length UART frame:

Header: 0x5A 0x5A
Frame length: 20 bytes
Checksum: sum of first 19 bytes (mod 256)

# This component:

Listens to UART traffic
Detects valid frames
Validates checksum
Parses sensor data
Publishes values to ESPHome
Installation

Add this to your ESPHome configuration:

external_components:
  - source: github://andy-hes/GY-MCU681-esphome
    components: [mcu680]
    
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

## Wiring
Typical connection:  
MCU681 TX → ESP32 RX  
MCU681 RX → ESP32 TX  
VCC → 3.3V or 5V (depending on module)  
GND → GND  

## Notes  
Gas resistance is reported in kΩ  
Altitude is calculated from pressure and may require calibration  
IAQ is based on the sensor’s internal algorithm  
Sensor values improve after warm-up time  
Different module variants may use slightly different firmware  

## Known limitations  
Altitude is pressure-based and can vary with weather  
IAQ values are relative, not absolute measurements  
Some MCU680/681 clones may use different frame formats  

## References  
This implementation is based on reverse engineering and existing work:  
https://github.com/avaldebe/PyPMS  
https://avaldebe.github.io/PyPMS/sensors/mcu680/ 
NodeMCU Lua implementation (protocol reference)  

## License  
MIT License
