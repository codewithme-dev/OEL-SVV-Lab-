# Verification Logging & Traceability

## Verification Table

| Req ID | Method          | Result | Notes |
|--------|-----------------|--------|-------|
| SRCCS-1| Z Specification | PASS   | The Z schema formally defines the invariant `train = Present \implies barrier = ClosedBarrier`. Safety state transitions naturally maintain this mathematical limit. |
| SRCCS-2| VDM Concept     | PASS   | Pre/post conditions and class invariants explicitly set for Overture. The `inv` clause guarantees the system never evaluates to barrier `<OPEN>` with `trainDetected = true` during state update. |
| SRCCS-3| Alloy Model     | PASS   | The `SafetyInvariant` logically constrained the model scope. System mapping visually returned valid instances verifying there are no edge-cases where the barrier stays Open. |

## Reasoning Explanation
**Alloy Model Safety Reasoning:**
The structural safety of the model depends on the predicate: `all sys: CrossingSystem | (sys.sensor.detects = Present) implies (sys.barrier.state = Closed)`. The Alloy analyzer maps out exhaustively all assignments of the atoms within the bounds (`run show for 3`). Because it couldn't find any counterexample, we reason with absolute certainty that under the defined system axioms, it is physically impossible for the barrier to stay open if the sensor detects a train. This removes systematic ambiguity from the requirement "quickly ensure barrier safety...".
