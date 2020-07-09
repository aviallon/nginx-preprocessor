#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 01:46:07 2020

@author: aviallon
"""

import argparse
import re
from pathlib import Path

parser = argparse.ArgumentParser(description='Preprocess any file with basic C-style macros')

parser.add_argument("-o", "--output", dest='output', metavar='OUTPUT_FILE', help='Which file to output to. Defaults to the name of the file minus ".gen"', required=False, default=None)

parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', help='Verbose mode', required=False, default=False)

parser.add_argument("input", metavar="INPUT_FILE", help="The input file to preprocess.")

args = parser.parse_args()


output_file = Path(args.input).with_suffix('')
if args.output is not None:
    output_file = args.output

inpt = open(args.input, 'r').readlines()

outpt = inpt[:]

macros={}

macro_identifier = "[a-zA-Z_]+[a-zA-Z0-9_]*"

macro_noparam_define_regex = re.compile(f"^ *#define +({macro_identifier}) +(.+)")
macro_define_regex = re.compile(f"^ *#define +({macro_identifier})(?:\(((?:{macro_identifier},)*{macro_identifier})\))? +(.+)")
macro_undefine_regex = re.compile(f"^ *#undef(?:ine)? +({macro_identifier})")

for i,l in enumerate(inpt):
    matches = re.match(macro_undefine_regex, l)
    if matches is not None:
        macro = matches[1]
        if macro not in macros:
            raise Exception(f"Macro '{macro}' was undefined whereas it wasn't defined")
        if args.verbose:
            print(f"Undefining macro '{macro}'")
        del macros[macro]
    
    matches = re.match(macro_noparam_define_regex, l)
    new_macro = None
    if matches is not None:
        macro = matches[1]
        if args.verbose:
            print(f"Defining macro '{macro}'", end='')
        value = None
        if len(matches.groups()) > 1:
            value = matches[2]
            if args.verbose:
                print(f" to '{value}'", end='')
        if args.verbose:
            print("")
        new_macro = (macro, {"expression": value, "arguments": []})
    elif (matches := re.match(macro_define_regex, l) ) is not None:
        print("Macro with params are not implemented yet!!!")
    
    for macro in macros.keys():
        macro_expr = macros[macro]["expression"]
        if macro in l and macro_expr is not None:
            if args.verbose:
                print(f"Found macro {macro}")
            replace_regex = rf'(?<=\b){macro}(?=\b)'
            #print("regex:", replace_regex)
            outpt[i] = re.sub(replace_regex, macro_expr, inpt[i])
            
    if new_macro is not None:
        macros[new_macro[0]] = new_macro[1]

if args.verbose:
    print("\n======\nOutput:\n======")
    for l in outpt:
        print(l, end='')
    
with open(output_file, 'w') as f:
    f.writelines(outpt)
    
print(f"Saved output to {output_file}")