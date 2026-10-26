# So Meta

| Field | Details |
|---|---|
| **Platform** | picoCTF 2019 |
| **Category** | Forensics |
| **Difficulty** | Medium |
| **Tools** | exiftool |
| **Flag** | `academy{s0_m3ta_d5c3711a}` |

---

## Challenge Description

> Find the flag in this picture

**Artifacts:** `pico_img.png` (PNG, 600×600, 8-bit RGB)

---

## Approach

The challenge provides a PNG image. Running `exiftool` reveals XMP metadata containing an `Artist` field with the flag directly embedded.

---

## Step-by-Step Solution

### Step 1 — File Verification

```bash
$ file pico_img.png
```

```
pico_img.png: PNG image data, 600 x 600, 8-bit/color RGB, non-interlaced
```

**Finding:** Confirmed the file is a valid PNG image (600×600, RGB).

---

### Step 2 — Metadata Extraction

```bash
$ exiftool pico_img.png
```

```
ExifTool Version Number         : 13.55
File Name                       : pico_img.png
Directory                       : .
File Size                       : 109 kB
File Modification Date/Time     : 2026:09:23 07:19:12+05:30
File Access Date/Time           : 2026:10:26 21:55:02+05:30
File Inode Change Date/Time     : 2026:10:26 21:54:54+05:30
File Permissions                : -rw-rw-r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 600
Image Height                    : 600
Bit Depth                       : 8
Color Type                      : RGB
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Software                        : Adobe ImageReady
XMP Toolkit                     : Adobe XMP Core 5.3-c011 66.145661, 2012/02/06-14:56:27
Creator Tool                    : Adobe Photoshop CS6 (Windows)
Instance ID                     : xmp.iid:A5566E73B2B811E8BC7F9A4303DF1F9B
Document ID                     : xmp.did:A5566E74B2B811E8BC7F9A4303DF1F9B
Derived From Instance ID        : xmp.iid:A5566E71B2B811E8BC7F9A4303DF1F9B
Derived From Document ID        : xmp.did:A5566E72B2B811E8BC7F9A4303DF1F9B
Artist                          : academy{s0_m3ta_d5c3711a}
Image Size                      : 600x600
Megapixels                      : 0.360
```

**Finding:** The `Artist` field in the XMP metadata contains the flag directly: `academy{s0_m3ta_d5c3711a}`. The image was created with Adobe Photoshop CS6 / Adobe ImageReady.

---

## Complete Command Summary

```bash
# 1. Verify file type
file pico_img.png

# 2. Extract metadata
exiftool pico_img.png

# 3. Flag found in Artist field
# academy{s0_m3ta_d5c3711a}
```

---

## What I Learned

- **PNG XMP metadata** — PNG files can store extensive XMP metadata (Adobe's Extensible Metadata Platform) including fields like `Artist`, `Creator Tool`, `Software`, and document identifiers
- **exiftool reads XMP** — Parses XMP blocks in PNG/JPEG/other formats, revealing fields not visible in standard EXIF
- **Artist field usage** — The `Artist` field (XMP `dc:creator`) is a common place to hide flags in CTF forensics challenges
- **Adobe software signatures** — `Software: Adobe ImageReady` and `Creator Tool: Adobe Photoshop CS6` indicate the image was edited/saved with Adobe tools, which write XMP metadata by default
- **No base64/encoding needed** — Unlike the previous `information` challenge, this flag was stored in plaintext in the metadata field

---

## Flag

```
academy{s0_m3ta_d5c3711a}
```