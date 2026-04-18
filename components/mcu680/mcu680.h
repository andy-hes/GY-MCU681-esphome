#pragma once

#include "esphome/core/component.h"
#include "esphome/core/log.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include <vector>

namespace esphome {
namespace mcu680 {

class MCU680Component : public Component, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;

  void set_temperature_sensor(sensor::Sensor *sensor) { temperature_sensor_ = sensor; }
  void set_humidity_sensor(sensor::Sensor *sensor) { humidity_sensor_ = sensor; }
  void set_pressure_sensor(sensor::Sensor *sensor) { pressure_sensor_ = sensor; }
  void set_iaq_sensor(sensor::Sensor *sensor) { iaq_sensor_ = sensor; }
  void set_iaq_accuracy_sensor(sensor::Sensor *sensor) { iaq_accuracy_sensor_ = sensor; }
  void set_gas_resistance_sensor(sensor::Sensor *sensor) { gas_resistance_sensor_ = sensor; }
  void set_altitude_sensor(sensor::Sensor *sensor) { altitude_sensor_ = sensor; }

 protected:
  bool valid_checksum_(const uint8_t *frame) const;
  void parse_frame_(const uint8_t *frame);
  bool initialized_{false};
  std::vector<uint8_t> buffer_;

  sensor::Sensor *temperature_sensor_{nullptr};
  sensor::Sensor *humidity_sensor_{nullptr};
  sensor::Sensor *pressure_sensor_{nullptr};
  sensor::Sensor *iaq_sensor_{nullptr};
  sensor::Sensor *iaq_accuracy_sensor_{nullptr};
  sensor::Sensor *gas_resistance_sensor_{nullptr};
  sensor::Sensor *altitude_sensor_{nullptr};
};

}  // namespace mcu680
}  // namespace esphome
