# sidharth-ctf

A structured collection of CTF writeups documenting forensic analysis, reverse engineering, web exploitation, and cybersecurity challenges.

---

## About

Computer Science student from Kerala, India with a focus on **Digital Forensics and Incident Response (DFIR)** and cybersecurity. This repository serves as an active learning journal — each writeup documents not just the solution, but the methodology and concepts learned.

---

## Progress Summary

| Category | Challenges Solved |
|----------|-------------------|
| Forensics | 6 |
| OSINT | 1 |
| **Total** | **7** |

---

## Challenges by Category

### Forensics

| Challenge | Platform | Difficulty | Key Concept |
|-----------|----------|------------|-------------|
| [Binary Digits](Forensics/binary-digit/) | picoCTF 2026 (CyLab) | Easy | Binary string to image decoding |
| [Glory of the Garden](Forensics/glory-of-garden/) | picoCTF 2019 (CyLab) | Easy | `strings` extraction from JPEG |
| [Riddle Registry](Forensics/riddle-registry/) | picoCTF 2026 (CyLab) | Easy | PDF metadata (Author field) base64 |
| [Disk, disk, sleuth! II](Forensics/disk-sleuth-2/) | picoCTF | Medium | TSK disk image analysis (mmls, fls, icat) |
| [information](Forensics/information/) | cylabs | Easy | JPEG metadata (License field) base64 |
| [So Meta](Forensics/so_meta/) | picoCTF 2019 | Medium | PNG XMP metadata (Artist field) plaintext |

### OSINT

| Challenge | Platform | Difficulty | Key Concept |
|-----------|----------|------------|-------------|
| [Papertrail](osint/papertrail/) | CREST CTF 2.0 | Medium | DOCX metadata forensics (core.xml) |

---

## Repository Structure

```
sidharth-ctf/
├── Forensics/
│   ├── binary-digit/
│   ├── glory-of-garden/
│   ├── riddle-registry/
│   ├── disk-sleuth-2/
│   ├── information/
│   └── so_meta/
├── osint/
│   └── papertrail/
├── _template/
│   └── README.md
├── scripts/
│   └── update_readmes.py
└── .github/workflows/
    └── update-readmes.yml
```

---

## Tools & Methodology

**Forensics:** `exiftool`, `strings`, `binwalk`, `xxd`, `The Sleuth Kit (mmls, fsstat, fls, icat)`, `CyberChef`

**OSINT:** `exiftool`, `unzip`, `grep`, `base64`, Python scripting

**Approach:** File analysis → Metadata extraction → String/hex inspection → Targeted tooling → Documentation

---

## Automation

All index pages (root README, category READMEs) are auto-generated via GitHub Actions on every push. The update script (`scripts/update_readmes.py`) parses individual challenge READMEs and regenerates summary tables.

---

## Connect

- **Location:** Kerala, India
- **Focus:** DFIR, Cyber Forensics, CTF
- **Repository:** [github.com/Sidharth-2007/sidharth-ctf](https://github.com/Sidharth-2007/sidharth-ctf)

---

*Last updated: 2026-10-26 • Auto-generated on push*