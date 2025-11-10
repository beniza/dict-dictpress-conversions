# Gundert Dictionary - Standard Format Markup (SFM) Export

## Overview
This document describes the SFM (Standard Format Markup) export format for the Gundert Malayalam-English Dictionary (1872).

## What is SFM?
Standard Format Markup is a plain text format used for lexicographic data interchange. It's widely supported by:
- **SIL Toolbox** (dictionary development tool)
- **SIL FieldWorks Language Explorer (FLEx)** (linguistic analysis tool)
- **LIFT (Lexicon Interchange FormaT)** - can be converted from SFM
- Various dictionary publishing tools

## File Structure

### Entry Format
Each dictionary entry starts with `\lx` (lexeme) and contains various field markers:

```
\lx Malayalam_headword
\ph romanization
\et etymology_language
\sn sense_number
\ge English_gloss
\dn Malayalam_definition
\so citation_sources
\dt date_stamp
\rf page_reference
```

### Field Markers Used

| Marker | Full Name | Description | Example |
|--------|-----------|-------------|---------|
| `\lx` | Lexeme | Malayalam headword | `\lx അഗ്നി` |
| `\ph` | Phonetic | Gundert's romanization | `\ph agni` |
| `\et` | Etymology | Source language | `\et sanskrit` |
| `\sn` | Sense Number | Definition number | `\sn 1`, `\sn 2` |
| `\ps` | Part of Speech | Grammatical category | `\ps noun` (future) |
| `\ge` | Gloss (English) | Brief English definition | `\ge Fire.` |
| `\dn` | Definition (National) | Malayalam definition/examples | `\dn അഗ്നിക്കു ബലം` |
| `\cf` | Cross-reference | See also | `\cf അക്ഷം` |
| `\so` | Source | Literary citations | `\so Bhr; KR` |
| `\dt` | Date | Page/year stamp | `\dt 28/1872` |
| `\rf` | Reference | Page citation | `\rf Gundert p.28` |

## Sample Entry

```
\lx അഗ്നി
\ph agni
\et sanskrit
\sn 1
\ge Fire.
\sn 2
\ge God of fire.
\sn 3
\dn grief ഉള്ളത്തിൽ അഗ്നി പിടിച്ചു ഞങ്ങൾക്കു SiP.
\sn 4
\ge digestive power
\dn അ വൎദ്ധിപ്പിക്ക, കെടുക്ക GP അഗ്നിക്കു ബലം ഇല്ലാത്തോർ Nid
\so Nid; GP
\dt 28/1872
\rf Gundert p.28
```

## Etymology Values

The `\et` field uses normalized language names:

| Value | Source Language |
|-------|----------------|
| `sanskrit` | Sanskrit (S.) |
| `tamil` | Tamil (T.) |
| `malayalam` | Malayalam (M.) |
| `canarese` | Kannada (C.) |
| `telugu` | Telugu (Te.) |
| `tulu` | Tulu (Tu.) |
| `persian` | Persian (P.) |
| `arabic` | Arabic (Ar.) |
| `portuguese` | Portuguese (Port.) |
| `english` | English (E.) |
| `hindustani` | Hindustani (H.) |

## Citation Abbreviations

Common source abbreviations in `\so` fields:

| Code | Source | Code | Source |
|------|--------|------|--------|
| TR | Tellicherry Records | Bhr | Bharatam |
| KR | Keralolpatti | Nal | Nala Charitam |
| CG | Chandrotsavam | RC | Ramacharitam |
| Bhg | Bhagavad Gita | PT | Puttari |
| AR | Arthashastram | TP | Tulapurushadanam |
| CC | Champuvarna | Mud | Mudrarakshasa |

*(See GUNDERT_CONVERTER_README.md for complete list of 40+ citations)*

## File Statistics

- **Total Entries**: 10,740
- **Total Lines**: ~86,000
- **File Size**: ~5-6 MB
- **Encoding**: UTF-8

## Usage Examples

### Import to SIL Toolbox
1. Open Toolbox
2. File → Import → Standard Format
3. Select `gundert.sfm`
4. Map field markers to database fields
5. Import entries

### Convert to LIFT (XML)
```bash
# Using Toolbox export
# File → Export → LIFT format

# Or using SFM2XML tool
sfm2xml gundert.sfm gundert.lift
```

### Import to FLEx (FieldWorks)
1. Open FLEx project
2. File → Import → Standard Format (Toolbox)
3. Select `gundert.sfm`
4. Configure field mappings:
   - `\lx` → Lexeme Form
   - `\ge` → Gloss
   - `\sn` → Sense Number
   - etc.
5. Import

### Process with Python
```python
# Parse SFM file
entries = []
current_entry = {}

with open('gundert.sfm', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            if current_entry:
                entries.append(current_entry)
                current_entry = {}
        elif line.startswith('\\'):
            marker, _, value = line.partition(' ')
            marker = marker[1:]  # Remove backslash
            
            if marker == 'lx':
                if current_entry:
                    entries.append(current_entry)
                current_entry = {'lexeme': value, 'senses': []}
            elif marker == 'sn':
                current_entry.setdefault('senses', []).append({})
            elif marker == 'ge':
                if 'senses' in current_entry and current_entry['senses']:
                    current_entry['senses'][-1]['gloss'] = value
            # ... handle other markers

print(f"Loaded {len(entries)} entries")
```

## Generating the SFM File

### From Source
```bash
# Generate SFM format
python gundert_to_dictpress.py gundert-1872.txt gundert.sfm --format=sfm

# Or let extension auto-detect
python gundert_to_dictpress.py gundert-1872.txt gundert.sfm
```

### Command Options
```bash
# Specify format explicitly
python gundert_to_dictpress.py input.txt output.sfm --format=sfm

# Generate both CSV and SFM
python gundert_to_dictpress.py input.txt output.csv
python gundert_to_dictpress.py input.txt output.sfm --format=sfm
```

## Validation

### Check Entry Count
```bash
# Count entries (should be 10,740)
grep -c "^\\\\lx " gundert.sfm

# Windows PowerShell
(Select-String -Pattern "^\\lx " gundert.sfm).Count
```

### Verify Structure
```python
import re

with open('gundert.sfm', 'r', encoding='utf-8') as f:
    content = f.read()

# Count markers
lx_count = len(re.findall(r'^\\lx ', content, re.MULTILINE))
ph_count = len(re.findall(r'^\\ph ', content, re.MULTILINE))
ge_count = len(re.findall(r'^\\ge ', content, re.MULTILINE))
dn_count = len(re.findall(r'^\\dn ', content, re.MULTILINE))

print(f"Lexemes: {lx_count}")
print(f"Phonetics: {ph_count}")
print(f"English glosses: {ge_count}")
print(f"Malayalam definitions: {dn_count}")
```

## Comparison with CSV Format

| Feature | SFM | CSV (dictpress) |
|---------|-----|-----------------|
| **Readability** | Human-readable | Requires parsing |
| **Editability** | Text editor | Spreadsheet/code |
| **Structure** | Hierarchical | Flat (relational) |
| **Import Tools** | Toolbox, FLEx | dictpress, databases |
| **File Size** | ~6 MB | ~3 MB |
| **Unicode Support** | ✅ Excellent | ✅ Excellent |
| **Citations** | Inline | Separate rows |
| **Cross-refs** | Dedicated field | In text |

## Limitations & Future Improvements

### Current Limitations
1. **Part of Speech**: Not currently extracted from Gundert's markers
2. **Complex Cross-refs**: Captured in text but not structured
3. **Example Sentences**: Mixed with definitions, not separated
4. **Homonym Numbers**: Not tracked (same Malayalam word different meanings)
5. **Semantic Domains**: Not categorized

### Planned Enhancements
- [ ] Extract POS from grammatical markers in definitions
- [ ] Separate example sentences with `\xv` marker
- [ ] Add `\hm` homonym numbers for disambiguation
- [ ] Include `\sd` semantic domain tags
- [ ] Add `\va` variant forms
- [ ] Include `\sy` synonyms from cross-references
- [ ] Add `\an` antonyms where indicated

## Resources

### Tools
- **SIL Toolbox**: https://software.sil.org/toolbox/
- **FLEx**: https://software.sil.org/fieldworks/
- **LIFT Format**: https://github.com/sillsdev/lift-standard

### Documentation
- **SFM Specification**: [MDF (Multi-Dictionary Formatter)](http://www.w3.org/2001/sw/BestPractices/WNET/mdf.htm)
- **LIFT Standard**: https://code.google.com/archive/p/lift-standard/

### Related Projects
- **Olam Dictionary**: https://olam.in
- **gpura.org**: https://gpura.org (Malayalam historical dictionaries)
- **Tübingen Gundert Portal**: https://gundert-project.de

## Contact & Support

- **Project**: Olam Malayalam Dictionary
- **Repository**: github.com/beniza/olam-dict
- **Format Issues**: Submit to project issue tracker

---

**Generated**: November 6, 2025  
**Version**: 1.0  
**Converter**: gundert_to_dictpress.py with SFMExporter class
