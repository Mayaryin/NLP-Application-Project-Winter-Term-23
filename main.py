#!/usr/bin/env python3
"""Module Docstring: A brief description of what this script does."""

# Imports
import sys
import argparse

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Script description.")
    parser.add_argument('-arg1', '--argument1', type=str, help='Description of argument1.')
    return parser.parse_args()


def perform_task():
    """Performs the main task of the script."""
    print("Performing the main task.")


def main(args):
    print("Script started.")

    # Use the command line arguments
    if args.argument1:
        print(f"Argument 1 is {args.argument1}")

    print("done")


# Entry-point check
if __name__ == '__main__':
    # Parse the command-line arguments
    arguments = parse_arguments()

    # Run the main function
    main(arguments)
