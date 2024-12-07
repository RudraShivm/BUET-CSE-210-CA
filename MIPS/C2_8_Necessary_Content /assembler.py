import re


class MIPSAssembler:
    def __init__(self):
        # Existing initialization remains the same
        self.r_type_opcodes = {
            "nor": "0100",
            "and": "1001",
            "or": "0110",
            "add": "1101",
            "sub": "1111",
            "srl": "1000",
            "sll": "1011",
        }

        self.i_type_opcodes = {
            "subi": "0000",
            "andi": "0011",
            "addi": "0101",
            "ori": "0111",
            "lw": "1100",
            "sw": "0001",
            "beq": "1110",
            "bneq": "0010",
        }

        self.j_type_opcodes = {"j": "1010"}

        self.registers = {
            "$zero": "0000",
            "$t0": "0001",
            "$t1": "0010",
            "$t2": "0011",
            "$t3": "0100",
            "$t4": "0101",
            "$sp": "0110",
        }
        self.labels = {}
        self.instruction_count = 0

    def decimal_to_binary(self, decimal_num, bits):
        """Convert decimal to binary with specified bit length."""
        try:
            if decimal_num < 0:
                binary = bin((1 << bits) + decimal_num)[2:]
            else:
                binary = bin(decimal_num)[2:]

            return binary.zfill(bits)[-bits:]
        except Exception:
            return "0" * bits

    def parse_instruction(self, instruction):
        """Parse assembly instruction and convert to machine code."""
        # Remove comments, leading/trailing whitespace, and handle blank lines
        instruction = instruction.split("#")[0].strip()

        if not instruction:
            return ""

        # Check if this is just a label
        if instruction.endswith(":"):
            return ""

        self.instruction_count += 1  # Increment instruction count

        # Split instruction into parts, handling multiple whitespace scenarios
        parts = re.split(r",\s*|\s+", instruction)
        opcode = parts[0].lower()

        # R-type instructions (add, sub, and, or, slt)
        if opcode in self.r_type_opcodes:
            inst_opcode = self.r_type_opcodes[opcode]
            rd = self.registers[parts[1]]
            if opcode in ["sll", "srl"]:
                rs = "0000"
                rt = self.registers[parts[2]]
                shamt = self.decimal_to_binary(int(parts[3]), 4)
            else:
                rs = self.registers[parts[2]]
                rt = self.registers[parts[3]]
                shamt = "0000"

            return inst_opcode + rs + rt + rd + shamt

        # I-type instructions (addi, beq, lw, sw)
        elif opcode in self.i_type_opcodes:
            inst_opcode = self.i_type_opcodes[opcode]

            if opcode in ["lw", "sw"]:
                # Handle memory instructions like: lw $t0, 4($s0)
                match = re.match(r"\$\w+,\s*(-?\d+)\((\$\w+)\)", ", ".join(parts[1:]))
                if match:
                    rt = self.registers[parts[1]]
                    rs = self.registers[match.group(2)]
                else:
                    raise ValueError(
                        "The input string does not match the expected format"
                    )
                immediate = self.decimal_to_binary(int(match.group(1)), 8)
            else:
                # Handle other I-type instructions
                rs = self.registers[parts[2]]
                rt = self.registers[parts[1]]
                if parts[3].lstrip("-").isdigit():  # Check if the string is numeric
                    immediate = self.decimal_to_binary(int(parts[3]), 8)
                else:
                    immediate = int(self.labels[parts[3]], 2) - self.instruction_count
                    immediate = self.decimal_to_binary(immediate, 8)

            return inst_opcode + rs + rt + immediate

        elif opcode in self.j_type_opcodes:
            # J-type instructions (j)
            inst_opcode = self.j_type_opcodes[opcode]
            target = self.labels[parts[1]]

            return inst_opcode + target + "00000000"

        else:
            return f"Invalid instruction: {instruction}"

    def convert_program(self, assembly_code):
        """Convert entire MIPS assembly program to machine code."""
        # Normalize the input: remove extra whitespace and handle multiple newlines
        # Split the code into lines, strip each line, and remove empty lines
        normalized_code = [
            line.strip() for line in assembly_code.split("\n") if line.strip()
        ]

        # First pass to extract labels
        self.instruction_count = 0
        for line in normalized_code:
            # Extract labels, handling label-only lines
            print(line)
            if line and line.endswith(":"):
                # Store label's address (instruction count at this point)
                self.labels[line[:-1]] = self.decimal_to_binary(
                    self.instruction_count, 8
                )
            elif not line.endswith(":") and not line.startswith("#"):
                # Only increment for actual instructions
                self.instruction_count += 1
        # Second pass to convert instructions to machine code
        machine_code = []
        self.instruction_count = 0  # Reset for second pass
        for line in normalized_code:
            print(line, end =" ")
            # Skip label-only lines
            if line.endswith(":"):
                continue

            machine_instruction = self.parse_instruction(line)
            if machine_instruction:
                # Convert binary to hex, ensuring 5-digit hex representation
                hexcode = hex(int(machine_instruction, 2))[2:].zfill(5)
                print("hexcode: "+hexcode)
                machine_code.append(hexcode)

        return machine_code


def main():
    assembler = MIPSAssembler()

    filepath = "assem.txt"
    with open(filepath, "r") as my_file:
        assembly_code = my_file.read()

    machine_code = assembler.convert_program(assembly_code)

    # Write machine code to file
    filepath = "machine_code.txt"
    with open(filepath, "w") as my_file:
        my_file.write("v2.0 raw\n")
        for code in machine_code:
            my_file.write(code + "\n")


if __name__ == "__main__":
    main()
