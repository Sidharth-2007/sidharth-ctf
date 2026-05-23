# Disk, disk, sleuth! II

| Field | Details |
|---|---|
| **Platform** | picoCTF |
| **Category** | Forensics |
| **Difficulty** | Medium |
| **Tools** | The Sleuth Kit (mmls, fsstat, fls, icat) |
| **Flag** | `picoCTF{f0r3ns1c4t0r_n0v1c3_4bd721f2}` |

---

## Challenge Description

> There's something fishy going on with this disk image. Download the disk image and use the Sleuth Kit to find the flag.
> The file with the flag is named `down-at-the-bottom.txt`.

**Artifact:** `dds2-alpine.flag.img` — a raw disk image of an Alpine Linux installation.

---

## Approach

The challenge provides a raw `.img` disk image and recommends The Sleuth Kit (TSK). The core workflow for any disk image forensics challenge is:

```
mmls  →  find partition offset
fsstat  →  confirm filesystem type
fls  →  list files, find target inode
icat  →  extract file content by inode
```

The key insight is that TSK tools need an **offset** (`-o`) to correctly address the filesystem when working with partitioned disk images.

---

## Step-by-Step Solution

### Step 1 — Read the Partition Table with `mmls`

```bash
$ mmls dds2-alpine.flag.img
```

```
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

  Slot      Start        End          Length       Description
  000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
  001:  -------   0000000000   0000002047   0000002048   Unallocated
  002:  000:000   0000002048   0000262143   0000260096   Linux (0x83)
```

**Finding:** The Linux partition starts at sector **2048**. All subsequent commands need `-o 2048`.

> **Why this matters:** A raw disk image contains more than just the filesystem — it includes the partition table and unallocated space before the actual data. Without specifying the offset, TSK can't locate the filesystem and returns `Cannot determine file system type`.

---

### Step 2 — Analyze the Filesystem with `fsstat`

```bash
$ fsstat -o 2048 dds2-alpine.flag.img
```

```
File System Type: Ext3
Volume ID: dc53a3bb0ae739a5164c89db56bbb12f
Last Written at: 2021-02-16 13:21:20 (EST)
Last Mounted at: 2021-02-16 13:21:19 (EST)
Last mounted on: /os/mnt
Root Directory:  Inode 2
Free Inodes:     30605 / 32513
```

**Forensic observations:**

- **Ext3** — standard journaled Linux filesystem, confirms a real Alpine Linux install
- **Timestamps** — written and mounted within 1 second → image was created programmatically, not used interactively
- **Mount point** `/os/mnt` — reveals the challenge creator's system mounted it here during creation
- **Inode utilization** — only ~6% used (1908/32513), confirming a minimal OS installation
- **Root inode is 2** — standard for all Unix filesystems; this is where `fls` begins directory traversal

---

### Step 3 — Locate the File with `fls` and `grep`

```bash
$ fls -o 2048 -r dds2-alpine.flag.img | grep "down-at-the-bottom"
```

```
r/r 18291:    down-at-the-bottom.txt
```

**Flags used:**
- `-o 2048` — partition offset
- `-r` — recursive listing through all subdirectories (needed because the file is deeply nested)

**Output breakdown:**

```
r/r   18291   down-at-the-bottom.txt
│ │     │
│ │     └── inode number — the file's unique address on disk
│ └──────── regular file (not a directory or symlink)
└────────── allocated file (not deleted/unallocated)
```

---

### Step 4 — Extract File Content with `icat`

```bash
$ icat -o 2048 dds2-alpine.flag.img 18291
```

```
picoCTF{f0r3ns1c4t0r_n0v1c3_4bd721f2}
```

`icat` extracts file content directly using the inode number — no filepath needed. TSK operates below the directory layer, reading raw disk blocks.

---

## Complete Command Summary

```bash
# 1. Find partition offset
mmls dds2-alpine.flag.img

# 2. Confirm filesystem (always use the offset from step 1)
fsstat -o 2048 dds2-alpine.flag.img

# 3. Find the target file and its inode
fls -o 2048 -r dds2-alpine.flag.img | grep "down-at-the-bottom"

# 4. Extract the file content
icat -o 2048 dds2-alpine.flag.img 18291
```

---

## Why Not QEMU?

The challenge also hinted at booting the image with QEMU. This failed for two reasons:

1. The Alpine root account had no accessible default password — login was rejected
2. Even if it worked, booting a disk image **modifies timestamps**, making it forensically unsound

TSK reads the disk **read-only at the block level**, completely bypassing the OS. This is why it's the industry standard in real DFIR investigations — evidence integrity is preserved.

---

## What I Learned

- Every partitioned disk image requires specifying the partition offset with `-o` before TSK can read the filesystem
- `fsstat` output reveals useful investigative metadata beyond just filesystem type — mount history, timestamps, and inode utilization all tell a story
- The `r/r` prefix in `fls` output indicates file allocation status — useful for spotting deleted files (`d/d`) in more advanced challenges
- Forensic tools must operate read-only — booting suspect media is never acceptable in real investigations because it modifies evidence
- The TSK workflow (`mmls → fsstat → fls → icat`) applies universally to any raw disk image, regardless of OS or filesystem type

---

## Flag

```
picoCTF{f0r3ns1c4t0r_n0v1c3_4bd721f2}
```
