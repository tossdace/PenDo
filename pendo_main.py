#!/usr/bin/env python3
"""
PenDo - Educational Penetration Testing Tool
A brute-force simulation tool for cybersecurity education and authorized testing

Author: Security Research Team
License: MIT
"""

import argparse
import sys
import time
import os
from pathlib import Path

# Import our utility modules
from utils.ui import display_banner, print_colored, setup_colors, loading_animation
from utils.bruteforce import BruteForceEngine
from utils.logger import Logger

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="PenDo - Educational Penetration Testing Tool",
        epilog="Example: python pendo.py --username admin --wordlist passwords.txt --target demo"
    )
    
    parser.add_argument(
        '--username', '-u',
        required=True,
        help='Target username for brute force simulation'
    )
    
    parser.add_argument(
        '--wordlist', '-w',
        required=True,
        help='Path to password wordlist file'
    )
    
    parser.add_argument(
        '--target', '-t',
        default='simulation',
        help='Target service (default: simulation mode)'
    )
    
    parser.add_argument(
        '--delay', '-d',
        type=float,
        default=0.5,
        help='Delay between attempts in seconds (default: 0.5)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

def validate_inputs(args):
    """Validate command line arguments."""
    errors = []
    
    # Check if wordlist file exists
    if not os.path.isfile(args.wordlist):
        errors.append(f"Wordlist file not found: {args.wordlist}")
    
    # Check delay value
    if args.delay < 0:
        errors.append("Delay must be a positive number")
    
    # Check username
    if not args.username.strip():
        errors.append("Username cannot be empty")
    
    return errors

def display_disclaimer():
    """Display ethical use disclaimer."""
    disclaimer = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                           ⚠️  DISCLAIMER ⚠️                           ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║  This tool is for EDUCATIONAL and AUTHORIZED TESTING purposes    ║
    ║  only. Only use this tool on systems you own or have explicit   ║
    ║  written permission to test.                                     ║
    ║                                                                  ║
    ║  Unauthorized access to computer systems is illegal and         ║
    ║  unethical. The developers assume no responsibility for          ║
    ║  misuse of this tool.                                           ║
    ║                                                                  ║
    ║  By using this tool, you agree to use it responsibly and        ║
    ║  in accordance with all applicable laws.                        ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print_colored(disclaimer, 'yellow')
    
    response = input("\nDo you agree to use this tool ethically? (yes/no): ").lower()
    if response not in ['yes', 'y']:
        print_colored("Ethical use agreement required. Exiting...", 'red')
        sys.exit(1)

def main():
    """Main function."""
    try:
        # Setup colors
        setup_colors()
        
        # Display banner
        display_banner()
        
        # Show disclaimer
        display_disclaimer()
        
        # Parse arguments
        args = parse_arguments()
        
        # Validate inputs
        errors = validate_inputs(args)
        if errors:
            print_colored("❌ Input validation errors:", 'red')
            for error in errors:
                print_colored(f"   • {error}", 'red')
            sys.exit(1)
        
        # Initialize logger
        logger = Logger(verbose=args.verbose)
        
        # Show loading animation
        loading_animation()
        
        # Display session info
        print_colored("\n🎯 Session Information:", 'cyan')
        print_colored(f"   Target: {args.target}", 'white')
        print_colored(f"   Username: {args.username}", 'white')
        print_colored(f"   Wordlist: {args.wordlist}", 'white')
        print_colored(f"   Delay: {args.delay}s", 'white')
        
        # Initialize brute force engine
        engine = BruteForceEngine(
            username=args.username,
            wordlist_path=args.wordlist,
            target=args.target,
            delay=args.delay,
            logger=logger
        )
        
        # Start the simulation
        print_colored("\n🚀 Starting brute force simulation...\n", 'green')
        result = engine.run()
        
        # Display results
        if result['success']:
            print_colored(f"\n✅ SUCCESS! Password found: {result['password']}", 'green')
            print_colored(f"   Attempts: {result['attempts']}", 'white')
            print_colored(f"   Time taken: {result['time_taken']:.2f}s", 'white')
        else:
            print_colored(f"\n❌ FAILED! No password found.", 'red')
            print_colored(f"   Total attempts: {result['attempts']}", 'white')
            print_colored(f"   Time taken: {result['time_taken']:.2f}s", 'white')
        
        print_colored("\n🏁 Simulation completed.", 'cyan')
        
    except KeyboardInterrupt:
        print_colored("\n\n⚡ Simulation interrupted by user.", 'yellow')
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n💥 Unexpected error: {str(e)}", 'red')
        sys.exit(1)

if __name__ == "__main__":
    main()