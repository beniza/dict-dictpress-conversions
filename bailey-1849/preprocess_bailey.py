#!/usr/bin/env python3
"""
Preprocessing script for Bailey's Dictionary (1849)

This script cleans and normalizes the source text file to make parsing more consistent.
It handles common OCR errors, formatting inconsistencies, and spacing issues.

Usage:
    python preprocess_bailey.py dictionary-full.txt dictionary-cleaned.txt
"""

import re
import sys
from typing import List, Tuple


class PreprocessingStats:
    """Track preprocessing changes for reporting."""
    
    def __init__(self):
        self.total_lines = 0
        self.fixed_comma_to_period = 0
        self.fixed_period_to_comma = 0
        self.fixed_semicolon_to_comma = 0
        self.fixed_missing_period_after_pos = 0
        self.fixed_spacing = 0
        self.fixed_pos_variants = 0
        self.unchanged_lines = 0
        self.empty_lines = 0
        self.section_headers = 0
    
    def report(self):
        """Print preprocessing statistics."""
        print("\n" + "=" * 70)
        print("PREPROCESSING SUMMARY")
        print("=" * 70)
        print(f"Total lines processed: {self.total_lines}")
        print(f"  Entry lines (modified): {self.total_lines - self.unchanged_lines - self.empty_lines - self.section_headers}")
        print(f"  Unchanged lines: {self.unchanged_lines}")
        print(f"  Empty lines: {self.empty_lines}")
        print(f"  Section headers: {self.section_headers}")
        print(f"\nFixes applied:")
        print(f"  Comma → Period after POS: {self.fixed_comma_to_period}")
        print(f"  Period → Comma after headword: {self.fixed_period_to_comma}")
        print(f"  Semicolon → Comma after headword: {self.fixed_semicolon_to_comma}")
        print(f"  Missing period after POS: {self.fixed_missing_period_after_pos}")
        print(f"  Spacing normalization: {self.fixed_spacing}")
        print(f"  POS variant normalization: {self.fixed_pos_variants}")


def fix_period_after_headword(line: str, stats: PreprocessingStats) -> str:
    """
    Fix lines where period appears instead of comma after headword.
    Example: "Admiration. s. ആശ്ചൎയ്യം" → "Admiration, s. ആശ്ചൎയ്യം"
    """
    # Pattern: Word. POS. Malayalam
    # Look for: word followed by period, space, lowercase letters (POS), period, Malayalam
    match = re.match(r'^([A-Za-z][A-Za-z\s\-\']+)\.(\s+[a-z. &]+\.)(\s+[\u0D00-\u0D7F])', line)
    
    if match:
        headword = match.group(1)
        pos_and_space = match.group(2)
        rest = match.group(3) + line[match.end():]
        
        fixed_line = f"{headword},{pos_and_space}{rest}"
        stats.fixed_period_to_comma += 1
        return fixed_line
    
    return line


def fix_semicolon_after_headword(line: str, stats: PreprocessingStats) -> str:
    """
    Fix lines where semicolon appears instead of comma after headword.
    Example: "Barb; v. a. ക്ഷൌരം" → "Barb, v. a. ക്ഷൌരം"
    """
    # Pattern: Word; POS. Malayalam
    match = re.match(r'^([A-Za-z][A-Za-z\s\-\']+);(\s+[a-z. &]+\.)(\s+[\u0D00-\u0D7F])', line)
    
    if match:
        headword = match.group(1)
        pos_and_space = match.group(2)
        rest = match.group(3) + line[match.end():]
        
        fixed_line = f"{headword},{pos_and_space}{rest}"
        stats.fixed_semicolon_to_comma += 1
        return fixed_line
    
    return line


def fix_missing_period_after_pos(line: str, stats: PreprocessingStats) -> str:
    """
    Fix lines where period is missing after POS.
    Example: "Assistance, s സഹായം" → "Assistance, s. സഹായം"
    """
    # Find the first comma (after headword)
    first_comma = line.find(',')
    if first_comma == -1:
        return line
    
    rest = line[first_comma + 1:]
    
    # Pattern: spaces, short POS (1-15 chars of lowercase/periods/spaces), space (no period), Malayalam
    # We want to match: ", s സഹായം" or ", v. a അൎത്ഥിക്കുന്നു"
    match = re.match(r'^(\s*)([a-z. &]{1,15})(\s+)([\u0D00-\u0D7F])', rest)
    
    if match:
        spaces_before = match.group(1)
        pos = match.group(2).strip()
        spaces_after = match.group(3)
        malayalam_start = match.group(4)
        
        # Check if POS doesn't already end with a period
        if not pos.endswith('.'):
            # Add period after POS
            fixed_rest = f"{spaces_before}{pos}.{spaces_after}{malayalam_start}{rest[match.end():]}"
            fixed_line = line[:first_comma + 1] + fixed_rest
            
            stats.fixed_missing_period_after_pos += 1
            return fixed_line
    
    return line


def fix_comma_after_pos(line: str, stats: PreprocessingStats) -> str:
    """
    Fix lines where comma appears instead of period after POS.
    Example: "Able, a, പ്രാപ്തി" → "Able, a. പ്രാപ്തി"
    """
    # Pattern: Headword, POS, Malayalam
    # We look for: word, short_english_abbrev, Malayalam
    # The second comma should be a period
    
    # Find the first comma (after headword)
    first_comma = line.find(',')
    if first_comma == -1:
        return line
    
    # Look for pattern: ", [a-z. &]+, [Malayalam]"
    # Between first comma and Malayalam, there might be a comma that should be period
    rest = line[first_comma + 1:]
    
    # Match: spaces, POS abbrev (letters/periods/spaces), comma, space, Malayalam
    match = re.match(r'^(\s*)([a-z. &]+)(,)(\s+)([\u0D00-\u0D7F])', rest)
    
    if match:
        # Replace the comma (group 3) with a period
        spaces_before = match.group(1)
        pos = match.group(2)
        # comma = match.group(3)  # This should become a period
        spaces_after = match.group(4)
        malayalam_start = match.group(5)
        
        # Reconstruct with period instead of comma
        fixed_rest = f"{spaces_before}{pos}.{spaces_after}{malayalam_start}{rest[match.end():]}"
        fixed_line = line[:first_comma + 1] + fixed_rest
        
        stats.fixed_comma_to_period += 1
        return fixed_line
    
    return line


def normalize_pos_spacing(line: str, stats: PreprocessingStats) -> str:
    """
    Normalize spacing in POS abbreviations.
    Examples:
    - "v.a" → "v. a"
    - "v . a" → "v. a"
    - "s ." → "s."
    """
    original = line
    
    # Fix "v.a" → "v. a" (missing space after period)
    line = re.sub(r'\bv\.a\b', 'v. a', line)
    line = re.sub(r'\bv\.n\b', 'v. n', line)
    
    # Fix "v . a" → "v. a" (extra space before period)
    line = re.sub(r'\bv\s+\.\s+a\b', 'v. a', line)
    line = re.sub(r'\bv\s+\.\s+n\b', 'v. n', line)
    
    # Fix "s ." → "s." (space before period at end of POS)
    line = re.sub(r'\b([a-z]+)\s+\.(\s+[\u0D00-\u0D7F])', r'\1.\2', line)
    
    # Fix "v.a." → "v. a" (extra period at end)
    line = re.sub(r'\bv\.a\.', 'v. a', line)
    line = re.sub(r'\bv\.n\.', 'v. n', line)
    
    if line != original:
        stats.fixed_spacing += 1
    
    return line


def normalize_pos_variants(line: str, stats: PreprocessingStats) -> str:
    """
    Normalize POS variant spellings to standard forms.
    Examples:
    - "v.a" → "v. a"
    - "v.n" → "v. n"
    - "ad." → "ad"
    - "s. pl" → "s. plural"
    """
    original = line
    
    # Common POS standardization
    replacements = {
        r'\bv\s*\.\s*a\b': 'v. a',
        r'\bv\s*\.\s*n\b': 'v. n',
        r'\bv\s*\.\s*a\s*\.\s*&\s*n\b': 'v. a. & n',
        r'\bv\s*\.\s*n\s*\.\s*&\s*a\b': 'v. n. & a',
        r'\bs\s*\.\s*pl\b': 's. plural',
        r'\bs\s*\.\s*plu\b': 's. plural',
        r'\bpron\s*\.\s*poss\b': 'pron. possessive',
        r'\bprep\s*\.\s*&\s*ad\b': 'prep. & ad',
        r'\bad\s*\.\s*&\s*prep\b': 'ad. & prep',
    }
    
    for pattern, replacement in replacements.items():
        line = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
    
    if line != original:
        stats.fixed_pos_variants += 1
    
    return line


def preprocess_line(line: str, stats: PreprocessingStats) -> str:
    """
    Apply all preprocessing fixes to a single line.
    
    Args:
        line: Original line from the dictionary
        stats: Statistics tracker
        
    Returns:
        Cleaned line
    """
    original = line
    
    # Skip empty lines
    if not line.strip():
        stats.empty_lines += 1
        return line
    
    # Skip section headers (all caps lines)
    if line.strip().isupper():
        stats.section_headers += 1
        return line
    
    # Apply fixes in order
    # 1. Fix period/semicolon after headword (must be before other fixes)
    line = fix_period_after_headword(line, stats)
    line = fix_semicolon_after_headword(line, stats)
    
    # 2. Fix missing period after POS
    line = fix_missing_period_after_pos(line, stats)
    
    # 3. Fix comma after POS (should be period)
    line = fix_comma_after_pos(line, stats)
    
    # 4. Fix spacing issues
    line = normalize_pos_spacing(line, stats)
    
    # 5. Normalize POS variants
    line = normalize_pos_variants(line, stats)
    
    # Track if line was changed
    if line == original:
        stats.unchanged_lines += 1
    
    return line


def preprocess_dictionary(input_file: str, output_file: str):
    """
    Preprocess Bailey's dictionary source file.
    
    Args:
        input_file: Path to original dictionary-full.txt
        output_file: Path to output dictionary-cleaned.txt
    """
    stats = PreprocessingStats()
    
    print("=" * 70)
    print("Bailey's Dictionary Preprocessing")
    print("=" * 70)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print()
    
    print("Reading and preprocessing...")
    
    with open(input_file, 'r', encoding='utf-8') as f_in:
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f_out:
            for line_number, line in enumerate(f_in, start=1):
                stats.total_lines += 1
                
                # Remove trailing whitespace but keep the line ending
                line = line.rstrip('\n\r')
                
                # Preprocess the line
                cleaned = preprocess_line(line, stats)
                
                # Write with consistent line ending
                f_out.write(cleaned + '\n')
                
                # Progress indicator
                if stats.total_lines % 5000 == 0:
                    print(f"  Processed {stats.total_lines} lines...")
    
    print(f"\n✓ Preprocessing complete!")
    print(f"  Output written to: {output_file}")
    
    # Print statistics
    stats.report()


def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: python preprocess_bailey.py <input_file> <output_file>")
        print("Example: python preprocess_bailey.py dictionary-full.txt dictionary-cleaned.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        preprocess_dictionary(input_file, output_file)
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
