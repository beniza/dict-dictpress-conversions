#!/usr/bin/env python3
"""
Test script for Gundert to dictpress converter
Runs a quick test on a sample of the data
"""

import sys
import os

# Test that required packages are installed
try:
    from bs4 import BeautifulSoup
    print("✓ beautifulsoup4 installed")
except ImportError:
    print("✗ beautifulsoup4 not found")
    print("  Install with: pip install beautifulsoup4")
    sys.exit(1)

try:
    import lxml
    print("✓ lxml installed")
except ImportError:
    print("✗ lxml not found")
    print("  Install with: pip install lxml")
    sys.exit(1)

# Import the converter
try:
    from gundert_to_dictpress import GundertParser, DictpressExporter
    print("✓ gundert_to_dictpress module loaded")
except ImportError as e:
    print(f"✗ Could not import gundert_to_dictpress: {e}")
    sys.exit(1)

def test_sample():
    """Test with a small sample of Gundert data"""
    
    # Create a small test file
    test_content = """
    <div id="transcript-content" class="contains-tei"><tei><teiheader></teiheader>
    <sourcedoc rend="lang(en) lang(ml)">
    <surface type="scan" n="105">
    <div>
    <table class="wikitable">
    <tbody><tr>
    <td>
    ആപ്പ āppa Spoon, ladle V1. (T. അകപ്പ).
    <p>ആപ്പു āppu̥ T. M. C. 1. Wedge, plug, what<lb></lb> 
    stops a crevice. ആപ്പും തട്ടി കവാടം അടെച്ചു<lb></lb> 
    (po.) bolted the door. 2. wad of gun.</p>
    </td>
    <td>
    കിണറു kiṇar̀u̥ T. M. Well (see കേണി) vu.<lb></lb> 
    കെരടു TP. കിണറും കുളവും; കിണറ്റിൻ കര.<lb></lb>
    കല്ക്കിണറു V1. കി. കുത്തുക to dig.
    </td>
    </tr></tbody>
    </table>
    </div>
    </surface>
    </sourcedoc></tei></div>
    """
    
    test_file = 'test_gundert_sample.txt'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("\n" + "=" * 70)
    print("Running test with sample data...")
    print("=" * 70)
    
    # Parse
    parser = GundertParser(test_file)
    entries = parser.parse()
    
    print(f"\nParsed {len(entries)} entries:")
    for i, entry in enumerate(entries, 1):
        print(f"\n{i}. {entry['malayalam']} ({entry['romanization']})")
        print(f"   Etymology: {entry['etymology']} ({entry['etymology_marker']})")
        print(f"   Page: {entry['page']}")
        print(f"   Definitions: {len(entry['definitions'])}")
        
        for defn in entry['definitions']:
            if defn['english']:
                print(f"     - English: {defn['english'][:80]}...")
            if defn['malayalam']:
                print(f"     - Malayalam: {defn['malayalam'][:80]}...")
    
    # Export
    test_output = 'test_output.csv'
    exporter = DictpressExporter(entries, test_output)
    exporter.export()
    
    # Show first few lines of output
    print("\n" + "=" * 70)
    print(f"Sample CSV output (first 5 lines from {test_output}):")
    print("=" * 70)
    
    with open(test_output, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            print(line.rstrip())
    
    # Cleanup
    os.remove(test_file)
    print(f"\n✓ Test completed successfully!")
    print(f"✓ Test output saved to: {test_output}")
    print("\nNext step: Run the full conversion with:")
    print("  python gundert_to_dictpress.py gundert-1872.txt gundert-dictpress.csv")

if __name__ == '__main__':
    test_sample()
