#!python

from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("file", help="asm file to compile")
parser.add_argument("--out", help="out hack file")
parser.add_argument("--vpretty", help="adds line bw ins", action="store_true")

args = parser.parse_args()

in_file = args.file
if args.out:
    out_file = args.out
else:
    out_file = in_file.replace(".asm", ".hack")

asm = open(in_file).read()

statements = []
statement_counter = 0
labels = dict()
used_addresses = []
variable_line_nums = defaultdict(list)

def get_comp_bits(comp: str) -> str:
    if comp == '0':
        return '101010'
    elif comp == '1':
        return '111111'
    elif comp == '-1':
        return '111010'
    elif comp == 'D':
        return '001100'
    elif comp == 'A' or comp == 'M':
        return '110000'
    elif comp == '!D':
        return '001101'
    elif '!' in comp:
        return '110001'
    elif comp == '-D':
        return '001111'
    elif comp.startswith('-'):
        return '110011'
    elif comp == 'D+1':
        return '011111'
    elif comp.endswith('+1'):
        return '110111'
    elif comp == 'D-1':
        return '001110'
    elif comp.endswith('-1'):
        return '110010'
    elif comp.startswith('D+'):
        return '000010'
    elif comp.startswith('D-'):
        return '010011'
    elif comp.endswith('-D'):
        return '000111'
    elif comp.startswith('D&'):
        return '000000'
    elif comp.startswith('D|'):
        return '010101'
    else:
        raise Exception("fuckall" + comp)

def get_dest(dest):
    dest_bits = ''
    dest_bits += '1' if 'A' in dest else '0'
    dest_bits += '1' if 'D' in dest else '0'
    dest_bits += '1' if 'M' in dest else '0'
    return dest_bits

def get_jmp(jmp):
    match jmp:
        case '':
            return '000'
        case 'JGT':
            return '001'
        case 'JEQ':
            return '010'
        case 'JGE':
            return '011'
        case 'JLT':
            return '100'
        case 'JNE':
            return '101'
        case 'JLE':
            return '110'
        case 'JMP':
            return '111'
    raise Exception("fuckall jmp")

# converts num to 7 bit address
def conv_to_bin(num):
    bin_str = str(bin(num))[2:]
    prepend = 15-len(bin_str)
    return '0'*prepend+bin_str

for line in asm.splitlines():
    # remove spaces
    line = line.replace(" ", "")
    # remove comment bits
    if "//" in line:
        comment_start = line.index("//")
        line = line[:comment_start]
    # remove empty line
    if line == "":
        continue

    if line.startswith('(') and line.endswith(')'):
        labels[line[1:-1]] = statement_counter
        used_addresses.append(statement_counter)
        continue

    if line.startswith('@'):
        # A ins
        line = line[1:]
        if line[0] == 'R' and line[1:].isdigit():
            line = line[1:]
        if line.isdigit(): # variable
            locn = conv_to_bin(int(line))
            used_addresses.append(locn)
            statements.append('0' + locn)
        else: # digit
            statements.append(line)
            variable_line_nums[line].append(statement_counter)
    else:
        # C ins
        jmp_cond = ""
        stmt = ""
        dest = ""
        comp = ""
        if ';' in line:
            ind = line.index(';')
            stmt = line[:ind]
            jmp_cond = line[ind+1:]
        else:
            stmt = line
        if '=' in stmt:
            ind = stmt.index('=')
            dest = stmt[:ind]
            comp = stmt[ind+1:]
        else:
            comp = stmt
        a_bit = '0'
        if 'M' in comp:
            a_bit = '1'
        bits = '111' + a_bit
        bits += get_comp_bits(comp)
        bits += get_dest(dest)
        bits += get_jmp(jmp_cond)
        statements.append(bits)
    statement_counter += 1

# assign variable values
mem_counter = 16

for var_name, line_nums in variable_line_nums.items():
    if var_name in labels:
        for ins_index in line_nums:
            statements[ins_index] = '0'+conv_to_bin(labels[var_name])
    else:
        # update mem counter till it hits unused
        while mem_counter in used_addresses:
            mem_counter += 1
        used_addresses.append(mem_counter)
        for ins_index in line_nums:
            statements[ins_index] = '0'+conv_to_bin(mem_counter)


write_file = open(out_file, 'w')
write_file.write(("\n" if args.vpretty else "").join(statements))
