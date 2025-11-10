# Gundert Dictionary to dictpress Converter

This tool converts the TEI-encoded Gundert Malayalam-English Dictionary (1872) from the Tübingen University digitization project into dictpress-compatible CSV format for import into Olam.

## Features

- Parses TEI XML structure from Tübingen digitization
- Extracts Malayalam headwords with romanization
- Identifies etymology markers (Sanskrit, Tamil, etc.)
- Separates Malayalam and English definitions
- Preserves citations and cross-references
- Generates dictpress-compatible CSV output
- Maintains page references for citation linking

## Prerequisites

```bash
pip install -r requirements.txt
```

Required Python packages:
- `beautifulsoup4` - HTML/XML parsing
- `lxml` - XML processing backend

## Usage

### Basic Usage

```bash
python gundert_to_dictpress.py gundert-1872.txt gundert-dictpress.csv
```

### Arguments

1. **Input file** (required): Path to the Gundert TEI XML file
2. **Output file** (optional): Path for the output CSV (default: `gundert-dictpress.csv`)

### Example

```bash
# Convert Gundert dictionary to CSV
python gundert_to_dictpress.py gundert-1872.txt output.csv

# Import to dictpress (after conversion)
./dictpress import --file=output.csv
```

## Output Format

The script generates a dictpress-compatible CSV with the following structure:

### Main Entry Row
```csv
-,അ,ആപ്പ,malayalam,"Gundert (1872) p.105","","",gundert|tamil,āppa,,"{'source':'gundert','year':1872,'page':'105'}"
```

### Definition Row
```csv
^,"","Spoon, ladle",english,"TR, CG",english,"","","",noun,""
```

### CSV Columns

| Column | Description |
|--------|-------------|
| 0 | Type (`-` = main entry, `^` = definition) |
| 1 | Initial letter |
| 2 | Content (headword or definition) |
| 3 | Language (`malayalam` or `english`) |
| 4 | Notes (page reference, citations) |
| 5 | tsvector_language |
| 6 | tsvector_tokens |
| 7 | Tags (source, etymology) |
| 8 | Phones (romanization) |
| 9 | Definition types (noun, verb, etc.) |
| 10 | Meta JSON |

## Data Structure

### Entry Dictionary

```python
{
    'malayalam': 'ആപ്പ',
    'romanization': 'āppa',
    'etymology_marker': 'T.',
    'etymology': 'tamil',
    'page': '105',
    'definitions': [...]
}
```

### Definition Dictionary

```python
{
    'sense': 1,
    'malayalam': 'കവാടം അടെച്ചു',
    'english': 'Spoon, ladle',
    'citations': ['TR', 'CG'],
    'cross_refs': [
        {'type': 'see_also', 'word': 'മേലാപ്പു'}
    ]
}
```

## Etymology Markers

The script recognizes these etymology markers:

- **S.** - Sanskrit
- **T.** - Tamil
- **M.** - Malayalam
- **C.** - Canarese (Kannada)
- **Te.** - Telugu
- **Tu.** - Tulu
- **So.** - Southern dialect
- **No.** - Northern dialect
- **P.** - Persian
- **Ar.** - Arabic
- **Port.** - Portuguese
- **E.** - English
- **H.** - Hindustani

## Citation Sources

Common citation markers from Gundert:

- **TR.** - Tellicherry Records
- **Bhg.** - Bhagavad Gita
- **CG.** - (Unknown source)
- **KR.** - (Unknown source)
- **Nal.** - Nala story
- **Bhr.** - (Unknown source)
- **CC.** - (Unknown source)
- And 30+ more...

## Processing Statistics

Expected output from the full Gundert file:

- **Pages**: ~1,200+
- **Entries**: ~15,000-20,000
- **Definitions**: ~40,000-60,000
- **Languages**: Malayalam, English
- **Time**: 2-5 minutes (depending on system)

## Limitations & Known Issues

1. **Entry Boundary Detection**: Complex entries with sub-entries may not parse perfectly
2. **Part of Speech**: Currently defaults to "noun" - could be improved with NLP
3. **Compound Words**: Some compound entries may be split incorrectly
4. **Special Characters**: Some rare diacritics may need normalization
5. **Cross-references**: Links are extracted but not validated

## Post-Processing Steps

After conversion, consider:

1. **Manual Review**: Check sample entries for accuracy
2. **mlphone Tokenization**: Add Malayalam phonetic search tokens
3. **POS Tagging**: Improve part-of-speech identification
4. **Cross-reference Validation**: Verify all links exist
5. **Deduplication**: Check for duplicate entries
6. **Page Link Integration**: Add deep links to Tübingen viewer

## Integration with Olam

### Import Process

```bash
# 1. Generate CSV
python gundert_to_dictpress.py gundert-1872.txt gundert.csv

# 2. Import to dictpress database
./dictpress import --file=gundert.csv

# 3. Verify import
psql -d olam -c "SELECT COUNT(*) FROM entries WHERE tags @> '{gundert}';"
```

### Adding Original Page Links

Update templates to add "View Original" links:

```html
<!-- In entry template -->
{% if entry.meta.source == 'gundert' %}
  <a href="https://opendigi.ub.uni-tuebingen.de/opendigi/CiXIV68#p={{entry.meta.page}}" 
     target="_blank">
    View Original (p. {{entry.meta.page}})
  </a>
{% endif %}
```

## Future Enhancements

- [ ] Add Malayalam POS tagging using mlmorph
- [ ] Extract botanical/scientific names
- [ ] Identify and link compound words
- [ ] Add pronunciation audio links (if available)
- [ ] Generate WordNet mappings
- [ ] Extract usage domains (medicine, botany, etc.)
- [ ] Create etymology tree visualization
- [ ] Add morphological analysis

## Technical Details

### Malayalam Unicode Range

- **Range**: U+0D00 to U+0D7F
- **Characters**: അ-ൿ (Malayalam script)
- **Pattern**: `[അ-ൿ]+` matches Malayalam words

### Romanization System

Gundert uses a custom romanization with diacritics:
- `ṭ` `ḍ` `ṇ` `ṟ` `ḷ` (retroflex)
- `ṅ` `ṁ` `ṃ` (nasals)
- `ḥ` `ś` `ṣ` (aspirates/sibilants)
- `ā` `ī` `ū` `ṛ` (long vowels)

## License

This conversion script is provided as-is for use with the Olam project. The original Gundert dictionary is in the public domain. Tübingen digitization is licensed under "Free Access – all rights reserved".

## Contact

For issues or questions about this converter:
- Open an issue on the Olam GitHub repository
- Contact: Indic Digital Archive Foundation

## Acknowledgments

- **Hermann Gundert** - Original dictionary author (1872)
- **Tübingen University Library** - Digitization and TEI encoding
- **DFG** - Funding for digitization project
- **Indic Digital Archive Foundation** - Olam dictionary project
