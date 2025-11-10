#!/usr/bin/env python3
"""
Sabdatharavali (STV) Dictionary to dictpress Converter
=======================================================

Converts the XDXF-encoded Sabdatharavali Malayalam Dictionary (1917)
to dictpress format for Olam integration.

Usage:
    python stv_to_dictpress.py <input_files> <output.csv>
    python stv_to_dictpress.py "*.xml" stv-dictpress.csv

Author: benVar w/ GitHub Copilot
Date: November 2025
"""

import re
import csv
import json
import sys
import glob
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional


class STVParser:
    """Parse Sabdatharavali XDXF files and extract structured entries"""
    
    def __init__(self):
        self.entries = []
        
    def parse_files(self, file_pattern: str) -> List[Dict]:
        """Parse multiple XDXF files"""
        files = glob.glob(file_pattern)
        
        if not files:
            print(f"Error: No files found matching: {file_pattern}")
            return []
        
        print(f"Found {len(files)} files to process")
        
        for filepath in sorted(files):
            if filepath.endswith('.dtd'):
                continue
            print(f"\nProcessing: {filepath}")
            self.parse_file(filepath)
        
        return self.entries
    
    def parse_file(self, filepath: str) -> None:
        """Parse a single XDXF file"""
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            # Get metadata
            meta = root.find('meta_info')
            title = meta.find('title').text if meta is not None else 'STV'
            
            # Parse entries
            lexicon = root.find('lexicon')
            if lexicon is None:
                print(f"  Warning: No lexicon found in {filepath}")
                return
            
            entries = lexicon.findall('ar')
            print(f"  Found {len(entries)} entries")
            
            for ar in entries:
                entry = self.parse_entry(ar)
                if entry:
                    self.entries.append(entry)
            
        except Exception as e:
            print(f"  Error parsing {filepath}: {e}")
    
    def parse_entry(self, ar: ET.Element) -> Optional[Dict]:
        """Parse a single entry (ar element)"""
        # Get headword(s)
        k_elements = ar.findall('k')
        if not k_elements:
            return None
        
        headword = self.get_text(k_elements[0])
        if not headword:
            return None
        
        # Parse definition block
        def_element = ar.find('def')
        if def_element is None:
            return None
        
        # Extract grammar info
        gr = def_element.find('gr')
        grammar = self.get_text(gr) if gr is not None else ''
        
        # Extract definitions
        definitions = []
        
        # Get direct deftexts
        for deftext in def_element.findall('deftext'):
            text = self.get_text(deftext)
            if text:
                definitions.append({
                    'type': 'definition',
                    'text': text,
                    'language': 'malayalam'
                })
        
        # Get nested defs (for multiple senses)
        for sub_def in def_element.findall('def'):
            for deftext in sub_def.findall('deftext'):
                text = self.get_text(deftext)
                if text:
                    definitions.append({
                        'type': 'definition',
                        'text': text,
                        'language': 'malayalam'
                    })
            
            # Get explanations
            for expl in sub_def.findall('expl'):
                text = self.get_text(expl)
                if text:
                    definitions.append({
                        'type': 'explanation',
                        'text': text,
                        'language': 'malayalam'
                    })
            
            # Get examples
            for ex in sub_def.findall('ex'):
                ex_type = ex.get('type', 'exm')
                ex_orig = ex.find('ex_orig')
                ex_tran = ex.find('ex_tran')
                
                if ex_orig is not None:
                    text = self.get_text(ex_orig)
                    if text:
                        definitions.append({
                            'type': 'example',
                            'text': text,
                            'example_type': ex_type,
                            'language': 'malayalam'
                        })
        
        # Get top-level explanations
        for expl in def_element.findall('expl'):
            text = self.get_text(expl)
            if text:
                definitions.append({
                    'type': 'explanation',
                    'text': text,
                    'language': 'malayalam'
                })
        
        # Get top-level examples
        for ex in def_element.findall('ex'):
            ex_type = ex.get('type', 'exm')
            ex_orig = ex.find('ex_orig')
            
            if ex_orig is not None:
                text = self.get_text(ex_orig)
                if text:
                    definitions.append({
                        'type': 'example',
                        'text': text,
                        'example_type': ex_type,
                        'language': 'malayalam'
                    })
        
        # Get cross-references
        cross_refs = []
        sr = def_element.find('sr')
        if sr is not None:
            for kref in sr.findall('kref'):
                ref_text = self.get_text(kref)
                ref_type = kref.get('type', 'rel')
                if ref_text:
                    cross_refs.append({
                        'word': ref_text,
                        'type': ref_type
                    })
        
        # Get etymology
        etm = def_element.find('etm')
        etymology = self.get_text(etm) if etm is not None else ''
        
        return {
            'headword': headword,
            'grammar': grammar,
            'definitions': definitions,
            'cross_refs': cross_refs,
            'etymology': etymology
        }
    
    def get_text(self, element: ET.Element) -> str:
        """Extract all text from an element, including nested elements"""
        if element is None:
            return ''
        
        # Get text content including tail
        text_parts = []
        
        if element.text:
            text_parts.append(element.text)
        
        for child in element:
            # Recursively get child text
            child_text = self.get_text(child)
            if child_text:
                text_parts.append(child_text)
            
            # Handle <br> tags
            if child.tag == 'br':
                text_parts.append(' ')
            
            # Add tail text
            if child.tail:
                text_parts.append(child.tail)
        
        return ''.join(text_parts).strip()


class DictpressExporter:
    """Export STV entries to dictpress CSV format"""
    
    def __init__(self, entries: List[Dict], output_file: str):
        self.entries = entries
        self.output_file = output_file
    
    def export(self):
        """Generate dictpress-compatible CSV"""
        print(f"\nGenerating dictpress CSV: {self.output_file}")
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            entry_count = 0
            definition_count = 0
            
            for entry in self.entries:
                # Main Malayalam headword entry
                meta = json.dumps({
                    'source': 'sabdatharavali',
                    'year': 1917,
                    'author': 'Sreekanteswaram Padmanabha Pillai',
                    'grammar': entry['grammar'],
                    'etymology': entry['etymology']
                }, ensure_ascii=False)
                
                # Tags
                tags = ['stv', 'sabdatharavali']
                if entry['grammar']:
                    # Extract POS if present
                    grammar_lower = entry['grammar'].lower()
                    if 'നാമം' in grammar_lower or 'n.' in grammar_lower:
                        tags.append('noun')
                    elif 'ക്രിയ' in grammar_lower or 'v.' in grammar_lower:
                        tags.append('verb')
                    elif 'വിശേഷണം' in grammar_lower or 'adj.' in grammar_lower:
                        tags.append('adjective')
                
                tag_str = '|'.join(tags)
                
                # Main entry row
                writer.writerow([
                    '-',  # type: main entry
                    entry['headword'][0] if entry['headword'] else '',  # initial
                    entry['headword'],  # content
                    'malayalam',  # language
                    f"STV (1917) {entry['grammar']}" if entry['grammar'] else "STV (1917)",  # notes
                    '',  # tsvector_language
                    '',  # tsvector_tokens (will use mlphone)
                    tag_str,  # tags
                    '',  # phones (no romanization in STV)
                    '',  # definition-types
                    meta  # meta JSON
                ])
                
                entry_count += 1
                
                # Prepare POS for definitions (column 9)
                # Map grammar abbreviations to full English POS terms
                pos_mapping = {
                    'adj.': 'adjective',
                    'n.': 'noun',
                    'v.': 'verb',
                    'trv.': 'transitive-verb',
                    'adv.': 'adverb',
                    'pron.': 'pronoun',
                    'conj.': 'conjunction',
                    'interj.': 'interjection'
                }
                definition_pos = pos_mapping.get(entry['grammar'], entry['grammar']) if entry['grammar'] else ''
                
                # Definition entries
                for defn in entry['definitions']:
                    if len(defn['text']) < 2:
                        continue
                    
                    # Determine row type based on definition type
                    content = defn['text'].strip()
                    
                    # Add type marker for examples
                    if defn['type'] == 'example':
                        ex_type = defn.get('example_type', 'exm')
                        type_labels = {
                            'exm': 'ഉദാഹരണം',
                            'poem': 'കവിത',
                            'prv': 'പഴഞ്ചൊൽ',
                            'phr': 'പദപ്രയോഗം'
                        }
                        label = type_labels.get(ex_type, 'ഉദാഹരണം')
                        content = f"[{label}] {content}"
                    elif defn['type'] == 'explanation':
                        content = f"[വിശദീകരണം] {content}"
                    
                    writer.writerow([
                        '^',  # type: definition
                        '',  # initial
                        content,  # content
                        'malayalam',  # language
                        '',  # notes
                        '',  # tsvector_language
                        '',  # tsvector_tokens
                        '',  # tags
                        '',  # phones
                        definition_pos,  # definition-types (POS for this definition)
                        ''  # meta
                    ])
                    definition_count += 1
                
                # Add cross-references
                for ref in entry['cross_refs']:
                    ref_type_labels = {
                        'syn': 'പര്യായം',
                        'ant': 'വിപരീതം',
                        'rel': 'ബന്ധപ്പെട്ടത്',
                        'hpr': 'ഉപരിവർഗ്ഗം',
                        'hpn': 'അധോവർഗ്ഗം'
                    }
                    label = ref_type_labels.get(ref['type'], 'കാണുക')
                    
                    writer.writerow([
                        '^',  # type: definition
                        '',  # initial
                        f"[{label}] {ref['word']}",  # content
                        'malayalam',  # language
                        '',  # notes
                        '',  # tsvector_language
                        '',  # tsvector_tokens
                        '',  # tags
                        '',  # phones
                        '',  # definition-types
                        ''  # meta
                    ])
                    definition_count += 1
        
        print(f"Exported {entry_count} entries with {definition_count} definitions")
        print(f"\nSuccess! Output saved to: {self.output_file}")


def main():
    """Main execution"""
    if len(sys.argv) < 3:
        print("Usage: python stv_to_dictpress.py <input_pattern> <output.csv>")
        print("\nExamples:")
        print('  python stv_to_dictpress.py "*.xml" stv-dictpress.csv')
        print('  python stv_to_dictpress.py "01-stv-vowels.xml" stv-vowels.csv')
        sys.exit(1)
    
    input_pattern = sys.argv[1]
    output_file = sys.argv[2]
    
    print("=" * 70)
    print("Sabdatharavali Dictionary to dictpress Converter")
    print("=" * 70)
    
    # Parse STV files
    parser = STVParser()
    entries = parser.parse_files(input_pattern)
    
    if not entries:
        print("\nError: No entries found!")
        sys.exit(1)
    
    print(f"\nTotal entries parsed: {len(entries)}")
    
    # Export to dictpress format
    exporter = DictpressExporter(entries, output_file)
    exporter.export()
    
if __name__ == '__main__':
    main()
