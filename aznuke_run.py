#!/usr/bin/env python3
"""
Quick run script for aznuke CLI without installation
"""

import sys
import os

# Add the current directory to the path so we can import the aznuke package
sys.path.insert(0, os.path.abspath('.'))

from aznuke.cli import main

if __name__ == "__main__":
    main() 