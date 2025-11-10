#!/usr/bin/env python3
"""
Bailey's English-Malayalam Dictionary (1849) to DictPress Converter

Converts Rev. Benjamin Bailey's pioneering English-Malayalam dictionary
from plain text format to DictPress-compatible CSV.

Author: ETL Conversion Project
License: Public Domain (dictionary), MIT (conversion script)
"""

import csv
import re
import sys
from typing import List, Tuple, Dict

# Part-of-speech mapping from Bailey's abbreviations to modern tags
POS_MAPPING = {
    'a': 'adjective',
    'ad': 'adverb',
    'adv': 'adverb',
    'art': 'article',
    'conj': 'conjunction',
    's': 'noun',
    'v. a': 'verb-transitive',
    'v. n': 'verb-intransitive',
    'v. a. & n': 'verb',
    'v. n. & a': 'verb',
    'prep': 'preposition',
    'pron': 'pronoun',
    'pron. poss': 'pronoun-possessive',
    'recip. pron': 'pronoun-reciprocal',
    'interj': 'interjection',
    'part': 'participle',
    'part. a': 'participle',
    'part. pass': 'participle-passive',
    'part. pass. & a': 'participle-passive',
    'pret': 'past-tense',
    'pret. & part': 'past-participle',
    'pret. & part. pass': 'past-participle-passive',
    'v. defect': 'verb-defective',
    'verb imper': 'verb-imperfect',
    'pl': 'plural',
    'plu': 'plural',
    'fem': 'feminine',
}


class BaileyEntry:
    """Represents a single dictionary entry from Bailey's dictionary."""
    
    def __init__(self, headword: str, pos: str, definitions: str, line_number: int):
        self.headword = headword.strip()
        self.pos = pos.strip() if pos else ''
        self.definitions = definitions.strip()
        self.line_number = line_number
        self.pos_normalized = POS_MAPPING.get(self.pos, self.pos)
    
    def to_dictpress_row(self) -> List[str]:
        """
        Convert entry to DictPress CSV format.
        
        DictPress CSV columns:
        1. headword (English word)
        2. alternate_headwords (empty)
        3. definition (Malayalam definitions)
        4. dictionary_name (source)
        5. tsvector_language (search tokenizer)
        6. tsvector_tokens (FTS tokens)
        7. link (empty)
        8. notes (empty)
        9. part_of_speech
        10. source_language (English)
        11. target_language (Malayalam)
        """
        return [
            self.headword,                    # 1. headword
            '',                                # 2. alternate_headwords
            self.definitions,                  # 3. definition
            "Bailey's English-Malayalam Dictionary (1849)",  # 4. dictionary_name
            '',                                # 5. tsvector_language
            '',                                # 6. tsvector_tokens
            '',                                # 7. link
            '',                                # 8. notes
            self.pos_normalized,               # 9. part_of_speech
            'English',                         # 10. source_language
            'Malayalam',                       # 11. target_language
        ]


def parse_entry_line(line: str, line_number: int) -> BaileyEntry | None:
    """
    Parse a single entry line from Bailey's dictionary.
    
    Format: Headword, pos. Malayalam_definitions.
    Example: Abandon, v. a. വിട്ടൊഴിയുന്നു, ത്യജിക്കുന്നു, പരിത്യാഗം ചെയ്യുന്നു.
    
    Returns:
        BaileyEntry object or None if the line is not an entry
    """
    line = line.strip()
    
    # Skip empty lines and section headers (all caps lines)
    if not line or line.isupper():
        return None
    
    # Entry pattern: Headword, POS. Definitions.
    # The POS section ends at the period followed by a space and Malayalam text
    # We need to find the comma, then capture everything up to ". " before Malayalam
    
    # First, find the comma that separates headword from POS
    comma_pos = line.find(',')
    if comma_pos == -1:
        return None
    
    headword = line[:comma_pos].strip()
    rest = line[comma_pos + 1:].strip()
    
    # Now find where POS ends - it's the period followed by space before Malayalam text
    # Match pattern: some English chars/periods/spaces, then ". " then Malayalam
    # We look for ". " followed by Malayalam characters (Unicode range 0D00-0D7F)
    pos_end_match = re.search(r'\.\s+[\u0D00-\u0D7F]', rest)
    
    if not pos_end_match:
        return None
    
    # The POS is everything before the period
    pos_end = pos_end_match.start()  # Position of the period
    pos = rest[:pos_end].strip()
    
    # Definitions start after ". "
    definitions = rest[pos_end + 1:].strip()  # +1 to skip the period
    
    # Remove trailing period if present
    if definitions.endswith('.'):
        definitions = definitions[:-1].strip()
    
    return BaileyEntry(headword, pos, definitions, line_number)


def convert_bailey_to_dictpress(input_file: str, output_file: str):
    """
    Convert Bailey's dictionary from plain text to DictPress CSV format.
    
    Args:
        input_file: Path to dictionary-full.txt
        output_file: Path to output CSV file
    """
    entries = []
    skipped_lines = []
    entries_with_unknown_pos = []
    
    print(f"Reading {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            entry = parse_entry_line(line, line_number)
            
            if entry:
                entries.append(entry)
                
                # Track entries with unmapped POS tags
                if entry.pos and entry.pos_normalized == entry.pos:
                    # POS wasn't found in mapping
                    entries_with_unknown_pos.append((line_number, entry.headword, entry.pos))
                
                # Progress indicator
                if len(entries) % 1000 == 0:
                    print(f"  Parsed {len(entries)} entries...")
            else:
                # Track skipped lines for debugging (except empty lines)
                if line.strip() and not line.strip().isupper():
                    skipped_lines.append((line_number, line.strip()))
    
    print(f"\n✓ Parsed {len(entries)} entries from {input_file}")
    
    # Report on data quality
    if skipped_lines:
        print(f"\n⚠ Warning: Skipped {len(skipped_lines)} non-entry lines")
        if len(skipped_lines) <= 10:
            print("  Skipped lines:")
            for line_num, line_text in skipped_lines:
                print(f"    Line {line_num}: {line_text[:70]}...")
        else:
            print(f"  First 10 skipped lines:")
            for line_num, line_text in skipped_lines[:10]:
                print(f"    Line {line_num}: {line_text[:70]}...")
            print(f"  ... and {len(skipped_lines) - 10} more")
    
    if entries_with_unknown_pos:
        print(f"\n⚠ Warning: {len(entries_with_unknown_pos)} entries have unmapped POS tags")
        # Show unique POS tags
        unique_pos = set(pos for _, _, pos in entries_with_unknown_pos)
        print(f"  Unmapped POS tags: {', '.join(sorted(unique_pos))}")
        if len(entries_with_unknown_pos) <= 5:
            print("  Examples:")
            for line_num, hw, pos in entries_with_unknown_pos:
                print(f"    Line {line_num}: {hw} ({pos})")
        else:
            print(f"  First 5 examples:")
            for line_num, hw, pos in entries_with_unknown_pos[:5]:
                print(f"    Line {line_num}: {hw} ({pos})")
    
    # Write to CSV
    print(f"\nWriting to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        
        # Write header
        writer.writerow([
            'headword',
            'alternate_headwords',
            'definition',
            'dictionary_name',
            'tsvector_language',
            'tsvector_tokens',
            'link',
            'notes',
            'part_of_speech',
            'source_language',
            'target_language'
        ])
        
        # Write entries
        for entry in entries:
            writer.writerow(entry.to_dictpress_row())
    
    print(f"\n✓ Conversion complete!")
    print(f"  Output: {output_file}")
    print(f"  Total entries: {len(entries)}")
    print(f"  Entries with mapped POS: {len(entries) - len(entries_with_unknown_pos)}")
    if entries_with_unknown_pos:
        print(f"  Entries with unmapped POS: {len(entries_with_unknown_pos)}")
    
    # Show some sample entries
    print(f"\nSample entries:")
    for i, entry in enumerate(entries[:3]):
        print(f"  {entry.headword} ({entry.pos_normalized}) -> {entry.definitions[:60]}...")


def main():
    """Main entry point for the converter."""
    if len(sys.argv) != 3:
        print("Usage: python bailey_to_dictpress.py <input_file> <output_file>")
        print("Example: python bailey_to_dictpress.py dictionary-full.txt output/bailey-dictpress.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print("=" * 70)
    print("Bailey's English-Malayalam Dictionary (1849) to DictPress Converter")
    print("=" * 70)
    
    try:
        convert_bailey_to_dictpress(input_file, output_file)
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
