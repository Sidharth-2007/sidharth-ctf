# Papertrail

Field | Details
--- | ---
**Platform** | CREST CTF 2.0
**Category** | OSINT
**Difficulty** | Medium
**Tools** | unzip, grep, base64, Python
**Flag** | `CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}`

---

## Challenge Description

> 9 Word documents were recovered from a backup share, along with `cover_memo.txt` explaining why. Only some of these documents actually matter.
> Flag format: `CREST{...}`

**Artifacts:** `doc_01.docx` … `doc_09.docx`, `cover_memo.txt`

---

## Approach

The cover memo indicates that R. Chen's workstation was compromised and only documents **authored by R. Chen** are relevant. This points directly at DOCX metadata — specifically the `dc:creator` field in `docProps/core.xml`. Each DOCX is a ZIP archive containing XML metadata; the author information and hidden fragments are stored in `docProps/core.xml`.

---

## Step-by-Step Solution

### Step 1 — Read the Cover Memo

```
cat cover_memo.txt
```

```
SECURITY ADVISORY — internal distribution
We believe R. Chen's workstation was compromised sometime this
month. IT recovered 9 documents from the affected backup share,
but only documents actually AUTHORED by the compromised account
are relevant -- the rest are unrelated noise from the same backup job.
```

**Finding:** The filter is "authored by R. Chen" — this maps to the `dc:creator` metadata field in DOCX files. The other 5 documents are distractors.

---

### Step 2 — Extract Core Properties from All Documents

```
for f in doc_0*.docx; do
  echo "== $f"
  unzip -p "$f" docProps/core.xml | grep -oE '<dc:creator>[^<]*|<dc:description>[^<]*|<cp:revision>[^<]*'
done
```

```
== doc_01.docx
<dc:creator>T. Nakamura</dc:creator>
<cp:revision>28</cp:revision>

== doc_02.docx
<dc:creator>R. Chen</dc:creator>
<dc:description>frag=QxZXNfYXIzX20zd</dc:description>
<cp:revision>23</cp:revision>

== doc_03.docx
<dc:creator>R. Chen</dc:creator>
<dc:description>frag=Q1JFU1R7ZDBjeF9</dc:description>
<cp:revision>11</cp:revision>

== doc_04.docx
<dc:creator>R. Chen</dc:creator>
<dc:description>frag=DRkNHQ0X3QwMH0=</dc:description>
<cp:revision>40</cp:revision>

== doc_05.docx
<dc:creator>R. Chen</dc:creator>
<dc:description>frag=jMHJlX3ByMHAzcn</dc:description>
<cp:revision>15</cp:revision>

== doc_06.docx
<dc:creator>M. Okonkwo</dc:creator>
<cp:revision>9</cp:revision>

== doc_07.docx
<dc:creator>D. Kowalski</dc:creator>
<cp:revision>5</cp:revision>

== doc_08.docx
<dc:creator>M. Okonkwo</dc:creator>
<cp:revision>58</cp:revision>

== doc_09.docx
<dc:creator>M. Okonkwo</dc:creator>
<cp:revision>12</cp:revision>
```

**Finding:** Exactly 4 documents authored by R. Chen, each containing a `frag=` base64 fragment in the `dc:description` field. The other 5 documents (T. Nakamura, M. Okonkwo, D. Kowalski) have no fragments — they are the "noise" mentioned in the memo.

---

### Step 3 — Order the Fragments

Two independent signals confirm the same order:

1. **Memo number in body text** (from `word/document.xml`): Internal Memo #1 through #4
2. **Revision count ascending**: 11, 15, 23, 40

| Order | File | Memo # | Revision | Fragment (base64) |
|-------|------|--------|----------|-------------------|
| 1 | doc_03 | #1 | 11 | `Q1JFU1R7ZDBjeF9` |
| 2 | doc_05 | #2 | 15 | `jMHJlX3ByMHAzcn` |
| 3 | doc_02 | #3 | 23 | `QxZXNfYXIzX20zd` |
| 4 | doc_04 | #4 | 40 | `DRkNHQ0X3QwMH0=` |

The fourth fragment ends with `=` (base64 padding), confirming it is the final piece.

---

### Step 4 — Concatenate and Decode

```
echo -n "Q1JFU1R7ZDBjeF9jMHJlX3ByMHAzcnQxZXNfYXIzX20zdDRkNHQ0X3QwMH0=" | base64 -d
```

```
CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}
```

**Finding:** The leading `Q1JFU1R7` decodes to `CREST{`, matching the expected flag format.

---

### Step 5 — Automated Solve Script (Python)

```python
import zipfile, re, base64, glob

frags = []
for path in sorted(glob.glob("doc_0*.docx")):
    z = zipfile.ZipFile(path)
    core = z.read("docProps/core.xml").decode()
    creator = re.search(r"<dc:creator>(.*?)</dc:creator>", core).group(1)
    desc = re.search(r"<dc:description>(.*?)</dc:description>", core).group(1)
    rev = int(re.search(r"<cp:revision>(\d+)</cp:revision>", core).group(1))
    if creator == "R. Chen" and desc.startswith("frag="):
        frags.append((rev, desc[5:]))

frags.sort()
print(base64.b64decode("".join(f for _, f in frags)).decode())
```

Output:
```
CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}
```

---

## Complete Command Summary

# 1. Read cover memo for filtering criteria
cat cover_memo.txt

# 2. Extract author, description, revision from all DOCX files
for f in doc_0*.docx; do
  echo "== $f"
  unzip -p "$f" docProps/core.xml | grep -oE '<dc:creator>[^<]*|<dc:description>[^<]*|<cp:revision>[^<]*'
done

# 3. Filter for R. Chen, sort by revision, concatenate fragments
# 4. Base64 decode
echo -n "Q1JFU1R7ZDBjeF9jMHJlX3ByMHAzcnQxZXNfYXIzX20zdDRkNHQ0X3QwMH0=" | base64 -d

---

## What I Learned

- Office documents (DOCX) carry rich metadata in `docProps/core.xml` — author (`dc:creator`), description (`dc:description`), revision count (`cp:revision`) — that survives backups and is often overlooked
- The cover memo's "authored by" wording was the critical filter: it selects documents by the `dc:creator` field, not by content
- Distractors (other authors, documents with "no fragment") punish anyone who concatenates all fragment-like strings without filtering by author
- Ordering was verified two independent ways (memo numbering in body text and revision count), and base64 padding (`=`) on the final fragment confirmed the sequence
- DOCX files are ZIP archives — `unzip -p` allows streaming XML content without full extraction, useful for quick forensic triage

---

## Flag

```
CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}
```