# Olam Malayalam Dictionary - ETL Conversions

This repository contains ETL (Extract, Transform, Load) scripts to convert various Malayalam dictionaries into the [dictpress](https://dict.press) format for integration into [Olam.in](https://olam.in), a comprehensive Malayalam dictionary platform.

## Disclaimer

Most tasks, including coding, are accomplished with the help of AI. 

## Project Status

| Dictionary | Status | Entries | Format | Year |
|------------|--------|---------|--------|------|
| **Sabdatharavali (STV)** | ✅ Complete | 55,643 | XDXF → dictpress | 1917 |
| **Bailey's Dictionary** | 🚧 In Progress | ~18,000 | Plain text → dictpress | 1849 |
| **Gundert's Dictionary** | 🚧 In Progress | ~18,500 | TEI XML → dictpress | 1872 |

## Dictionaries

### 1. Sabdatharavali (ശബ്ദതാരാവലി) - ✅ Complete

**Malayalam-Malayalam monolingual dictionary** by Sreekanteswaram Padmanabha Pillai (1917).

- **Source**: [Sayahna Foundation](https://dict.sayahna.org/stv) (XDXF format)
- **License**: CC BY-SA 4.0
- **Output**: `stv/output/stv-dictpress-final.csv` (23.3 MB)
- **Documentation**: See [`stv/README.md`](stv/README.md)

**Quick Start:**
```bash
cd stv
python src/stv_to_dictpress.py "sayahna/*.xml" output/stv-dictpress.csv
```

### 2. Bailey's English-Malayalam Dictionary - 🚧 In Progress

**The first English-Malayalam dictionary** by Rev. Benjamin Bailey (1849), a pioneering work in Malayalam lexicography.

- **Source**: Plain text format (digitized from original print)
- **Historical Significance**: First bilingual English-Malayalam dictionary
- **Orthographic Note**: Uses pre-reform Malayalam orthography (no visible word-final chandrakkala)
- **Documentation**: See [`bailey-1849/README.md`](bailey-1849/README.md)

**Quick Start:**
```bash
cd bailey-1849
python bailey_to_dictpress.py dictionary-full.txt output/bailey-dictpress.csv
```

### 3. Gundert's Dictionary - 🚧 In Progress

**Malayalam-English dictionary** by Hermann Gundert (1872), a foundational work in Malayalam lexicography.

- **Source**: TEI XML format
- **Output Format**: dictpress CSV & SFM (Standard Format Marker)
- **Documentation**: See [`gundert-1872/QUICKSTART.md`](gundert-1872/QUICKSTART.md)

**Quick Start:**
```bash
cd gundert-1872
pip install -r requirements.txt
python gundert_to_dictpress.py gundert-1872.txt gundert-dictpress.csv
```

## About DictPress Format

[DictPress](https://dict.press) is a dictionary platform. The conversion scripts generate CSV files compatible with DictPress import requirements:

- Column structure optimized for Malayalam lexical data
- Proper handling of Unicode Malayalam text
- Preservation of etymological information
- Part-of-speech tagging where available
- Cross-reference support

## Repository Structure

```
olam-conversions/
├── stv/                      # Sabdatharavali conversion (complete)
│   ├── src/                  # Conversion scripts
│   ├── sayahna/              # Source XDXF files
│   ├── output/               # Final dictpress CSV
│   ├── analysis/             # Analysis & verification scripts
│   └── README.md             # Detailed documentation
│
├── bailey-1849/              # Bailey conversion (in progress)
│   ├── dictionary-full.txt   # Source plain text file
│   ├── bailey_to_dictpress.py
│   ├── test_converter.py
│   ├── output/               # Generated dictpress CSV
│   └── README.md
│
├── gundert-1872/             # Gundert conversion (in progress)
│   ├── gundert_to_dictpress.py
│   ├── gundert-1872.txt      # Source TEI XML
│   ├── gundert.sfm           # SFM format output
│   ├── requirements.txt
│   └── QUICKSTART.md
│
└── README.md                 # This file
```

## Prerequisites

- Python 3.7+
- Dependencies vary by project (see individual `requirements.txt` or README files)

## Contributing

This is a work in progress. Contributions, suggestions, and issue reports are welcome.

## License

- **STV Dictionary Content**: CC BY-SA 4.0 (via Sayahna Foundation)
- **Gundert Dictionary**: Public domain (published 1872)
- **Conversion Scripts**: CC BY-SA 4.0 (Copyright 2025 benVar)

## About Olam

[Olam](https://olam.in) is a comprehensive Malayalam dictionary platform that aggregates multiple lexical resources to provide rich definitions, etymologies, and usage examples for Malayalam words.
