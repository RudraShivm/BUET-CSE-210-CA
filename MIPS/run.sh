#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python "$SCRIPT_DIR/C2_8_Necessary_Content/assembler.py"
python "$SCRIPT_DIR/C2_8_Necessary_Content/control_unit.py"
java -jar "$SCRIPT_DIR/C2_8_Simulation/logisim-generic-2.7.1.jar" "$SCRIPT_DIR/C2_8_Simulation_single_cycle/MIPS.circ"
java -jar "$SCRIPT_DIR/C2_8_Simulation/logisim-generic-2.7.1.jar" "$SCRIPT_DIR/C2_8_Simulation_Pipelined/MIPS.circ"
