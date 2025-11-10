#!/usr/bin/env python3
"""
Test script for Bailey's dictionary converter

Tests the bailey_to_dictpress.py conversion script with sample data.
"""

import sys
import tempfile
import csv
from pathlib import Path

# Add current directory to path to import the converter
sys.path.insert(0, str(Path(__file__).parent))

from bailey_to_dictpress import parse_entry_line, BaileyEntry, convert_bailey_to_dictpress


# Sample test data from Bailey's dictionary
TEST_DATA = """ABD
A, art. ഒരു.

Aback, ad. പുറകൊട്ട, പിന്നൊക്കം.

Abandon, v. a. വിട്ടൊഴിയുന്നു, ത്യജിക്കുന്നു, പരിത്യാഗം ചെയ്യുന്നു; ഉപെക്ഷിക്കുന്നു, കൈവിടുന്നു.

Abandoned, a. വിട്ടൊഴിയപ്പെട്ട,ത്യജിക്കപ്പെട്ട; ഉപെക്ഷിക്കപ്പെട്ട, കൈവിടപ്പെട്ട; മഹാ കെട്ട, ദുഷ്ടതയുള്ള, വഷളായുള്ള, മഹാ ചീത്ത.

Ability, s. പ്രാപ്തി, സാമൎത്ഥ്യം, ശക്തി, നിപുണത, മിടുക്ക.

Abide, v. n. & a. പാൎക്കുന്നു, വസിക്കുന്നു, നിലനില്ക്കുന്നു, ഇരിക്കുന്നു; കാത്തിരിക്കുന്നു, സഹിക്കുന്നു.

Above-board, ad. പ്രത്യക്ഷമായി, മറവുകൂടാതെ, ക്രിത്രിമം കൂടാതെ.
"""


def test_parse_entry_line():
    """Test parsing individual entry lines."""
    print("\n" + "=" * 70)
    print("TEST 1: Parsing Individual Entries")
    print("=" * 70)
    
    test_cases = [
        ("A, art. ഒരു.", "A", "art", "ഒരു"),
        ("Abandon, v. a. വിട്ടൊഴിയുന്നു, ത്യജിക്കുന്നു.", "Abandon", "v. a", "വിട്ടൊഴിയുന്നു, ത്യജിക്കുന്നു"),
        ("Ability, s. പ്രാപ്തി, സാമൎത്ഥ്യം, ശക്തി.", "Ability", "s", "പ്രാപ്തി, സാമൎത്ഥ്യം, ശക്തി"),
        ("Abide, v. n. & a. പാൎക്കുന്നു, വസിക്കുന്നു.", "Abide", "v. n. & a", "പാൎക്കുന്നു, വസിക്കുന്നു"),
    ]
    
    passed = 0
    failed = 0
    
    for line, expected_hw, expected_pos, expected_def_start in test_cases:
        entry = parse_entry_line(line, 1)
        
        if entry is None:
            print(f"✗ FAILED: Could not parse: {line[:50]}...")
            failed += 1
            continue
        
        # Check headword
        if entry.headword != expected_hw:
            print(f"✗ FAILED: Headword mismatch for '{line[:40]}'")
            print(f"  Expected: {expected_hw}")
            print(f"  Got: {entry.headword}")
            failed += 1
            continue
        
        # Check POS
        if entry.pos != expected_pos:
            print(f"✗ FAILED: POS mismatch for '{entry.headword}'")
            print(f"  Expected: {expected_pos}")
            print(f"  Got: {entry.pos}")
            failed += 1
            continue
        
        # Check definitions start
        if not entry.definitions.startswith(expected_def_start):
            print(f"✗ FAILED: Definition mismatch for '{entry.headword}'")
            print(f"  Expected to start with: {expected_def_start}")
            print(f"  Got: {entry.definitions}")
            failed += 1
            continue
        
        print(f"✓ PASSED: {entry.headword} ({entry.pos})")
        passed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_pos_mapping():
    """Test POS tag normalization."""
    print("\n" + "=" * 70)
    print("TEST 2: Part-of-Speech Mapping")
    print("=" * 70)
    
    test_cases = [
        ("s", "noun"),
        ("v. a", "verb-transitive"),
        ("v. n", "verb-intransitive"),
        ("a", "adjective"),
        ("ad", "adverb"),
        ("art", "article"),
        ("pron", "pronoun"),
    ]
    
    passed = 0
    failed = 0
    
    for pos, expected_normalized in test_cases:
        entry = BaileyEntry("Test", pos, "test definition", 1)
        
        if entry.pos_normalized == expected_normalized:
            print(f"✓ PASSED: {pos} → {expected_normalized}")
            passed += 1
        else:
            print(f"✗ FAILED: {pos}")
            print(f"  Expected: {expected_normalized}")
            print(f"  Got: {entry.pos_normalized}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_full_conversion():
    """Test full conversion with sample data."""
    print("\n" + "=" * 70)
    print("TEST 3: Full Conversion")
    print("=" * 70)
    
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
        f.write(TEST_DATA)
        input_file = f.name
    
    # Create temporary output file
    output_file = tempfile.mktemp(suffix='.csv')
    
    try:
        # Run conversion
        convert_bailey_to_dictpress(input_file, output_file)
        
        # Read and verify output
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            entries = list(reader)
        
        print(f"\nConverted {len(entries)} entries")
        
        # Verify we got expected entries
        expected_headwords = ['A', 'Aback', 'Abandon', 'Abandoned', 'Ability', 'Abide', 'Above-board']
        actual_headwords = [e['headword'] for e in entries]
        
        if actual_headwords == expected_headwords:
            print(f"✓ PASSED: All expected headwords found")
            
            # Show sample entry
            sample = entries[2]  # Abandon
            print(f"\nSample entry: {sample['headword']}")
            print(f"  POS: {sample['part_of_speech']}")
            print(f"  Definition: {sample['definition'][:60]}...")
            
            return True
        else:
            print(f"✗ FAILED: Headword mismatch")
            print(f"  Expected: {expected_headwords}")
            print(f"  Got: {actual_headwords}")
            return False
    
    finally:
        # Cleanup
        Path(input_file).unlink(missing_ok=True)
        Path(output_file).unlink(missing_ok=True)


def main():
    """Run all tests."""
    print("=" * 70)
    print("Bailey Dictionary Converter - Test Suite")
    print("=" * 70)
    
    results = []
    
    # Run tests
    results.append(("Parse Entry Lines", test_parse_entry_line()))
    results.append(("POS Mapping", test_pos_mapping()))
    results.append(("Full Conversion", test_full_conversion()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
