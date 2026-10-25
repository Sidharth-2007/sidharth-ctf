# 🔍 Forensics

Forensics challenges involve extracting hidden information from files, disk images, network captures, memory dumps, and other artifacts. These challenges closely mirror real-world **Digital Forensics and Incident Response (DFIR)** work.

---

## Solved Challenges

| Challenge | Platform | Difficulty | Key Concept | Flag |
|---|---|---|---|---|
| [Binary Digits](./binary-digit/) | picoCTF 2026 (CyLab) | Easy | Binary string to image decoding | ✅ |
| [Disk, disk, sleuth! II](./disk-sleuth-2/) | picoCTF | Medium | TSK disk image analysis | ✅ |

---

## Key Tools for Forensics

| Tool | Use Case |
|---|---|
| `mmls` | Read partition table from disk image |
| `fsstat` | Filesystem metadata analysis |
| `fls` | List files in a disk image |
| `icat` | Extract file by inode number |
| `strings` | Extract readable strings from binary files |
| `binwalk` | Detect and extract embedded files |
| `steghide` | Steganography detection/extraction |
| `wireshark` | Network packet capture analysis |
| `volatility` | Memory dump forensics |
| `exiftool` | File metadata extraction |

---

*All writeups include step-by-step commands, terminal output, and a "What I Learned" section.*
