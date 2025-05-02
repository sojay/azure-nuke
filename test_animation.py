#!/usr/bin/env python3
"""
Test script to demonstrate Azure Nuke ASCII art banners
"""
import time
from aznuke.src.animations import (
    show_startup_animation,
    show_warning_banner,
    show_completion_animation,
    BANNER,
    WARNING_BANNER,
    COMPLETE_BANNER,
    PARTIAL_COMPLETE_BANNER
)

def main():
    """Display all the ASCII art banners with delays between them"""
    print("Starting animation test...\n")
    time.sleep(1)
    
    # Show the startup banner
    show_startup_animation()
    time.sleep(2)
    
    # Show the warning banner
    show_warning_banner()
    time.sleep(2)
    
    # Show the complete banner
    print("\nTesting successful completion:")
    show_completion_animation(True, 10, 0)
    time.sleep(2)
    
    # Show the partial completion banner
    print("\nTesting completion with errors:")
    show_completion_animation(False, 8, 2)
    
    print("\nAnimation test complete!")

if __name__ == "__main__":
    main() 