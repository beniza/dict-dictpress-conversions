# Sabdatharavali Dictionary Conversion

**Malayalam-Malayalam Dictionary (1917) → dictpress Format**

This project converts the historical [Sabdatharavali](https://dict.sayahna.org/stv) (സബ്ദതരവാളി) Malayalam dictionary from XDXF format to dictpress-compatible CSV for integration into the [Olam](https://olam.in) Malayalam dictionary platform.

## Dictionary Information

- **Title**: സബ്ദതരവാളി (Sabdatharavali)
- **Author**: Sreekanteswaram Padmanabha Pillai
- **Year**: 1917
- **Type**: Malayalam-Malayalam (monolingual)
- **License**: [CC BY-SA 4.0](LICENSE)
- **Digital Source**: [Sayahna Foundation](https://dict.sayahna.org/stv)

## Statistics

- **55,643** Malayalam headwords
- **187,353** total entries (including definitions, examples, and cross-references)
- **5,970** entries with part-of-speech tags
- **Output size**: 23.3 MB CSV

## Quick Start

### Prerequisites

- Python 3.7+
- No external dependencies (uses only Python standard library)

### Convert XDXF to dictpress CSV

```bash
python src/stv_to_dictpress.py "sayahna/*.xml" output/stv-dictpress.csv
```

The conversion script will:
1. Parse all 7 XDXF files from the `sayahna/` directory
2. Extract headwords, definitions, examples, and cross-references
3. Generate dictpress-compatible CSV with proper formatting
4. Preserve Malayalam type labels (വിശദീകരണം, കവിത, പഴഞ്ചൊൽ, etc.)
5. Map part-of-speech tags to column 9 for proper categorization

## Project Structure

```
stv/
├── sayahna/           # Source XDXF files (7 files, alphabetically organized)
│   ├── 01-stv-vowels.xml      # അ-ഔ (12,596 entries)
│   ├── 02-stv-k-set.xml       # ക-ഞ (9,113 entries)
│   ├── 03-stv-ca-set.xml      # ട-ണ (3,821 entries)
│   ├── 04-stv-ta-set.xml      # ത-ന (112 entries)
│   ├── 05-stv-tha-set.xml     # പ-മ (8,492 entries)
│   ├── 06-stv-pa-set.xml      # യ-വ (8,684 entries)
│   ├── 07-stv-ya-zha-set.xml  # ശ-ഹ (12,835 entries)
│   └── xdxf_strict.dtd        # XDXF DTD schema
├── src/
│   └── stv_to_dictpress.py    # Main conversion script
├── output/
│   └── stv-dictpress-final.csv # Final dictpress-ready output (23.3 MB)
├── LICENSE                     # CC BY-SA 4.0
└── README.md                   # This file
```

## dictpress CSV Format

The output CSV follows the dictpress schema with 11 columns:

| Column | Field | Description | STV Usage |
|--------|-------|-------------|-----------|
| 0 | type | `-` (main) or `^` (definition) | Entry type marker |
| 1 | initial | First character | അ, ക, etc. |
| 2 | content | Word/definition text | Malayalam content |
| 3 | language | Language code | `malayalam` |
| 4 | notes | Optional notes | `STV (1917) adj.` |
| 5 | tsvector_language | Postgres tokenizer | Empty (needs mlphone) |
| 6 | tsvector_tokens | FTS tokens | Empty (for external tokenizer) |
| 7 | tags | Pipe-separated tags | `stv\|sabdatharavali\|adjective` |
| 8 | phones | Phonetic notations | Empty (no romanization) |
| 9 | definition-types | POS for definitions | `adjective`, `noun`, etc. |
| 10 | meta | JSON metadata | Source, author, year |

### Example Output

```csv
-,അ,അംശജ,malayalam,STV (1917) adj.,,,stv|sabdatharavali|adjective,,,"{""source"": ""sabdatharavali"", ""year"": 1917, ""author"": ""Sreekanteswaram Padmanabha Pillai"", ""grammar"": ""adj."", ""etymology"": """"}"
^,,അംശം കൊണ്ടു ജനിച്ച,malayalam,,,,,,,adjective,
^,,[വിശദീകരണം] അംശോത്ഭവൻ.,malayalam,,,,,,,adjective,
```

## Features

### Malayalam Type Labels

The conversion preserves Malayalam type indicators for better readability:

- `[വിശദീകരണം]` - Explanation
- `[ഉദാഹരണം]` - Example
- `[കവിത]` - Poem/Verse
- `[പഴഞ്ചൊൽ]` - Proverb
- `[പര്യായം]` - Synonym
- `[വിപരീതം]` - Antonym

### Part-of-Speech Mapping

The script automatically maps grammar tags to dictpress format:

| XDXF Tag | dictpress POS |
|----------|---------------|
| `adj.` | `adjective` |
| `n.` | `noun` |
| `v.` | `verb` |
| `trv.` | `transitive-verb` |

**Note**: The source data contains only `adj.` tags (5,970 entries). Other entries have no POS tags.

## Integration with Olam

### Database Import

```bash
./dictpress import --file=stv-dictpress-final.csv
```

This will create:
- Entry records for all headwords and definitions
- Relationship links between headwords and definitions
- POS-based categorization for filtering

### Malayalam Search Tokenization

The CSV is prepared for external Malayalam tokenization using [mlphone](https://gitlab.com/smc/mlphone):

```python
from mlphone import MLPhone
mlp = MLPhone()

# Generate phonetic tokens for each Malayalam entry
tokens = mlp.soundex(malayalam_word)
# Add to column 6 (tsvector_tokens) before import
```

## Data Quality

✅ **Verified**:
- All 55,643 entries successfully parsed
- Malayalam Unicode properly preserved (UTF-8)
- Nested XML elements correctly flattened
- JSON metadata properly escaped
- Cross-references maintained with type labels
- Examples and poems preserved with markers

⚠️ **Known Limitations**:
- Only 5,970 entries have POS tags (all `adj.`)
- No phonetic romanization in source data
- Requires external Malayalam tokenizer (mlphone) for full-text search

## Citation

If you use this data in academic or research work, please cite:

```
Padmanabha Pillai, Sreekanteswaram (1917). Sabdatharavali: Malayalam Dictionary.
Digital edition by Sayahna Foundation (2021).
Available at: https://dict.sayahna.org/stv
License: CC BY-SA 4.0
```

## Credits

- **Original Dictionary**: Sreekanteswaram Padmanabha Pillai (1917)
- **XDXF Digitization**: [Sayahna Foundation](http://sayahna.org)
- **Conversion**: beniza/olam-dict project (2025)

## Contributing

This is a data conversion project. The source XDXF files are maintained by the Sayahna Foundation. Issues with the source data should be reported to them.

For conversion script improvements:
1. Fork the repository
2. Make your changes
3. Test with the sample XDXF files
4. Submit a pull request

## License

The dictionary data is licensed under [CC BY-SA 4.0](LICENSE) by the Sayahna Foundation.

The conversion script (`stv_to_dictpress.py`) is released under the same license for compatibility.

## Related Projects

- [Olam Dictionary](https://olam.in) - Malayalam dictionary platform
- [Sayahna Foundation](https://dict.sayahna.org) - Digital Malayalam dictionaries
- [dictpress](https://dict.press) - Dictionary database system

---

**Last Updated**: November 2025
