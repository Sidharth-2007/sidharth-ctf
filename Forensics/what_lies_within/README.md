# What Lies Within

| Field | Details |
|---|---|
| **Platform** | cylabs |
| **Category** | Forensics |
| **Difficulty** | Medium |
| **Tools** | file, exiftool, binwalk, zsteg |
| **Flag** | `academy{h1d1ng_1n_th3_b1t5}` |

---

## Challenge Description

> There's something in the building. Can you retrieve the flag?

**Artifacts:** `buildings.png` (PNG, 657×438, 8-bit RGBA)

---

## Approach

Standard metadata analysis (`exiftool`) reveals nothing. `binwalk` finds a zlib stream but extraction yields empty data and a false-positive JBOOT header. `zsteg` (LSB steganography tool) successfully extracts the flag from the least significant bits of RGB pixel channels. This challenge demonstrates the critical distinction between **file-structure analysis** (binwalk) and **pixel-level steganography** (zsteg).

---

## Step-by-Step Solution

### Step 1 — File Verification

```bash
$ file buildings.png
```

```
buildings.png: PNG image data, 657 x 438, 8-bit/color RGBA, non-interlaced
```

**Finding:** Confirmed PNG with alpha channel (RGBA), 657×438 pixels.

---

### Step 2 — Metadata Check

```bash
$ exiftool buildings.png
```

```
ExifTool Version Number         : 13.55
File Name                       : buildings.png
Directory                       : .
File Size                       : 616 kB
File Modification Date/Time     : 2026:09:23 07:22:09+05:30
File Access Date/Time           : 2026:10:26 22:19:38+05:30
File Inode Change Date/Time     : 2026:10:26 22:19:32+05:30
File Permissions                : -rw-rw-r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 657
Image Height                    : 438
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Image Size                      : 657x438
Megapixels                      : 0.288
```

**Finding:** No suspicious metadata fields (no XMP, IPTC, or custom fields). Standard PNG structure only.

---

### Step 3 — Binwalk Analysis (File Structure)

```bash
$ binwalk buildings.png
```

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 657 x 438, 8-bit/color RGBA, non-interlaced
41            0x29            Zlib compressed data, best compression
220405        0x35CF5         JBOOT STAG header, image id: 2, timestamp 0xE6FB789D, image size: 1990138519 bytes, image JBOOT checksum: 0x1801, header JBOOT checksum: 0x986C
```

```bash
$ binwalk -e buildings.png
```

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
41            0x29            Zlib compressed data, best compression

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented
```

```bash
$ cd _buildings.png.extracted && ls -la
```

```
total 604K
-rw-rw-r-- 1 kali kali    0 Oct 26 23:02 29
-rw-rw-r-- 1 kali kali 602K Oct 26 23:02 29.zlib
```

**Finding:** 
- Binwalk identifies a zlib stream at offset 0x29 (expected — PNG IDAT chunks use zlib compression)
- The **JBOOT header at 0x35CF5 is a false positive** — random compressed data matching a firmware signature pattern
- Extraction produces an empty file (`29`) and the raw zlib stream (`29.zlib`), neither containing the flag
- **Lesson:** Binwalk examines file structure for embedded files/signatures; it cannot detect pixel-level steganography

---

### Step 4 — LSB Steganography (zsteg)

```bash
$ zsteg buildings.png
```

```
b1,rgb,lsb,xy       .. text: "academy{h1d1ng_1n_th3_b1t5}"
b2,b,lsb,xy         .. text: "XuH}p#8Iy="
b3,abgr,msb,xy      .. text: "t@Wp-_tH_v\r"
b4,r,lsb,xy         .. text: "fdD\"\"\"\" "
b4,r,msb,xy         .. text: "%Q#gpSv0c05"
b4,g,lsb,xy         .. text: "fDfffDD\"\""
b4,g,msb,xy         .. text: "f\"fff\"\"DD"
b4,b,lsb,xy         .. text: "\"$BDDDDf"
b4,b,msb,xy         .. text: "wwBDDDfUU53w"
b4,rgb,msb,xy       .. text: "dUcv%F#A`"
b4,bgr,msb,xy       .. text: " V\"c7Ga4"
b4,abgr,msb,xy      .. text: "gOC_$_@o"
```

**Finding:** The flag is found in the **first bit plane (b1), RGB channels, LSB-first, XY order** — classic LSB steganography hiding data in the least significant bits of pixel color values.

---

## Complete Command Summary

```bash
# 1. Verify file type
file buildings.png

# 2. Check metadata (none found)
exiftool buildings.png

# 3. Binwalk — file structure analysis (false positive JBOOT)
binwalk buildings.png
binwalk -e buildings.png

# 4. zsteg — pixel-level LSB analysis (success)
zsteg buildings.png
# Flag: academy{h1d1ng_1n_th3_b1t5}
```

---

## What I Learned

- **Tool selection is critical** — Binwalk and zsteg serve fundamentally different purposes:
  - **Binwalk**: File structure analysis — finds embedded files, compressed streams, firmware signatures, archive headers
  - **zsteg**: Pixel-level analysis — tests bit planes (b1, b2...), color channels (rgb, bgr, abgr), bit orders (lsb, msb), and pixel orders (xy, yx) for LSB steganography
- **False positives in binwalk** — Compressed image data (zlib/PNG IDAT) can randomly match firmware signatures like **JBOOT**; always verify extracted content
- **LSB steganography** — Hides data in the least significant bits of pixel values (R, G, B, A channels), invisible to file-structure tools
- **RGBA vs RGB** — Alpha channel provides an additional hiding place; zsteg tests `abgr`/`rgba` channel orders
- **Online alternatives** — Tools like **stylesuxx** (steganography decoder), **StegOnline**, **CyberChef** (LSB extraction recipes) can replicate zsteg functionality in-browser for quick checks
- **No metadata ≠ clean image** — Absence of EXIF/XMP/IPTC metadata doesn't mean no hidden data; pixel-level steganography leaves no file-structure traces

---

## Flag

```
academy{h1d1ng_1n_th3_b1t5}
```