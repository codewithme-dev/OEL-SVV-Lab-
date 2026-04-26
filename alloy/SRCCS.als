module SRCCS

abstract sig BarrierState {}
one sig Open extends BarrierState {}
one sig Closed extends BarrierState {}

abstract sig TrainState {}
one sig Present extends TrainState {}
one sig NotPresent extends TrainState {}

sig Sensor {
  detects: TrainState
}

sig Barrier {
  state: BarrierState
}

sig CrossingSystem {
  sensor: one Sensor,
  barrier: one Barrier
}

-- Safety constraint (Invariant)
-- As per formal requirement: "Train present => barrier must not be open" (i.e. must be closed)
fact SafetyInvariant {
  all sys: CrossingSystem |
    (sys.sensor.detects = Present) implies (sys.barrier.state = Closed)
}

-- Ensure that the system defaults to opening barrier if no train is present
fact NormalOperation {
  all sys: CrossingSystem |
    (sys.sensor.detects = NotPresent) implies (sys.barrier.state = Open)
}

pred show[] {}

run show for 3
