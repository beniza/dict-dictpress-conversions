#!/usr/bin/env python3
"""
Gundert Dictionary to dictpress Converter
==========================================

Converts the TEI-encoded Gundert Malayalam-English Dictionary (1872)
from Tübingen University's digitization project into dictpress format.

Usage:
    python gundert_to_dictpress.py gundert-1872.txt output.csv

Author: GitHub Copilot
Date: November 2025
"""

import re
import csv
import json
import sys
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Optional


class GundertParser:
    """Parse Gundert Dictionary TEI XML and extract structured entries"""
    
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.entries = []
        
        # Etymology marker mapping
        self.etymology_map = {
            'S.': 'sanskrit',
            'T.': 'tamil',
            'M.': 'malayalam',
            'C.': 'canarese',
            'Te.': 'telugu',
            'Tu.': 'tulu',
            'So.': 'southern',
            'No.': 'northern',
            'V1.': 'verapoli1',
            'V2.': 'verapoli2',
            'TR.': 'tellicherry',
            'P.': 'persian',
            'Ar.': 'arabic',
            'Port.': 'portuguese',
            'E.': 'english',
            'H.': 'hindustani'
        }
        
        # Citation sources
        self.citation_markers = [
            'TR.', 'Bhg.', 'CG.', 'KR.', 'TP.', 'PT.', 'AR.', 'Nal.', 'Bhr.',
            'CC.', 'RC.', 'VyM.', 'KU.', 'Mud.', 'ChVr.', 'UR.', 'GP.',
            'VCh.', 'MC.', 'MR.', 'Anj.', 'RS.', 'SiPu.', 'Bhag.', 'Nid.',
            'Arb.', 'Matsy.', 'VivR.', 'Sab.', 'Tantr.', 'VetC.', 'Asht.',
            'Gan.', 'GnP.', 'Rh.', 'PR.', 'Sk.', 'Tatw.', 'VedD.', 'KumK.',
            'Sah.', 'Anach.', 'Si Pu.'
        ]
    
    def parse(self) -> List[Dict]:
        """Parse the entire Gundert file"""
        print(f"Reading file: {self.input_file}")
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        print("Extracting entries from TEI XML...")
        page_count = 0
        entry_count = 0
        
        for surface in soup.find_all('surface', {'type': 'scan'}):
            page_num = surface.get('n')
            
            # Dictionary starts at page 23 (first actual dictionary content)
            try:
                if int(page_num) < 23:
                    continue
            except ValueError:
                continue
            
            page_count += 1
            
            # Extract entries from <p> tags (each <p> is typically one entry)
            for p in surface.find_all('p'):
                text = self.clean_text(p)
                if text and self.looks_like_entry(text):
                    entry = self.extract_entry(text, page_num)
                    if entry:
                        self.entries.append(entry)
                        entry_count += 1
            
            if page_count % 50 == 0:
                print(f"  Processed {page_count} pages, {entry_count} entries...")
        
        print(f"\nCompleted: {page_count} pages, {entry_count} total entries")
        return self.entries
    
    def looks_like_entry(self, text: str) -> bool:
        """Check if text looks like a dictionary entry"""
        # Should start with Malayalam characters followed by romanization
        pattern = r'^[അ-ൿ]+\s+[a-zA-Zṭḍṇṟḷṅṁṃḥśṣāīūṛṝḹēōàèìòùâêîôûäëïöüãõñ̤̥̄̀̃]+'
        return bool(re.match(pattern, text))
    
    def clean_text(self, element) -> str:
        """Remove XML tags and normalize text, handling line breaks properly"""
        # Convert to string
        text = str(element)
        
        # Replace line break tags with no space (they split words mid-line)
        # Example: "അക<lb></lb>ഷങ്ങൾ" should become "അക്ഷങ്ങൾ" not "അക ഷങ്ങൾ"
        text = re.sub(r'<lb\s*/?\s*></?\s*lb\s*>', '', text)
        text = re.sub(r'<lb\s*/>', '', text)
        
        # Remove remaining HTML
        text = BeautifulSoup(text, 'html.parser').get_text()
        
        # Normalize whitespace (multiple spaces to single space)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_entry(self, text: str, page_num: str) -> Optional[Dict]:
        """Extract a single dictionary entry from paragraph text"""
        # Pattern for Malayalam headword + romanization + optional etymology marker
        # Example: "അക്ഷം akšam S. (oc-ulus) 1. Eye..."
        pattern = r'^([അ-ൿ]+)\s+([a-zA-Zṭḍṇṟḷṅṁṃḥśṣāīūṛṝḹēōàèìòùâêîôûäëïöüãõñ̤̥̄̀̃]+)(?:\s+(S\.|T\.|M\.|C\.|Te\.|Tu\.|So\.|No\.|V\d\.|TR\.|P\.|Ar\.|Port\.|E\.|H\.|Tdbh\.))?(.*)$'
        
        match = re.match(pattern, text, re.DOTALL)
        if not match:
            return None
        
        malayalam = match.group(1)
        romanization = match.group(2)
        etymology_marker = match.group(3) if match.group(3) else ''
        definition_text = match.group(4).strip()
        
        # Skip very short entries that are likely parsing errors
        if len(definition_text) < 3:
            return None
        
        entry = {
            'malayalam': malayalam,
            'romanization': romanization,
            'etymology_marker': etymology_marker,
            'etymology': self.etymology_map.get(etymology_marker, ''),
            'page': page_num,
            'raw_definition': definition_text,
            'definitions': self.parse_definitions(definition_text)
        }
        
        return entry
    
    def parse_definitions(self, text: str) -> List[Dict]:
        """Parse numbered definitions, examples, and citations"""
        definitions = []
        
        # Split on numbered senses (1., 2., 3., etc.)
        sense_pattern = r'(?:^|\s)(\d+)\.\s+'
        parts = re.split(sense_pattern, text)
        
        # Handle text before first numbered sense
        if parts[0].strip() and not parts[0].strip().startswith('('):
            # This might be unnumbered definition or etymology info
            definitions.append(self.parse_single_definition(0, parts[0]))
        
        # Parse numbered senses
        for i in range(1, len(parts), 2):
            if i+1 < len(parts):
                sense_num = int(parts[i])
                sense_text = parts[i+1]
                definitions.append(self.parse_single_definition(sense_num, sense_text))
        
        return definitions
    
    def parse_single_definition(self, sense_num: int, text: str) -> Dict:
        """Parse a single definition with its components"""
        # Extract citations
        citations = self.extract_citations(text)
        
        # Extract cross-references
        cross_refs = self.extract_cross_refs(text)
        
        # Separate Malayalam and English
        malayalam_parts, english_parts = self.separate_languages(text)
        
        return {
            'sense': sense_num,
            'malayalam': ' '.join(malayalam_parts).strip(),
            'english': ' '.join(english_parts).strip(),
            'citations': citations,
            'cross_refs': cross_refs,
            'raw': text.strip()
        }
    
    def separate_languages(self, text: str) -> Tuple[List[str], List[str]]:
        """Separate Malayalam and English portions of text"""
        malayalam_parts = []
        english_parts = []
        
        # Split on sentence boundaries
        sentences = re.split(r'[.!?]\s+', text)
        
        for sent in sentences:
            # Check if sentence contains Malayalam characters
            if re.search(r'[അ-ൿ]', sent):
                malayalam_parts.append(sent)
            elif sent.strip() and len(sent.strip()) > 2:
                # Only add if it's substantial text
                english_parts.append(sent)
        
        return malayalam_parts, english_parts
    
    def extract_citations(self, text: str) -> List[str]:
        """Extract citation markers"""
        citations = []
        for marker in self.citation_markers:
            if marker in text:
                citations.append(marker.replace('.', ''))
        return list(set(citations))
    
    def extract_cross_refs(self, text: str) -> List[Dict]:
        """Extract cross-references to other entries"""
        refs = []
        
        # Pattern: (= word) or (=word)
        equals_refs = re.findall(r'\(=\s*([അ-ൿa-zA-Z]+)\)', text)
        refs.extend([{'type': 'synonym', 'word': w} for w in equals_refs])
        
        # Pattern: see word
        see_refs = re.findall(r'see\s+([അ-ൿa-zA-Z]+)', text, re.IGNORECASE)
        refs.extend([{'type': 'see_also', 'word': w} for w in see_refs])
        
        # Pattern: opp. word
        opp_refs = re.findall(r'opp\.\s+([അ-ൿa-zA-Z]+)', text)
        refs.extend([{'type': 'antonym', 'word': w} for w in opp_refs])
        
        return refs


class SFMExporter:
    """Export Gundert entries to Standard Format Markup (SFM)"""
    
    def __init__(self, entries: List[Dict], output_file: str):
        self.entries = entries
        self.output_file = output_file
    
    def export(self):
        """Generate SFM format file"""
        print(f"\nGenerating SFM file: {self.output_file}")
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            entry_count = 0
            
            for entry in self.entries:
                # Write entry separator
                f.write('\n')
                
                # \lx - Lexeme (headword in Malayalam)
                f.write(f"\\lx {entry['malayalam']}\n")
                
                # \ph - Phonetic/pronunciation (romanization)
                if entry['romanization']:
                    f.write(f"\\ph {entry['romanization']}\n")
                
                # \et - Etymology
                if entry['etymology']:
                    f.write(f"\\et {entry['etymology']}\n")
                
                # \hm - Homonym number (if needed, currently not tracked)
                # f.write(f"\\hm 1\n")
                
                # Process definitions
                for i, defn in enumerate(entry['definitions'], 1):
                    # \sn - Sense number
                    if defn['sense'] > 0:
                        f.write(f"\\sn {defn['sense']}\n")
                    
                    # \ps - Part of speech (default to noun, could be improved)
                    # f.write(f"\\ps noun\n")
                    
                    # \ge - Gloss in English
                    if defn['english'] and len(defn['english'].strip()) > 0:
                        f.write(f"\\ge {defn['english'].strip()}\n")
                    
                    # \de - Definition in English (more detailed)
                    # Using same as gloss for now
                    
                    # \dn - Definition in national language (Malayalam)
                    if defn['malayalam'] and len(defn['malayalam'].strip()) > 0:
                        f.write(f"\\dn {defn['malayalam'].strip()}\n")
                    
                    # \xv - Example sentence/usage
                    # Could extract from citations if needed
                    
                    # \cf - Cross reference
                    if defn['cross_refs']:
                        for ref in defn['cross_refs']:
                            f.write(f"\\cf {ref}\n")
                    
                    # \so - Source/citation
                    if defn['citations']:
                        citations_str = '; '.join(defn['citations'])
                        f.write(f"\\so {citations_str}\n")
                
                # \dt - Date stamp
                f.write(f"\\dt {entry['page']}/1872\n")
                
                # \rf - Reference (page number)
                f.write(f"\\rf Gundert p.{entry['page']}\n")
                
                entry_count += 1
            
            # Write end marker
            f.write('\n')
        
        print(f"Exported {entry_count} entries to SFM format")
        print(f"Success! Output saved to: {self.output_file}")


class DictpressExporter:
    """Export Gundert entries to dictpress CSV format"""
    
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
                    'source': 'gundert',
                    'year': 1872,
                    'page': entry['page'],
                    'etymology': entry['etymology']
                }, ensure_ascii=False)
                
                # Tags
                tags = ['gundert']
                if entry['etymology']:
                    tags.append(entry['etymology'])
                tag_str = '|'.join(tags)
                
                # Main entry row
                writer.writerow([
                    '-',  # type: main entry
                    entry['malayalam'][0] if entry['malayalam'] else '',  # initial
                    entry['malayalam'],  # content
                    'malayalam',  # language
                    f"Gundert (1872) p.{entry['page']}",  # notes
                    '',  # tsvector_language (Malayalam doesn't have Postgres tokenizer)
                    '',  # tsvector_tokens (will use mlphone)
                    tag_str,  # tags
                    entry['romanization'],  # phones
                    '',  # definition-types
                    meta  # meta JSON (CSV writer handles escaping automatically)
                ])
                
                entry_count += 1
                
                # Definition entries
                for defn in entry['definitions']:
                    # English definition
                    if defn['english'] and len(defn['english']) > 3:
                        writer.writerow([
                            '^',  # type: definition
                            '',  # initial
                            defn['english'].strip(),  # content
                            'english',  # language
                            ', '.join(defn['citations']) if defn['citations'] else '',  # notes with citations
                            'english',  # tsvector_language
                            '',  # tsvector_tokens
                            '',  # tags
                            '',  # phones
                            'noun',  # definition-types (default, could be improved with POS tagging)
                            ''  # meta
                        ])
                        definition_count += 1
                    
                    # Malayalam definition (if any)
                    if defn['malayalam'] and len(defn['malayalam']) > 3:
                        writer.writerow([
                            '^',  # type: definition
                            '',  # initial
                            defn['malayalam'].strip(),  # content
                            'malayalam',  # language
                            ', '.join(defn['citations']) if defn['citations'] else '',  # notes
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
    if len(sys.argv) < 2:
        print("Usage: python gundert_to_dictpress.py <input_file> [output_file] [--format=csv|sfm]")
        print("\nExamples:")
        print("  python gundert_to_dictpress.py gundert-1872.txt gundert-dictpress.csv")
        print("  python gundert_to_dictpress.py gundert-1872.txt gundert.sfm --format=sfm")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'gundert-dictpress.csv'
    
    # Determine format from file extension or --format flag
    output_format = 'csv'  # default
    for arg in sys.argv:
        if arg.startswith('--format='):
            output_format = arg.split('=')[1].lower()
    
    if output_file.endswith('.sfm'):
        output_format = 'sfm'
    
    print("=" * 70)
    print(f"Gundert Dictionary Converter (Format: {output_format.upper()})")
    print("=" * 70)
    
    # Parse Gundert file
    parser = GundertParser(input_file)
    entries = parser.parse()
    
    if not entries:
        print("\nError: No entries found!")
        sys.exit(1)
    
    # Export to requested format
    if output_format == 'sfm':
        exporter = SFMExporter(entries, output_file)
        exporter.export()
        print("\n" + "=" * 70)
        print("Next steps:")
        print("  1. Review the SFM file for accuracy")
        print("  2. Import to Toolbox, FLEx, or convert to LIFT format")
        print("  3. Use SFM2XML or similar tools for further processing")
        print("=" * 70)
    else:
        exporter = DictpressExporter(entries, output_file)
        exporter.export()
        print("\n" + "=" * 70)
        print("Next steps:")
        print("  1. Review the CSV file for accuracy")
        print("  2. Import to dictpress: ./dictpress import --file=" + output_file)
        print("  3. Add mlphone tokenization for Malayalam search")
        print("=" * 70)


if __name__ == '__main__':
    main()
