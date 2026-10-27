# Matryoshka Dolls

| Field | Details |
|---|---|
| **Platform** | picoCTF 2021 (CyLab) |
| **Category** | Forensics |
| **Difficulty** | Medium |
| **Tools** | file, exiftool, binwalk, unzip |
| **Flag** | `academy{ZNTyvSDXRNO1d0xCkBRMhAoiafpCTvgW}` |

---

## Challenge Description

> Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one? Image: dolls.jpg

**Artifact:** `dolls.jpg` (PNG image with nested embedded archives)

---

## Approach

The challenge provides an image file that appears to be a simple PNG. However, the filename extension (.jpg) is misleading — the file is actually a PNG containing nested zip archives, each embedding another PNG with another zip, recursively (like Matryoshka dolls). The solution requires recursively extracting embedded archives until reaching the final flag.

---

## Step-by-Step Solution

### Step 1 — File Inspection

```bash
$ file dolls.jpg
```

```
dolls.jpg: PNG image data, 594 x 1104, 8-bit/color RGBA, non-interlaced
```

**Finding:** The file is a PNG despite the `.jpg` extension.

---

### Step 2 — Metadata Analysis

```bash
$ exiftool dolls.jpg
```

```
...
Warning                         : [minor] Trailer data after PNG IEND chunk
...
```

**Finding:** The PNG has trailing data after the IEND chunk, indicating embedded content.

---

### Step 3 — First Extraction with binwalk

```bash
$ binwalk dolls.jpg
```

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 594 x 1104, 8-bit/color RGBA, non-interlaced
3226          0xC9A           TIFF image data, big-endian, offset of first image directory: 8
272492        0x4286C         Zip archive data, at least v2.0 to extract, compressed size: 378929, uncompressed size: 383919, name: base_images/2_c.jpg
651587        0x9F143         End of Zip archive, footer length: 22
```

```bash
$ binwalk -e dolls.jpg
```

**Finding:** A zip archive embedded at offset 0x4286C containing `base_images/2_c.jpg`.

---

### Step 4 — Recursive Extraction

**Layer 2 — 2_c.jpg:**
```bash
$ cd _dolls.jpg.extracted/base_images
$ binwalk 2_c.jpg
```
```
187707        0x2DD3B         Zip archive data, at least v2.0 to extract, name: base_images/3_c.jpg
```
Extract → `3_c.jpg` (526x1106 PNG)

**Layer 3 — 3_c.jpg:**
```bash
$ binwalk 3_c.jpg
```
```
123606        0x1E2D6         Zip archive data, at least v2.0 to extract, name: base_images/4_c.jpg
```
Extract → `4_c.jpg` (428x1104 PNG)

**Layer 4 — 4_c.jpg:**
```bash
$ binwalk 4_c.jpg
```
```
79578         0x136DA         Zip archive data, at least v1.0 to extract, compressed size: 42, name: flag.txt
```

---

### Step 5 — Flag Recovery

```bash
$ cd _4_c.jpg.extracted
$ cat flag.txt
```

```
academy{ZNTyvSDXRNO1d0xCkBRMhAoiafpCTvgW}
```

**Finding:** The final embedded zip contains `flag.txt` with the flag.

---

## Complete Command Summary

```bash
# 1. Inspect file
file dolls.jpg

# 2. Check metadata
exiftool dolls.jpg

# 3. Find embedded archives
binwalk dolls.jpg

# 4. Extract first layer
binwalk -e dolls.jpg
cd _dolls.jpg.extracted/base_images

# 4. Recursively extract each layer
binwalk -e 2_c.jpg
cd _2_c.jpg.extracted/base_images
binwalk -e 3_c.jpg
cd _3_c.jpg.extracted/base_images
binwalk -e 4_c.jpg
cd _4_c.jpg.extracted

# 5. Read flag
cat flag.txt
```

---

## What I Learned

- **File extension ≠ file type** — always verify with `file` command
- **PNG trailer data** — data after IEND chunk often indicates embedded content
- **binwalk for nested extraction** — recursively finds and extracts embedded archives
- **Matryoshka-style embedding** — files within files within files; requires patience and systematic extraction
- **PNG can embed zip archives** — PNG's chunk structure allows appending data after IEND

---

## Flag

```
academy{ZNTyvSDXRNO1d0xCkBRMhAoiafpCTvgW}
```