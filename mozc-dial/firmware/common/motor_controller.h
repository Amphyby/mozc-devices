// Copyright 2025 Google Inc.
// Use of this source code is governed by an Apache License that can be found
// in the LICENSE file.

#ifndef COMMON_MOTOR_CONTROLLER_H_
#define COMMON_MOTOR_CONTROLLER_H_

#include <cstdint>
#include <memory>

#include "pico/time.h"

class MotorController final {
 public:
  enum class Mode { k1Motor, k9Motor };
  enum class Direction { kForward, kBackward };
  explicit MotorController(Mode = Mode::k9Motor, Direction = Direction::kForward);
  MotorController(const MotorController&) = delete;
  MotorController& operator=(const MotorController&) = delete;
  ~MotorController();

  void Start(uint8_t index);
  void Stop(uint8_t index);

 private:
  class Decoder;

  static bool OnAlarm(repeating_timer* t);
  void Step();

  static constexpr size_t kNumOfPhases = 4;
  static constexpr size_t kNumOfMotors = 9;
  std::unique_ptr<Decoder> decoder_[kNumOfPhases];
  bool started_[kNumOfMotors] = { false };
  uint8_t phase_ = 0;
  repeating_timer timer_;
  Direction direction_ = Direction::kForward;
};

#endif  // COMMON_MOTOR_CONTROLLER_H_