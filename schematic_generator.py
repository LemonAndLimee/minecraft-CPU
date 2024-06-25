import mcschematic
import re
import sys
import math

'''This script takes a generated machine code program and creates a 1.20.1 Minecraft schematic to represent this.
A schematic is a collection of blocks that can be spawned in using the WorldEdit mod: this allows large programs to be spawned instantly without the possibility of human error.
A program is represented by a collection of redstone signal strengths, and therefore can be represented using barrels of various fullness levels: the signal strength read from a barrel depends on the number of blocks in it.'''

'''The script takes a program file name as input and generates one or more schematics, stored in the schematics folder.
If the program is longer than 15 instructions, it will need to be broken into more than one schematic.
Schematics will be named: filename_block1.schem, filename_block2.schem, etc.
'''

'''The format for generating a minecraft container block is as follows:
minecraft:barrel{Items:[{Slot:0, Count:64, id:"minecraft:oak_planks"}]}
This refers to a barrel with 64 (1 stack) oak planks in the first container slot. This can be used to create barrels with various signal strengths, which can be spawned and read from to create a machine code program.

The lower bounds for each signal strength in barrels are as follows:
0 = 0 items
1 = 1 item
2 = 1 stack and 60
3 = 3 stacks and 55
4 = 5 stacks and 51
5 = 7 stacks and 46
6 = 9 stacks and 42
7 = 11 stacks and 37
8 = 13 stacks and 32
9 = 15 stacks and 28
10 = 17 stacks and 23
11 = 19 stacks and 19
12 = 21 stacks and 14
13 = 23 stacks and 10
14 = 25 stacks and 5
15 = 27 stacks
'''

# the gap between instructions, used to calculate the coordinates of barrels
HORIZONTAL_GAP = 5
VERTICAL_GAP = 2

SIGNAL_STRENGTH_LOWER_BOUNDS = {
    0:0,
    1:1,
    2:124,
    3:247,
    4:371,
    5:494,
    6:618,
    7:741,
    8:864,
    9:988,
    10:1111,
    11:1235,
    12:1358,
    13:1482,
    14:1605,
    15:1728
}
'''Describes the number of blocks needed in a barrel to achieve a given signal strength.'''

def read_file_into_list(filename:str) -> list:
    '''Reads machine code file into list of instructions. Each instruction is a list of 4 integers.'''
    results = []
    with open("programs/" + filename + "_converted.txt", 'r') as input_file:
        for line in input_file:
            line = line[:-1] if line[-1] == '\n' else line
            parts = re.split(" ", line)
            parts = parts[-4:]
            integer_parts = []
            for part in parts:
                try:
                    integer_parts.append(int(part))
                except:
                    raise Exception("Machine code must be integers.")
            results.append(integer_parts)
    return results

def calculate_barrel_position(instruction_index:int, parameter_index:int) -> tuple:
    '''Calculates coordinates of a barrel given the instruction index and index of parameter within the instruction.
    Returns a tuple in the form (x, y, z)
    '''
    x = instruction_index*HORIZONTAL_GAP
    y = -(parameter_index*VERTICAL_GAP)
    coords = (x, y, 0)
    return coords

def get_barrel_string(signal_strength:str) -> str:
    '''Returns string describing barrel of given signal strength.'''
    blocks_needed = SIGNAL_STRENGTH_LOWER_BOUNDS[signal_strength]
    stacks = blocks_needed // 64
    remainder = blocks_needed % 64

    barrel_string = "minecraft:barrel{Items:["
    for inventory_slot in range(stacks):
        barrel_string = barrel_string + "{Slot:" + str(inventory_slot) + ", Count:64, id:\"minecraft:oak_planks\"}, "
    
    # if barrel is not full, add final stack
    if signal_strength < 15:
        barrel_string = barrel_string + "{Slot:" + str(stacks) + ", Count:" + str(remainder) +", id:\"minecraft:oak_planks\"}"
    # if barrel is full, remove the final comma
    else:
        barrel_string = barrel_string[:-2]
    barrel_string = barrel_string + "]}"
    
    return barrel_string

def add_instruction_to_schematic(schematic:mcschematic.MCSchematic, instruction:list, instruction_index:int) -> None:
    '''Adds a given instruction to the schematic.'''
    # for each 4 bits of the instruction, add it to the schematic
    for parameter_index in range(len(instruction)):
        parameter = instruction[parameter_index]
        barrel_position = calculate_barrel_position(instruction_index=instruction_index, parameter_index=parameter_index)
        barrel_string = get_barrel_string(signal_strength=parameter)
        schematic.setBlock(barrel_position, barrel_string)

def create_block_schematic(block:list, block_index:int) -> None:
    '''Given a block of 15 instructions, creates a schematic file to represent the code.'''
    schematic = mcschematic.MCSchematic()
    
    for instruction_index in range(len(block)):
        instruction = block[instruction_index]
        add_instruction_to_schematic(schematic, instruction, instruction_index)
    
    schematic.save(outputFolderPath="schematics", schemName=f"{sys.argv[1]}_block{block_index}", version=mcschematic.Version.JE_1_20_1)

def generate_schematics(instructions:list) -> None:
    '''Given a list of instructions, splits them into blocks of 15 then generates 1 or more schematic files and stores them in schematics folder.'''
    number_of_blocks = math.ceil(len(instructions)/15)
    for block_index in range(1, number_of_blocks+1):
        start_index = (block_index-1)*15
        end_index = start_index + 15
        if end_index >= len(instructions):
            end_index = len(instructions)
        
        block = instructions[start_index:end_index]
        create_block_schematic(block, block_index)

instructions = read_file_into_list(sys.argv[1])
'''for instr in instructions:
    print(instr)'''

generate_schematics(instructions)