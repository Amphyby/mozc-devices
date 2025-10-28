// Copyright 2025 Google Inc.
// Use of this source code is governed by an Apache License that can be found
// in the LICENSE file.

#include "photo_sensor.h"

#include "hardware/gpio.h"

//#define NO_SENSOR_PULL

PhotoSensor::PhotoSensor(int8_t bit0,
                         int8_t bit1,
                         int8_t bit2,
                         int8_t bit3,
                         int8_t bit4,
                         int8_t bit5)
    : bits({bit0, bit1, bit2, bit3, bit4, bit5}) {
  for (int8_t gpio : bits) {
    gpio_init(gpio);
    gpio_set_dir(gpio, GPIO_IN);
#ifdef NO_SENSOR_PULL
    gpio_disable_pulls(gpio);
#else
    // Built-in 50-80K pull-up is expected, but the actual value appears to
    // depend on the RP2040's shipping years?
    gpio_pull_up(gpio);
#endif  // NO_SENSOR_PULL
  }
}

uint8_t PhotoSensor::Read() {
  uint8_t value = 0;
  for (size_t bit = 0; bit < bits.size(); ++bit) {
    if (bits[bit] == kNotUsed) {
      break;
    }
    value |= gpio_get(bits[bit]) ? (1 << bit) : 0;
  }
  return value;
}