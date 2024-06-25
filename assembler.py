import re
import sys

NUMBER_OF_REGISTERS = 15
OPCODES = {
    "ADD":1,
    "SUB":2,
    "AND":3,
    "OR":4,
    
    "LS":5,
    "RS":6,
    
    "LD":7,
    "LDI":8,
    "STR":9,
    
    "BRE":10,
    "BRLT":11
}
'''Dict of opcodes in the form "STR":opcode'''

int_branch_labels = {}
'''Dict of labels and their instruction cycle numbers.'''
mem_cell_branch_labels = {}
'''Dict of labels and their instruction memory cell number (integer).'''

unused_registers = []
'''Stores numbers of all unused registers.'''
for i in range(1, NUMBER_OF_REGISTERS):
    unused_registers.append(i)

immediate_registers = {}
'''Stores all registers that are written to only with LDIs before the first branch of the program. (All of them if there are no branches).
These are the registers which are suitable to replace immediate operands, as the values in them won't change.
key:value pairs are in the form, register number : RegisterInfo() instance
'''

class RegisterInfo:
    '''RegisterInfo : Class

    Attributes:
    value:int -- value stored in register
    cycle_last_written:int -- the instruction cycle in which the register was last written to
    '''
    def __init__(self, value:int=0, cycle_last_written:int=0):
        self.value = value
        self.cycle_last_written = cycle_last_written
    
    def __str__(self):
        return f"Value: {self.value}, Cycle last written: {self.cycle_last_written}"

def read_file_into_list(filename:str) -> list:
    '''Reads file into list of instruction lists, each in the form [opcode, operand 1, operand 2, etc.]'''
    results = []
    with open("programs/" + filename + ".txt", 'r') as input_file:
        for line in input_file:
            line = line[:-1] if line[-1] == '\n' else line
            if len(line) > 0:
                parts = re.split(" |, ", line)
                results.append(parts)
    return results

def begins_with_label(instruction:list) -> bool:
    '''Returns True if instruction begins with label, False otherwise'''
    if str(instruction[0])[-1] == ':':
        return True
    else:
        return False

def get_opcode_str(instruction:list) -> int:
    '''Returns string version of instruction opcode.'''
    opcode_str = instruction[1] if begins_with_label(instruction) else instruction[0]
    return opcode_str

def get_opcode(instruction:list) -> int:
    '''Returns instruction opcode in integer form. Returns -1 if it is not a known opcode.'''
    opcode_str = get_opcode_str(instruction)
    try:
        return OPCODES[opcode_str]
    except:
        return -1

def is_branch_instruction(instruction:list) -> bool:
    '''Returns True if instruction is a branch, False otherwise.'''
    opcode_str = get_opcode_str(instruction)
    if opcode_str[:2] == "BR":
        return True
    else:
        return False

def get_operands_start_index(instruction:list) -> int:
    '''Returns index in the instruction list in which the operands start.'''
    start_index = 2 if begins_with_label(instruction) else 1
    return start_index

def get_operands(instruction:list) -> list:
    '''Returns list of instruction operands.'''
    start_index = get_operands_start_index(instruction)
    operands = instruction[start_index:]
    return operands

def is_operand_immediate(operand:str) -> bool:
    '''Returns True if operand is immediate, False otherwise.'''
    if operand[0] == '#':
        return True
    else:
        return False

def get_operand_value(operand:str) -> int:
    '''Returns operand integer value by removing the 'R' or the '#' from the beginning.'''
    value_str = operand[1:]
    try:
        return int(value_str)
    except:
        raise Exception("Operand must consist of an R or #, followed only by an integer.")

def get_cycle_of_first_branch_or_label(instructions:list) -> int:
    '''Returns instruction cycle of the first branch or label in the program. Returns -1 if there are none.'''
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        if begins_with_label(instruction) or is_branch_instruction(instruction):
            return instruction_cycle

    return -1

def scan_for_immediate_registers(instructions:list) -> None:
    '''Scans instructions for registers which are suitable for the immediate_registers dict, adding them.'''
    instruction_cycle = 0
    while instruction_cycle < len(instructions):
        instruction = instructions[instruction_cycle]
        opcode = get_opcode(instruction)

        #if instruction is a write-back instruction, remove from unused_registers
        if opcode >= OPCODES["ADD"] and opcode <= OPCODES["LDI"]:
            operands = get_operands(instruction)
            write_back_operand = operands[0]
            #write-back reg must be a register, not an immediate value
            if is_operand_immediate(write_back_operand):
                raise Exception(f"i {instruction_cycle}, operand 0: must be a register.")
            
            write_back_reg_number = get_operand_value(write_back_operand)

            if write_back_reg_number in unused_registers:
                unused_registers.remove(write_back_reg_number)

            first_branch_cycle = get_cycle_of_first_branch_or_label(instructions)

            value = get_operand_value(operands[1])
            #if write-back register exists in the immediate registers list
            if write_back_reg_number in immediate_registers.keys():
                if opcode == OPCODES["LDI"]:
                    #if instruction past the first branch, remove from immediate registers list
                    if (first_branch_cycle > -1 and instruction_cycle >= first_branch_cycle):
                        immediate_registers.pop(write_back_reg_number)
                    #if instruction before first branch, or if there are no branches, update RegisterInfo
                    else:
                        reg_info = immediate_registers[write_back_reg_number]
                        reg_info.value = value
                        reg_info.cycle_last_written = instruction_cycle
                #if instruction not an LDI, remove from immediate registers list
                else:
                    immediate_registers.pop(write_back_reg_number)
            #if write-back register not in immediate registers list, and instruction is an LDI, add to list
            elif opcode == OPCODES["LDI"]:
                reg_info = RegisterInfo(value=value, cycle_last_written=instruction_cycle)
                immediate_registers[write_back_reg_number] = reg_info
            
        instruction_cycle += 1

def remove_zero_ldis(instructions:list) -> None:
    '''Removes any redundant #0 LDIs, excluding multiple-write registers or instructions with a label.'''
    instruction_cycle = 0
    while instruction_cycle < len(instructions):
        instruction = instructions[instruction_cycle]
        opcode = get_opcode(instruction)
        operands = get_operands(instruction)
        
        #remove any LDI #0 instructions that are in immediate_registers, as they are redundant
        if opcode == OPCODES["LDI"] and not begins_with_label(instruction):
            value = get_operand_value(operands[1])
            if value == 0:
                write_back_reg_number = get_operand_value(operands[0])
                if write_back_reg_number in immediate_registers.keys():
                    immediate_registers[write_back_reg_number].cycle_last_written = 0
                    instructions.remove(instruction)
                    instruction_cycle -= 1
        
        instruction_cycle += 1

def find_existing_immediate_register(immediate_value:int, instruction_cycle:int) -> int:
    '''Given immediate_value, returns register number of immediate register holding that value.
    Register is only suitable if it was last written to before the given instruction cycle.
    Returns -1 if no such register exists.
    '''
    for reg_num in immediate_registers.keys():
        register_info = immediate_registers[reg_num]
        if register_info.value == immediate_value:
            if register_info.cycle_last_written < instruction_cycle:
                return reg_num
    return -1

def replace_operand(instructions:list, instr_cycle:int, op_index:int, new_value:str) -> None:
    '''Replaces operand at given location with new_value.'''
    start_index = get_operands_start_index(instructions[instr_cycle])
    instructions[instr_cycle][start_index+op_index] = new_value

def increment_last_writtens() -> None:
    '''Increments cycle_last_written values in all existing immediate_register objects.
    Used for when a new LDI is added, incrementing all instruction indexes.
    '''
    for reg_num in immediate_registers.keys():
        reg_info = immediate_registers[reg_num]
        reg_info.cycle_last_written = reg_info.cycle_last_written + 1

def create_new_ldi(instructions:list, immediate_value:int) -> int:
    '''Adds a new LDI operation to the beginning of the instructions, loading in immediate_value.
    Finds unused register for LDI, removes it from unused_registers and adds it to immediate_registers.
    Returns register number used.
    '''
    if len(unused_registers) < 1:
        raise Exception("Run out of registers to use.")
    #get unused register, remove it from list
    register = unused_registers[-1]
    unused_registers.pop()

    #define new RegisterInfo() instance for placing into immediate_registers
    reg_info = RegisterInfo(value=immediate_value, cycle_last_written=0)
    #an LDI is unnecessary for a #0
    if immediate_value != 0:
        #increment cycle_last_written values in immediate_registers
        increment_last_writtens()
        #create new instruction and add to beginning of instructions list
        instruction = ["LDI", f"R{register}", f"#{immediate_value}"]
        instructions.insert(0, instruction)
    immediate_registers[register] = reg_info

    return register

def convert_immediate_operands(instructions:list) -> None:
    '''Converts any immediate operands not in an LDI operation, by either using an existing immediate register, or creating a new LDI operation.'''
    instruction_cycle = 0
    while instruction_cycle < len(instructions):
        instruction = instructions[instruction_cycle]
        opcode = get_opcode(instruction)
        operands = get_operands(instruction)

        #if instruction is not allowed an immediate operand, convert it
        if opcode != OPCODES["LDI"]:
            for operand_index in range(len(operands)):
                operand = operands[operand_index]
                if is_operand_immediate(operand):
                    operand_value = get_operand_value(operand)
                    #if there is an existing suitable register with that value, replace with that
                    register_num = find_existing_immediate_register(immediate_value=operand_value, instruction_cycle=instruction_cycle)
                    #if no suitable register exists, create new LDI instruction
                    if register_num == -1:
                        register_num = create_new_ldi(instructions=instructions, immediate_value=operand_value)
                        if operand_value != 0:
                            instruction_cycle += 1
                    
                    #replace the operand with the relevant register number
                    replace_operand(instructions=instructions, instr_cycle=instruction_cycle, op_index=operand_index, new_value=f"R{register_num}")

        instruction_cycle += 1

def replace_instruction(instructions:list, instr_cycle:int, new_instruction:list) -> None:
    '''Replaces instruction at specified cycle.'''
    instructions[instr_cycle] = new_instruction

def convert_custom_branches(instructions:list) -> None:
    '''Converts custom branches to a format accepted by the instruction set.
    - BRZ becomes BRE with a #0
    - BRU becomes BRE R1 R1
    - BRGT a,b becomes BRLT b,a
    '''
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        opcode_str = get_opcode_str(instruction)
        operands = get_operands(instruction)

        target_operand = operands[0]
        remaining_operands = operands[1:]
        
        replacement_instr = []
        if opcode_str == "BRZ":
            replacement_instr = ["BRE", target_operand, remaining_operands[0], "#0"]
        elif opcode_str == "BRU":
            replacement_instr = ["BRE", target_operand, "R1", "R1"]
        elif opcode_str == "BRGT":
            replacement_instr = ["BRLT", target_operand, remaining_operands[1], remaining_operands[0]]
        if len(replacement_instr) > 0:
            if begins_with_label(instruction):
                replacement_instr.insert(0, instruction[0])
            replace_instruction(instructions=instructions, instr_cycle=instruction_cycle, new_instruction=replacement_instr)

def convert_cycle_to_custom_hex(instr_cycle:int) -> str:
    '''Takes instruction cycle integer and converts to custom hexadecimal, starting from 0x11 and omitting any 0's.'''
    first_bit = (instr_cycle // 15) + 1
    second_bit = (instr_cycle % 15) + 1

    first_hex = hex(first_bit)
    second_hex = hex(second_bit)
    combined_hex = first_hex + second_hex[2:]
    return combined_hex

def convert_cycle_to_instruction_cell_int(instr_cycle:int) -> int:
    '''Converts instruction cycle number into the integer that is needed to represent its memory cell.'''
    custom_hex = convert_cycle_to_custom_hex(instr_cycle)
    int_version = int(custom_hex, 16)
    return int_version

def get_instruction_label(instruction:list) -> str:
    '''Returns label at the beginning of the instruction, without the :.'''
    if begins_with_label(instruction):
        label = instruction[0][:-1]
        return label
    else:
        raise Exception("Instruction must begin with a label to call get_instruction_label()")

def calculate_branch_labels(instructions:list) -> None:
    '''Calculates branch label values, adding them in integer form to int_branch_labels dict.'''
    #find labels and assign them to dictionary
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        if begins_with_label(instruction):
            label = get_instruction_label(instruction)
            int_branch_labels[label] = instruction_cycle

def increment_branch_labels(amount:int) -> None:
    '''Increments all values in int_branch_labels by amount specified.'''
    for label in int_branch_labels.keys():
        int_branch_labels[label] = int_branch_labels[label] + amount

def add_label_ldi_instructions(instructions:list) -> None:
    '''Adds any necessary LDIs for the labels, incrementing the values in int_branch_labels.'''

    increment_amount = 0
    #first pass - if any values already exist, there is 1 less increment required, so decrement the amount variable
    for label in int_branch_labels.keys():
        instr_cycle = int_branch_labels[label]
        mem_cell = convert_cycle_to_instruction_cell_int(instr_cycle=instr_cycle)
        existing_register = find_existing_immediate_register(immediate_value=mem_cell, instruction_cycle=instr_cycle)
        if existing_register == -1:
            increment_amount += 1
    #increment all labels by the number of LDIs needed
    increment_branch_labels(increment_amount)

    for label in int_branch_labels.keys():
        instr_cycle = int_branch_labels[label]
        mem_cell = convert_cycle_to_instruction_cell_int(instr_cycle=instr_cycle)
        existing_register = find_existing_immediate_register(immediate_value=mem_cell, instruction_cycle=instr_cycle)
        #if no existing register with the desired value, create an LDI and increment future branch labels
        if existing_register == -1:
            create_new_ldi(instructions=instructions, immediate_value=mem_cell)

def remove_label_declarations(instructions:list) -> None:
    '''Removes labels from the beginning of instructions.'''
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        if begins_with_label(instruction):
            instructions[instruction_cycle].pop(0)

def convert_branch_labels(instructions:list) -> None:
    '''Replaces instances of branch labels with the register that points to it.'''
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        operands = get_operands(instruction)
        for operand_index in range(len(operands)):
            operand = operands[operand_index]
            if operand in int_branch_labels.keys():
                pointer_instr_cycle = int_branch_labels[operand]
                mem_cell = convert_cycle_to_instruction_cell_int(instr_cycle=pointer_instr_cycle)
                #there should be an existing register as all necessary LDIs have been created
                existing_register = find_existing_immediate_register(immediate_value=mem_cell, instruction_cycle=instruction_cycle)
                replace_operand(instructions, instr_cycle=instruction_cycle, op_index=operand_index, new_value=f"R{existing_register}")

def remove_comments(instructions:list) -> None:
    '''Removes any comment lines that begin with a //'''
    instr_index = 0
    while instr_index < len(instructions):
        instruction = instructions[instr_index]
        if instruction[0][0:2] == "//":
            instructions.pop(instr_index)
        else:
            instr_index += 1

def convert_syntax(instructions:list) -> None:
    '''Converts instructions into correct syntax, on a 1-1 relationship with the machine code.'''
    remove_comments(instructions)
    scan_for_immediate_registers(instructions)
    remove_zero_ldis(instructions)
    convert_custom_branches(instructions)
    convert_immediate_operands(instructions)
    calculate_branch_labels(instructions)
    add_label_ldi_instructions(instructions)
    remove_label_declarations(instructions)
    convert_branch_labels(instructions)

def convert_opcodes(instructions:list) -> None:
    '''Converts opcode strings into their numbers'''
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        opcode = get_opcode(instruction)
        instructions[instruction_cycle][0] = opcode

def convert_operands(instructions:list) -> None:
    '''Removes the R or # from the start of operands. Splits LDI operands that are >15 over two operands.'''
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        start_offset = 2 if begins_with_label(instruction) else 1
        for operand_index in range(start_offset, len(instruction)):
            operand_value = get_operand_value(instruction[operand_index])
            #if operand value fits into 1 bit, replace operand with the value
            if operand_value <= 15:
                #if instruction is an LDI, final operand value must be in the second bit, in the form 0, x
                if instruction[0] == 8 and operand_index == 2:
                    instructions[instruction_cycle][operand_index] = 0
                    instructions[instruction_cycle].append(operand_value)
                #otherwise it can replace the initial operand position
                else:
                    instructions[instruction_cycle][operand_index] = operand_value
            #if operand is larger than 1 bit
            else:
                #if instruction is an LDI, split the value over 2 operands
                if instruction[0] == 8:
                    hex_version = hex(operand_value)
                    digit_1 = int(hex_version[2], 16)
                    digit_2 = int(hex_version[3], 16)
                    instructions[instruction_cycle][operand_index] = digit_1
                    instructions[instruction_cycle].append(digit_2)
                else:
                    raise Exception("Direct operands must be between 1 and 15.")

def pad_to_equal_width(instructions:list) -> None:
    '''Pads any instructions that have < 4 bits with 0 operands, so they are all of width 4.'''
    for instruction_cycle in range(len(instructions)):
        instruction = instructions[instruction_cycle]
        if len(instruction) < 4:
            pad_number = 4 - len(instruction)
            for i in range(pad_number):
                instructions[instruction_cycle].append(0)

def convert_to_machine_code(instructions:list) -> None:
    '''Converts given list of assembly instructions into machine code numbers.'''
    convert_opcodes(instructions)
    convert_operands(instructions)
    pad_to_equal_width(instructions)

def write_to_file(instructions:list, filename:str) -> None:
    with open("programs/machine code/" + filename + "_converted.txt", 'w') as output_file:
        instrs_output = []
        counter = 0
        for instruction in instructions:
            instruction_str = ""
            for bit in instruction:
                instruction_str = instruction_str + " " + str(bit)
                
            instr_hex = convert_cycle_to_custom_hex(counter)
            bit_1 = int(instr_hex[2], 16)
            bit_2 = int(instr_hex[3], 16)
            new_instr_hex = f"{bit_1} {bit_2}"
            
            joined = f"instr {new_instr_hex}:{instruction_str}"
            if instruction != instructions[-1]:
                joined = joined + "\n"
            instrs_output.append(joined)
            counter += 1
        output_file.writelines(instrs_output)

instructions = read_file_into_list(sys.argv[1])

for instr in instructions:
    print(instr)

convert_syntax(instructions)

print("\n")
for instr_index in range(len(instructions)):
    print(f"{instr_index+1} {instructions[instr_index]}")

convert_to_machine_code(instructions)

print("\n")
for instr_index in range(len(instructions)):
    print(f"{instr_index+1} {instructions[instr_index]}")
    
write_to_file(instructions, sys.argv[1])