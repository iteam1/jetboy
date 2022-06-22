## Issues

This document contain the issues of developing the repository

|No|Issue|Status|Date|Description|Comment|Solution|
|---|---|---|---|---|---|---|
|1|Robot battery|searching| June,17th,22 |Use 60V battery of VinFast for robot|Large voltage meaning low current, that why they use high voltage for the eletric car or bike, due to large torque problem you need large current then the battery volume need to be large too, we use voltage adapter to convert 50V to any lower range like 24V or 12V but be sure the circuit can handle well |Voltage adapter|
|2| Robot motor noise | searching | June,17th,22 | We need large torque to carry heavy load, meaning if your motor is less power also less current-load, they need a gearbox to increase the torque, carry itself body and a battery (7-8kg), no matter the battery's position is high or low the motor's torque still required large |---| Let keep the previous one |
|3|Robot cover |searching|June,17th,22 |the robot looking is important, so we need a morden cover, but making a morden cover need alot money, 3D printing is the cheapest and easiest way but right now the price is `5000` |---|Let split apart which one making by 3D printing and which one making by other machining |
|4|Smooth moving|searching|June,17th,22|Robot working by a python program, inside the `while loop` the workflow is : `get input` -> `decide` -> `action` -> `loop to first step` Check the flowchart [here](./assets/UML_flowchart_tracking_marker.png)|---|The `multi tread` architecture may be the solution, but transfer the data between them is also a problem|