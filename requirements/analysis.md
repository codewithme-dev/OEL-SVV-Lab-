# Requirement Analysis & Refinement

## Original Informal Requirement
“The system should quickly ensure barrier safety when a train is nearby.”

## Identified Defects
1. **Ambiguity**: Terms like "quickly" and "nearby" are subjective and lack precise, measurable definitions. "Ensure barrier safety" is also vague about the exact physical state expected of the barrier (e.g., fully lowered, mechanically locked).
2. **Non-verifiability**: Because there are no specific time constraints or distance thresholds, testers cannot conclusively test or formally verify if the system complies with this requirement under different operational scenarios.
3. **Incompleteness**: The requirement fails to outline the expected behavior once the train is no longer "nearby," nor does it mention warning signals (lights, alarms) prior to closing.

## Refined Precise Measurable Statements
To enable formal verification and validation, the requirement is refined as follows:
1. When a sensor detects an approaching train at a distance of 2000 meters or less, the system shall within 1 second activate the warning lights and alarms.
2. The system must trigger the lowering of the barrier exactly 5 seconds after the alarms are activated. 
3. The barrier must be completely closed (in a locked state) within 15 seconds of the train detection event.
4. **Safety Verification Invariant**: Under no circumstances shall the barrier be in any state other than `Closed` when a train is at a distance of 500 meters or less from the crossing.
5. The barrier shall remain closed until the sensors verify the train has completely cleared the crossing zone (distance > 0 meters moving away).
