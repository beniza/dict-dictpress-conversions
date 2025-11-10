#!/usr/bin/env python3
"""
Analyze skipped lines from Bailey's dictionary conversion

This script runs the parser and exports all skipped lines to a file for review.
"""

import sys
from bailey_to_dictpress import parse_entry_line


def analyze_skipped_lines(input_file: str, output_file: str):
    """
    Parse dictionary and export all skipped lines.
    
    Args:
        input_file: Path to dictionary file
        output_file: Path to output file for skipped lines
    """
    skipped_lines = []
    parsed_count = 0
    
    print(f"Analyzing {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            entry = parse_entry_line(line, line_number)
            
            if entry:
                parsed_count += 1
            else:
                # Track non-empty, non-header lines
                if line.strip() and not line.strip().isupper():
                    skipped_lines.append((line_number, line.rstrip('\n\r')))
    
    print(f"\nResults:")
    print(f"  Parsed entries: {parsed_count}")
    print(f"  Skipped lines: {len(skipped_lines)}")
    
    # Write skipped lines to file
    print(f"\nWriting skipped lines to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"Skipped Lines Analysis - Bailey's Dictionary\n")
        f.write(f"Input: {input_file}\n")
        f.write(f"Total skipped: {len(skipped_lines)}\n")
        f.write("=" * 80 + "\n\n")
        
        for line_num, line_text in skipped_lines:
            f.write(f"Line {line_num}:\n")
            f.write(f"  {line_text}\n")
            f.write("\n")
    
    print(f"✓ Done! Skipped lines written to {output_file}")
    
    # Show first few examples
    print(f"\nFirst 10 skipped lines:")
    for line_num, line_text in skipped_lines[:10]:
        print(f"  Line {line_num}: {line_text[:70]}...")


def main():
    if len(sys.argv) != 3:
        print("Usage: python analyze_skipped.py <input_file> <output_file>")
        print("Example: python analyze_skipped.py dictionary-cleaned.txt skipped-lines.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        analyze_skipped_lines(input_file, output_file)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
