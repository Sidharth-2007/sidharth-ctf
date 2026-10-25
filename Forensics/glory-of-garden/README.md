# Glory of the Garden

| Field | Details |
|---|---|
| **Platform** | picoCTF 2019 (CyLab) |
| **Category** | Forensics |
| **Difficulty** | Easy |
| **Tools** | wget, file, exiftool, strings, ghex |
| **Flag** | `academy{more_than_m33ts_the_3y3ee53c6bc}` |

---

## Challenge Description

> This file contains more than it seems. Get the flag from garden.jpg

**Artifact:** `garden.jpg` (2.3 MB JPEG image)

---

## Approach

The challenge provides a JPEG image file. Standard forensic methodology for image files:
1. Verify file type and integrity
2. Extract and analyze metadata (EXIF, ICC profiles, etc.)
3. Search for embedded strings or hidden data
4. If needed, inspect raw hex for anomalies

The hint "What is a hex editor?" suggests looking beyond metadata, but `strings` proved sufficient.

---

## Step-by-Step Solution

### Step 1 — Download and Verify File

```bash
$ wget https://challenge-files.cylabacademy.net/library/.../garden.jpg
$ file garden.jpg
```

```
garden.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, baseline, precision 8, 2999x2249, components 3
```

**Finding:** Valid JPEG, 2999x2249 pixels, 2.3 MB. No obvious anomalies in file type.

---

### Step 2 — Metadata Analysis with exiftool

```bash
$ exiftool garden.jpg
```

```
ExifTool Version Number         : 13.55
File Name                       : garden.jpg
Directory                       : .
File Size                       : 2.3 MB
File Type                       : JPEG
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 72
Y Resolution                    : 72
Profile CMM Type                : Linotronic
Profile Version                 : 2.1.0
Profile Class                   : Display Device Profile
Color Space Data                : RGB
Profile Connection Space        : XYZ
...
Image Width                     : 2999
Image Height                    : 2249
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2999x2249
Megapixels                      : 6.7
```

**Finding:** Metadata contains standard EXIF/ICC profile data — camera info, color profiles, resolution. No flag or suspicious fields in metadata.

---

### Step 3 — String Extraction (Primary Solution)

```bash
$ strings garden.jpg
```

```
...
s\]|."Ue
\qZf
Here is a flag: academy{more_than_m33ts_the_3y3ee53c6bc}
...
```

**Finding:** Flag embedded as plaintext string in the JPEG data section. Visible immediately in `strings` output.

---

### Step 4 — Alternative: Hex Editor Inspection

```bash
$ ghex garden.jpg
```

**Finding:** Opening in ghex (GNOME Hex Editor) reveals the same flag at offset near the end of the file, embedded after the image data. The hex view shows:
- JPEG header (`FF D8 FF E0`)
- Image data
- Flag string at offset ~0x22F000
- JPEG trailer (`FF D9`)

The flag was appended after the image data but before/within the JPEG trailer — a simple steganography technique detectable by both `strings` and hex inspection.

---

## Complete Command Summary

```bash
# 1. Download file
wget https://challenge-files.cylabacademy.net/.../garden.jpg

# 2. Verify file type
file garden.jpg

# 3. Extract metadata
exiftool garden.jpg

# 4. Find flag via strings (primary)
strings garden.jpg | grep -i flag

# 5. Alternative: hex editor inspection
ghex garden.jpg
# or
xxd garden.jpg | grep -i "academy"
```

---

## What I Learned

- **`strings` is the first line of defense** — most CTF flags embedded in images appear as plaintext and are caught instantly
- **Metadata ≠ embedded data** — EXIF/ICC profiles are separate from the image data payload; flags are often in the data section
- **JPEG structure** — `FF D8` (SOI) starts the file, `FF D9` (EOI) ends it; data between can contain appended content
- **Hex editor as backup** — when `strings` misses something (encoding, fragmentation), raw hex inspection catches it
- **Hint interpretation** — "hex editor" hint was valid but `strings` is faster for ASCII flags

---

## Flag

```
academy{more_than_m33ts_the_3y3ee53c6bc}
```