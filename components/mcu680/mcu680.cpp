#include "mcu680.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace mcu680 {

static const char *const TAG = "mcu680";
static constexpr uint8_t FRAME_LEN = 20;

void MCU680Component::setup() {
  this->check_uart_settings(9600);
  this->buffer_.reserve(64);

  const uint8_t cmd1[] = {0xA5, 0x55, 0x3F, 0x39};
  const uint8_t cmd2[] = {0xA5, 0x56, 0x02, 0xFD};
  this->write_array(cmd1, sizeof(cmd1));
  this->write_array(cmd2, sizeof(cmd2));
  this->flush();
  this->initialized_ = true;
  ESP_LOGCONFIG(TAG, "MCU680 initialized");
}

void MCU680Component::dump_config() {
  ESP_LOGCONFIG(TAG, "MCU680 / MCU681 UART Sensor");
  LOG_UART_DEVICE(this);
  LOG_SENSOR("  ", "Temperature", this->temperature_sensor_);
  LOG_SENSOR("  ", "Humidity", this->humidity_sensor_);
  LOG_SENSOR("  ", "Pressure", this->pressure_sensor_);
  LOG_SENSOR("  ", "IAQ", this->iaq_sensor_);
  LOG_SENSOR("  ", "IAQ Accuracy", this->iaq_accuracy_sensor_);
  LOG_SENSOR("  ", "Gas Resistance", this->gas_resistance_sensor_);
  LOG_SENSOR("  ", "Altitude", this->altitude_sensor_);
}

bool MCU680Component::valid_checksum_(const uint8_t *frame) const {
  uint32_t sum = 0;
  for (int i = 0; i < 19; i++)
    sum += frame[i];
  return (sum % 256) == frame[19];
}

void MCU680Component::parse_frame_(const uint8_t *frame) {
  // frame layout confirmed from the uploaded NodeMCU parser:
  // 0-1 header 0x5A 0x5A
  // 4-5 temp (signed, /100)
  // 6-7 hum (/100)
  // 8-10 pressure (u24, /100)
  // 11 high nibble iaq_accuracy, low nibble iaq high bits
  // 12 iaq low byte
  // 13-16 gas resistance (u32, ohm)
  // 17-18 altitude (signed)
  // 19 checksum
  const int16_t temp_raw = (int16_t(frame[4]) << 8) | frame[5];
  const uint16_t hum_raw = (uint16_t(frame[6]) << 8) | frame[7];
  const uint32_t press_raw = (uint32_t(frame[8]) << 16) | (uint32_t(frame[9]) << 8) | frame[10];
  const uint8_t iaq_acc = (frame[11] & 0xF0) >> 4;
  const uint16_t iaq = (uint16_t(frame[11] & 0x0F) << 8) | frame[12];
  const uint32_t gas_raw = (uint32_t(frame[13]) << 24) | (uint32_t(frame[14]) << 16) |
                           (uint32_t(frame[15]) << 8) | frame[16];
  const int16_t altitude_raw = (int16_t(frame[17]) << 8) | frame[18];

  const float temp = temp_raw / 100.0f;
  const float hum = hum_raw / 100.0f;
  const float press = press_raw / 100.0f;
  const float gas_kohm = gas_raw / 1000.0f;

  ESP_LOGD(TAG, "Frame ok: temp=%.2fC hum=%.2f%% press=%.2fhPa iaq_acc=%u iaq=%u gas=%.1fkOhm alt=%dm",
           temp, hum, press, iaq_acc, iaq, gas_kohm, altitude_raw);

  if (this->temperature_sensor_ != nullptr)
    this->temperature_sensor_->publish_state(temp);
  if (this->humidity_sensor_ != nullptr)
    this->humidity_sensor_->publish_state(hum);
  if (this->pressure_sensor_ != nullptr)
    this->pressure_sensor_->publish_state(press);
  if (this->iaq_accuracy_sensor_ != nullptr)
    this->iaq_accuracy_sensor_->publish_state(iaq_acc);
  if (this->iaq_sensor_ != nullptr)
    this->iaq_sensor_->publish_state(iaq);
  if (this->gas_resistance_sensor_ != nullptr)
    this->gas_resistance_sensor_->publish_state(gas_kohm);
  if (this->altitude_sensor_ != nullptr)
    this->altitude_sensor_->publish_state(altitude_raw);
}

void MCU680Component::loop() {
  while (this->available()) {
    uint8_t byte;
    if (this->read_byte(&byte)) {
      this->buffer_.push_back(byte);
    }
  }

  while (this->buffer_.size() >= 2) {
    if (!(this->buffer_[0] == 0x5A && this->buffer_[1] == 0x5A)) {
      this->buffer_.erase(this->buffer_.begin());
      continue;
    }

    if (this->buffer_.size() < FRAME_LEN)
      return;

    if (this->valid_checksum_(this->buffer_.data())) {
      this->parse_frame_(this->buffer_.data());
      this->buffer_.erase(this->buffer_.begin(), this->buffer_.begin() + FRAME_LEN);
    } else {
      ESP_LOGW(TAG, "Checksum failed, shifting by one byte");
      this->buffer_.erase(this->buffer_.begin());
    }
  }

  if (this->buffer_.size() > 128) {
    ESP_LOGW(TAG, "Clearing oversized UART buffer (%u bytes)", (unsigned) this->buffer_.size());
    this->buffer_.clear();
  }
}

}  // namespace mcu680
}  // namespace esphome
