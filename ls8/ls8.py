#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from examples import *

cpu = CPU()

cpu.load(program_file)
cpu.run()