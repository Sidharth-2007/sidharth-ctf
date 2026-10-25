# Binary Digits

| Field | Details |
|---|---|
| **Platform** | picoCTF 2026 (CyLab) |
| **Category** | Forensics |
| **Difficulty** | Easy |
| **Tools** | head, xxd, CyberChef |
| **Flag** | `academy{h1dd3n_1n_th3_b1n4ry_75fdfb71}` |

---

## Challenge Description

> This file doesn't look like much... just a bunch of 1s and 0s. But maybe it's not just random noise. Can you recover anything meaningful from this? Download the file here.

**Artifact:** `digits.bin` — a text file containing ASCII binary digits (1s and 0s).

---

## Approach

The challenge provides a `.bin` file containing only ASCII characters `1` and `0`. Initial inspection reveals this is not raw binary data but a **binary string representation** of an image file. The pattern `1111111111011000...` corresponds to the binary encoding of image magic bytes (likely JPEG `FF D8 FF`). The solution requires converting this binary string back to raw bytes and rendering the resulting image.

---

## Step-by-Step Solution

### Step 1 — Initial Inspection with `head` and `xxd`

```bash
$ head -c 100 digits.bin
```

```
1111111111011000111111111110000000000000000100000100101001000110010010010100011000000000000000010000
```

```bash
$ xxd digits.bin | head -5
```

```
00000000: 3131 3131 3131 3131 3130 3131 3030 30  1111111111011000
00000010: 3131 3131 3131 3131 3130 3030 3030 30  1111111111100000
00000020: 3030 3030 3030 3030 3030 3130 3030 30  0000000000010000
00000030: 3031 3030 3130 3130 3031 3030 3031 31  0100101001000110
00000040: 3031 3030 3130 3031 3031 3030 3031 31  0100100101000110
```

**Finding:** The file contains only ASCII `1` (0x31) and `0` (0x30) characters — a binary string, not raw binary. The first byte `11111111` = 0xFF suggests a JPEG header (FF D8 FF) or similar image format.

---

### Step 2 — Format Recognition

The binary string `11111111 1011000...` translates to:
- `11111111` = 0xFF
- `11011000` = 0xD8
- `11111111` = 0xFF

This matches the **JPEG magic bytes**: `FF D8 FF` (start of JPEG image). Confirmed the binary string encodes a JPEG image.

---

### Step 3 — CyberChef Decode: Binary String to Image

**CyberChef Recipe:**
1. **From Binary** — Delimiter: `None` (treats entire input as continuous binary)
2. **Render Image** — Auto-detects JPEG format and displays

**Input:** Contents of `digits.bin` (pasted or loaded)
**Output:** Rendered image showing the flag

---

### Step 4 — Flag Recovery

The rendered image displays the flag clearly:
```
academy{h1dd3n_1n_th3_b1n4ry_75fdfb71}
```

**Finding:** The binary string was a direct bit-for-bit encoding of a JPEG image containing the flag as visible text.

---

## Complete Command Summary

```bash
# 1. Inspect file format
head -c 200 digits.bin
xxd digits.bin | head -10

# 2. CyberChef (GUI - no CLI equivalent)
# Recipe: From Binary (delimiter: none) → Render Image
# Input: full contents of digits.bin
```

---

## What I Learned

- **Binary string encoding** — Data can be represented as ASCII `1`/`0` strings instead of raw bytes, requiring conversion before analysis
- **Magic bytes in binary** — File signatures (JPEG `FF D8 FF`, PNG `89 50 4E 47`) are recognizable even in binary string form
- **CyberChef for rapid prototyping** — "From Binary" + "Render Image" instantly handles binary-string-to-image conversion without scripting
- **picoCTF forensics methodology** — Always inspect raw bytes first (`xxd`, `head`) to identify encoding layers before applying tools

---

## Flag

```
academy{h1dd3n_1n_th3_b1n4ry_75fdfb71}
```