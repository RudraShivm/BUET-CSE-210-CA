#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the Java command with absolute paths
java -jar "$SCRIPT_DIR/logisim-evolution-3.9.0-all.jar" "$SCRIPT_DIR/Ckt/Final_C2_Group_8.circ"

