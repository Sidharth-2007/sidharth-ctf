# Riddle Registry

| Field | Details |
|---|---|
| **Platform** | picoCTF 2026 (CyLab) |
| **Category** | Forensics |
| **Difficulty** | Easy |
| **Tools** | file, exiftool, base64 |
| **Flag** | `academy{puzzl3d_m3tadata_f0und!_3cc7cea9}` |

---

## Challenge Description

> Hi, intrepid investigator! 📄🔍 You've stumbled upon a peculiar PDF filled with what seems like nothing more than garbled nonsense. But beware! Not everything is as it appears. Amidst the chaos lies a hidden treasure—an elusive flag waiting to be uncovered. Find the PDF file here Hidden Confidential Document and uncover the flag within the metadata.

**Artifacts:** `confidential.pdf`, `track.txt`

---

## Approach

The challenge provides a PDF file with visible content appearing as garbled text/blacked-out sections. The key insight is that the flag is not in the visible content but hidden in the PDF **metadata** — specifically the `Author` field, which contains a base64-encoded string. Standard forensic tools like `exiftool` can extract this metadata directly.

---

## Step-by-Step Solution

### Step 1 — File Inspection with `file`

```bash
$ file confidential.pdf
```

```
confidential.pdf: PDF document, version 1.7, 1 page(s)
```

**Finding:** Confirmed PDF 1.7 format, single page. No obvious anomalies.

---

### Step 2 — Metadata Extraction with `exiftool`

```bash
$ exiftool confidential.pdf
```

```
...
Author                          : YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0=
```

**Finding:** The `Author` field contains a base64 string (`YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0=`). This is the hidden flag.

---

### Step 3 — Base64 Decode

```bash
$ echo YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0= | base64 -d
```

```
academy{puzzl3d_m3tadata_f0und!_3cc7cea9}
```

**Finding:** Decoded flag matches expected format.

---

## Complete Command Summary

```bash
# 1. Inspect file type
file confidential.pdf

# 2. Extract metadata
exiftool confidential.pdf

# 3. Decode base64 from Author field
echo "YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0=" | base64 -d
```

---

## What I Learned

- PDF metadata fields (Author, Producer, Creator, etc.) can store hidden data — always check metadata first
- `exiftool` is the go-to tool for quick metadata extraction from PDFs and other file types
- Base64 encoding is commonly used to obfuscate flags in metadata fields
- Visual content (blacked-out text) can be a distraction — the real payload may be in metadata

---

## Flag

```
academy{puzzl3d_m3tadata_f0und!_3cc7cea9}
```