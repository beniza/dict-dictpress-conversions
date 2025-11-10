# Bailey's English-Malayalam Dictionary (1849)

**The First English-Malayalam Dictionary** by Rev. Benjamin Bailey

This directory contains the historical English-Malayalam dictionary compiled by Rev. Benjamin Bailey of the Church Missionary Society, published in 1849 at the Church Mission Press in Cottayam (now Kottayam), Kerala.

## Historical Significance

Bailey's 1849 dictionary holds immense importance in Malayalam lexicography and Indian linguistic history:

- **First English-Malayalam Dictionary**: This is the pioneering bilingual dictionary that enabled English learners to acquire Malayalam and Malayalam speakers to learn English
- **Companion to Malayalam-English Dictionary**: Bailey had previously published a Malayalam-English dictionary (dedicated to the Rajah's predecessor), making this the complementary counterpart
- **Early Typography**: Printed using Malayalam type at the Church Mission Press, representing early Malayalam printing technology
- **Colonial Era Documentation**: Provides insight into Malayalam language as understood and documented during the British colonial period in Travancore

## Dictionary Information

- **Title**: A Dictionary, English and Malayalim
- **Author**: Rev. Benjamin Bailey (Church Missionary Society)
- **Publisher**: Church Mission Press, Cottayam
- **Year**: 1849
- **Dedication**: His Highness the Rajah of Travancore
- **Patronage**: General Cullen (British Resident), Rajah of Travancore, Government of Fort St. George (Madras)
- **Type**: English-Malayalam (bilingual)
- **Format**: Plain text extraction from original print
- **License**: Public domain (published 1849)

## Content Structure

### Entry Format

The dictionary follows a structured format:

```
Headword, part-of-speech. Malayalam_definition1, Malayalam_definition2, Malayalam_definition3.
```

**Example entries:**
```
Abandon, v. a. വിട്ടൊഴിയുന്നു, ത്യജിക്കുന്നു, പരിത്യാഗം ചെയ്യുന്നു; ഉപെക്ഷിക്കുന്നു, കൈവിടുന്നു.

Ability, s. പ്രാപ്തി, സാമൎത്ഥ്യം, ശക്തി, നിപുണത, മിടുക്ക.

Abstemious, a. മിതമായുള്ള, പ്രമാണമായുള്ള, വ്രതമായുള്ള, അടക്കമുള്ള.
```

### Part-of-Speech Abbreviations

Bailey's dictionary uses the following abbreviated terms:

| Abbreviation | Full Form | Malayalam Context |
|--------------|-----------|-------------------|
| **a.** | adjective | വിശെഷണം |
| **ad.** | adverb | ക്രിയാവിശെഷണം |
| **conj.** | conjunction | അവ്യയം |
| **s.** | substantive (noun) | നാമം |
| **v. a.** | verb active (transitive) | സകൎമ്മക ക്രിയ |
| **v. n.** | verb neuter (intransitive) | അകൎമ്മക ക്രിയ |
| **v. a. & n.** | verb active & neuter | സകൎമ്മക-അകൎമ്മക ക്രിയ |
| **prep.** | preposition | ഉപസൎഗ്ഗം |
| **pron.** | pronoun | സൎവ്വനാമം |
| **interj.** | interjection | വ്യാക്ഷെപം |
| **part.** | participle | കൃദന്തം |
| **pret.** | preterit (past tense) | ഭൂതകാലം |

## Statistics

- **Total entries**: ~18,000+ (estimated from 55,490 lines)
- **Coverage**: A-Z complete alphabetical coverage
- **Language**: English headwords with Malayalam definitions/equivalents
- **File size**: Plain text format

## Source File

- **File**: `dictionary-full.txt`
- **Format**: Plain text with Unicode Malayalam
- **Encoding**: UTF-8
- **Lines**: 55,490

## Orthographic Notes

### Absence of Visible Chandrakkala (്)

A key characteristic of Bailey's dictionary and other early Malayalam printed works is the **absence of visible chandrakkala** at word endings (also called *meethal* or *virama*, Unicode U+0D4D). 

**What's present:**
- Chandrakkala exists in conjunct consonants (e.g., പ്ര, പ്ത, ക്ക) but in its invisible combining form
- Consonant clusters within words are properly formed

**What's missing:**
- The visible chandrakkala mark at word endings
- Example: Modern "മിടുക്ക്" (with final chandrakkala) appears as "മിടുക്ക" in Bailey's text

**Impact on the text:**
- Word-final consonants appear to have an inherent vowel by modern standards
- Words ending in pure consonants lack the visible chandrakkala marker
- Internal conjuncts are correctly rendered, but final pure consonants are not marked

**Historical context:**
- The systematic use of visible chandrakkala for word-final consonants was introduced later in Malayalam orthographic reforms
- This represents an important evolution in Malayalam script standardization
- Bailey's work reflects the orthographic conventions of mid-19th century Malayalam printing

**For conversion:**
- Modern dictpress integration may require adding word-final chandrakkala where appropriate
- Historical forms should be preserved alongside normalized forms for linguistic research
- Cross-referencing with modern spellings will enhance usability and searchability

## Historical Context

### About the Author

Rev. Benjamin Bailey (1791-1871) was a pioneering missionary, linguist, and printer who made significant contributions to Malayalam literature and education:

- Member of the Church Missionary Society
- Established printing press in Kottayam
- Created Malayalam typography and fonts
- Compiled the first Malayalam-English and English-Malayalam dictionaries
- Translated numerous religious and educational texts into Malayalam

### Publisher's Note (from 1849 Preface)

Bailey acknowledged in his preface:

> "This being the first work of the kind ever published it cannot of course be expected to be perfect or incapable of improvement... executed with no little labour, and a desire to give the correct rendering of the words in Malayalim in all their meanings."

**Known limitation noted by Bailey:**
- In letters A and B, the word "To" is not prefixed to verbs (oversight)
- This was corrected from letter C onwards

## Conversion Status

🚧 **Status**: Ready for conversion to dictpress format

**Next Steps:**
1. Develop parser for entry structure
2. Extract headwords, part-of-speech, and Malayalam definitions
3. Handle multi-definition entries (semicolon-separated)
4. Map Bailey's abbreviations to modern POS tags
5. Generate dictpress-compatible CSV

## Usage Notes

### For Researchers
- Provides insight into 19th-century Malayalam vocabulary
- Shows English loanwords and concepts being introduced to Malayalam
- Documents Malayalam orthography of the colonial period
- Valuable for historical linguistics and lexicography studies

### For Dictionary Integration
- Complements Gundert's Malayalam-English dictionary (1872)
- Provides reverse lookup capability for Malayalam learners
- Historical benchmark for Malayalam language evolution

## License

This dictionary is in the **public domain** (published 1849, copyright expired).

The conversion scripts and modern adaptations are part of the [dict-dictpress-conversions](https://github.com/beniza/dict-dictpress-conversions) project.

## Related Works

- **Sabdatharavali (1917)**: Malayalam-Malayalam dictionary by Sreekanteswaram Padmanabha Pillai
- **Gundert's Dictionary (1872)**: Malayalam-English dictionary by Hermann Gundert
- **Bailey's Malayalam-English Dictionary**: The predecessor to this work (earlier publication)

## About Olam Integration

This dictionary will be converted to [dictpress](https://dict.press) format for integration into [Olam.in](https://olam.in), providing historical English-Malayalam lexical data to complement modern resources.

---

**Compiled by**: Rev. Benjamin Bailey  
**Published**: 1849, Church Mission Press, Cottayam  
**Digital preservation**: Part of Malayalam lexicographic heritage
