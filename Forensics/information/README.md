# information

| Field | Details |
|---|---|
| **Platform** | cylabs |
| **Category** | Forensics |
| **Difficulty** | Easy |
| **Tools** | exiftool, base64 |
| **Flag** | `academy{the_m3tadata_1s_modified}` |

---

## Challenge Description

> Files can always be changed in a secret way. Can you find the flag? cat.jpg

**Artifacts:** `cat.jpg` (JPEG, JFIF 1.02, 2560x1598)

---

## Approach

The challenge provides a JPEG image. Initial inspection with `exiftool` reveals a `License` field containing a base64-encoded string. Decoding this string yields the flag.

---

## Step-by-Step Solution

### Step 1 — File Verification

```bash
$ file cat.jpg
```

```
cat.jpg: JPEG image data, JFIF standard 1.02, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 2560x1598, components 3
```

**Finding:** Confirmed the file is a valid JPEG image.

---

### Step 2 — Metadata Extraction

```bash
$ exiftool cat.jpg
```

```
ExifTool Version Number         : 13.55
File Name                       : cat.jpg
Directory                       : .
File Size                       : 878 kB
File Modification Date/Time     : 2026:09:23 08:14:41+05:30
File Access Date/Time           : 2026:10:26 21:31:30+05:30
File Inode Change Date/Time     : 2026:10:26 21:31:26+05:30
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.02
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Current IPTC Digest             : 7a78f3d9cfb1ce42ab5a3aa30573d617
Copyright Notice                : PicoCTF
Application Record Version      : 4
XMP Toolkit                     : Image::ExifTool 13.25
License                         : YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9
Rights                          : PicoCTF
Image Width                     : 2560
Image Height                    : 1598
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2560x1598
Megapixels                      : 4.1
```

**Finding:** The `License` field contains a base64-encoded string: `YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9`. The `Copyright Notice` and `Rights` fields also reference "PicoCTF" / "PicoCTF".

---

### Step 3 — Base64 Decode

```bash
$ echo YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9 | base64 -d
```

```
academy{the_m3tadata_1s_modified}
```

**Finding:** Decoding the base64 string from the `License` field reveals the flag.

---

## Complete Command Summary

```bash
# 1. Verify file type
file cat.jpg

# 2. Extract metadata
exiftool cat.jpg

# 3. Decode base64 from License field
echo YWNhZGVteXt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9 | base64 -d
```

---

## What I Learned

- **JPEG metadata fields** — IPTC/XMP fields like `License`, `Copyright Notice`, and `Rights` can store hidden data beyond standard EXIF
- **exiftool comprehensiveness** — Parses all metadata blocks (EXIF, IPTC, XMP, ICC, etc.) making it essential for forensic image analysis
- **Base64 obfuscation** — Commonly used to hide flags in metadata fields; always check non-standard fields
- **Platform labeling** — Challenge sourced from cylabs but uses picoCTF-style flag format (`academy{...}`)

---

## Flag

```
academy{the_m3tadata_1s_modified}
```