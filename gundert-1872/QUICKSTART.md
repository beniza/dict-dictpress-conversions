# Quick Start Guide: Gundert to Olam Integration

## Step-by-Step Instructions

### 1. Install Dependencies

```bash
cd gundert-1872
pip install -r requirements.txt
```

This installs:
- `beautifulsoup4` - for parsing HTML/XML
- `lxml` - XML processing backend

### 2. Verify Installation

```bash
python test_converter.py
```

Expected output:
```
✓ beautifulsoup4 installed
✓ lxml installed
✓ gundert_to_dictpress module loaded

Running test with sample data...
Parsed 3 entries...
✓ Test completed successfully!
```

### 3. Run Full Conversion

```bash
python gundert_to_dictpress.py gundert-1872.txt gundert-dictpress.csv
```

Expected output:
```
======================================================================
Gundert Dictionary to dictpress Converter
======================================================================
Reading file: gundert-1872.txt
Extracting entries from TEI XML...
  Processed 50 pages, 412 entries...
  Processed 100 pages, 845 entries...
  ...
  Processed 1200 pages, 18,523 entries...

Completed: 1200 pages, 18,523 total entries

Generating dictpress CSV: gundert-dictpress.csv
Exported 18,523 entries with 52,341 definitions

Success! Output saved to: gundert-dictpress.csv
```

Processing time: **2-5 minutes** depending on your system.

### 4. Review Output

Open `gundert-dictpress.csv` in a text editor or spreadsheet:

```bash
# View first 20 lines
head -n 20 gundert-dictpress.csv

# Or in PowerShell
Get-Content gundert-dictpress.csv -TotalCount 20
```

Check for:
- Malayalam characters display correctly
- Romanization is present
- English definitions are clear
- Page numbers are included

### 5. Import to dictpress (Olam)

**Note**: This requires Olam's dictpress instance to be set up.

```bash
# Navigate to dictpress directory
cd /path/to/dictpress

# Import the CSV
./dictpress import --file=/path/to/gundert-dictpress.csv
```

### 6. Verify Import

Check the database:

```sql
-- Connect to PostgreSQL
psql -d olam_db

-- Count Gundert entries
SELECT COUNT(*) FROM entries WHERE tags @> '{gundert}';

-- Sample some entries
SELECT content, lang, notes 
FROM entries 
WHERE tags @> '{gundert}' 
LIMIT 10;

-- Check definitions
SELECT e1.content as headword, e2.content as definition
FROM entries e1
JOIN relations r ON e1.id = r.from_id
JOIN entries e2 ON r.to_id = e2.id
WHERE e1.tags @> '{gundert}'
LIMIT 10;
```

## Troubleshooting

### Problem: "Import bs4 could not be resolved"

**Solution**: Install dependencies
```bash
pip install beautifulsoup4 lxml
```

### Problem: "No entries found"

**Solution**: Check input file path
```bash
# Verify file exists
ls gundert-1872.txt

# Check file size (should be ~10MB+)
du -h gundert-1872.txt
```

### Problem: "Malayalam characters show as boxes"

**Solution**: Ensure UTF-8 encoding
```bash
# Check file encoding
file -i gundert-dictpress.csv

# Should show: text/plain; charset=utf-8
```

### Problem: "Import takes too long"

**Solution**: This is normal for large datasets
- Expected: 2-5 minutes for parsing
- Expected: 10-30 minutes for dictpress import
- Use `--verbose` flag to see progress

## Next Steps

After successful import:

### 1. Add Malayalam Search Tokenization

Install mlphone for Malayalam phonetic search:
```bash
pip install mlphone
```

Update entries with mlphone tokens:
```python
from mlphone import MLPhone
mlp = MLPhone()

# For each Malayalam entry
token = mlp.soundex(malayalam_word)
# Update tsvector_tokens field
```

### 2. Add Page Links to UI

Update Olam templates to link back to original Gundert pages:

```html
<!-- In entry detail template -->
{% if entry.meta.source == 'gundert' %}
  <div class="source-citation">
    <strong>Gundert (1872)</strong> p. {{ entry.meta.page }}
    <a href="https://opendigi.ub.uni-tuebingen.de/opendigi/CiXIV68#p={{ entry.meta.page }}" 
       target="_blank" 
       class="view-original">
      View Original Page →
    </a>
  </div>
{% endif %}
```

### 3. Add Source Filter

Allow users to filter by Gundert entries:

```javascript
// In search UI
<select name="source">
  <option value="">All Sources</option>
  <option value="gundert">Gundert (1872)</option>
  <option value="ekkurup">E.K. Kurup</option>
  <option value="datuk">Datuk Corpus</option>
</select>
```

### 4. Create Citation Display

Show all dictionary sources for a word:

```html
<div class="multi-source-view">
  <h3>വാക്ക്</h3>
  
  <div class="source gundert">
    <h4>Gundert (1872) · p. 312</h4>
    <ol>
      <li>A word, speech, saying</li>
      <li>Promise, assurance</li>
    </ol>
  </div>
  
  <div class="source ekkurup">
    <h4>E.K. Kurup Corpus</h4>
    <ul>
      <li>വാഗ്ദാനം, ഉറപ്പ്</li>
    </ul>
  </div>
</div>
```

### 5. Add Etymology Display

Show word origins from Gundert:

```html
{% if entry.meta.etymology %}
  <div class="etymology">
    <strong>Etymology:</strong>
    <span class="etymology-tag">{{ entry.meta.etymology }}</span>
    {% if entry.meta.etymology == 'sanskrit' %}
      <span class="lang-indicator">← Sanskrit</span>
    {% elif entry.meta.etymology == 'tamil' %}
      <span class="lang-indicator">← Tamil</span>
    {% endif %}
  </div>
{% endif %}
```

## Expected Results

After complete integration:

- ✅ **18,000+** Gundert entries searchable
- ✅ **Malayalam ↔ English** definitions
- ✅ **Page citations** for every entry
- ✅ **Etymology** tags (Sanskrit, Tamil, etc.)
- ✅ **Romanization** for pronunciation
- ✅ **Historical authority** for Malayalam words
- ✅ **Deep links** to original pages

## Success Metrics

Check these metrics after import:

```sql
-- Total Gundert entries
SELECT COUNT(DISTINCT id) FROM entries WHERE tags @> '{gundert}';
-- Expected: ~18,000

-- Total definitions from Gundert
SELECT COUNT(*) FROM entries e
JOIN relations r ON e.id = r.from_id
WHERE e.tags @> '{gundert}';
-- Expected: ~50,000

-- Languages represented
SELECT lang, COUNT(*) FROM entries WHERE tags @> '{gundert}' GROUP BY lang;
-- Expected: malayalam: ~18,000, english: ~32,000

-- Etymology breakdown
SELECT 
  meta->>'etymology' as etymology, 
  COUNT(*) 
FROM entries 
WHERE tags @> '{gundert}' 
GROUP BY etymology;
-- Expected: sanskrit: ~8,000, tamil: ~4,000, etc.
```

## Support

If you encounter issues:

1. Check the `GUNDERT_CONVERTER_README.md` for detailed documentation
2. Run `test_converter.py` to verify setup
3. Open an issue on the Olam GitHub repository
4. Contact: Indic Digital Archive Foundation

---

**Congratulations!** You're now integrating 150 years of Malayalam lexicography into Olam! 🎉
