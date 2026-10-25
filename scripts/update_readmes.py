#!/usr/bin/env python3
"""
Auto-generate README files for sidharth-ctf repository.
Generates: root README.md, Forensics/README.md, OSINT/README.md
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent
EXCLUDE_DIRS = {'.git', '.github', 'scripts', '_template', '__pycache__'}
CATEGORY_EMOJI = {
    'Forensics': '🔍',
    'OSINT': '🕵️',
    'Reverse Engineering': '🔄',
    'Web': '🌐',
    'General Skills': '⚙️',
    'Crypto': '🔐',
    'Pwn': '💥',
}
DIFF_EMOJI = {'Easy': '🟢', 'Medium': '🟡', 'Hard': '🔴'}

BANNER = r"""
███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
        sidharth-ctf
"""

CATEGORY_INTROS = {
    'Forensics': 'Forensics challenges involve extracting hidden information from files, disk images, network captures, memory dumps, and other artifacts. These challenges closely mirror real-world **Digital Forensics and Incident Response (DFIR)** work.',
    'OSINT': 'OSINT challenges focus on gathering intelligence from publicly available sources. These mirror real-world reconnaissance and threat intelligence workflows.',
    'Reverse Engineering': 'Reverse Engineering challenges require analyzing binaries, understanding program logic, and uncovering hidden functionality without source code.',
    'Web': 'Web exploitation challenges target vulnerabilities in web applications, APIs, and client-side logic.',
    'General Skills': 'General Skills challenges cover fundamental techniques useful across all CTF categories.',
    'Crypto': 'Cryptography challenges involve breaking or analyzing encryption, hashing, and encoding schemes.',
    'Pwn': 'Binary exploitation challenges focus on memory corruption, shellcode, and bypassing mitigations.',
}


def parse_challenge_readme(path: Path) -> Optional[Dict]:
    """Parse a challenge README.md and extract metadata."""
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return None

    lines = content.split('\n')

    # Title from first # heading
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.parent.name

    # Metadata table - handle both formats:
    # Format 1: | **Platform** | value |
    # Format 2: **Platform** | value (in Field | Details table)
    # Format 3: **Platform** | value (no leading/trailing pipes)
    platform = difficulty = flag = ''
    for line in lines:
        line_stripped = line.strip()
        # Format 1 & 3: **Platform** | value (with or without leading/trailing pipes)
        if '**Platform**' in line_stripped and '|' in line_stripped:
            parts = [p.strip() for p in line_stripped.split('|')]
            # Find the value after **Platform**
            for i, part in enumerate(parts):
                if '**Platform**' in part:
                    if i + 1 < len(parts):
                        platform = parts[i + 1]
                    break
        # Format 2: **Platform** | value (Field | Details) - line starts with **Platform**
        elif line_stripped.startswith('**Platform**'):
            match = re.search(r'\*\*Platform\*\*\s*\|\s*(.+)', line_stripped)
            if match:
                platform = match.group(1).strip()
        elif '**Difficulty**' in line_stripped and '|' in line_stripped:
            parts = [p.strip() for p in line_stripped.split('|')]
            for i, part in enumerate(parts):
                if '**Difficulty**' in part:
                    if i + 1 < len(parts):
                        difficulty = parts[i + 1]
                    break
        elif line_stripped.startswith('**Difficulty**'):
            match = re.search(r'\*\*Difficulty\*\*\s*\|\s*(.+)', line_stripped)
            if match:
                difficulty = match.group(1).strip()
        elif '**Flag**' in line_stripped:
            flag_match = re.search(r'`([^`]+)`', line_stripped)
            flag = flag_match.group(1) if flag_match else ''

    # Key concept from first "What I Learned" bullet
    key_concept = ''
    learned_section = False
    for line in lines:
        if '## What I Learned' in line or '## What I learned' in line:
            learned_section = True
            continue
        if learned_section and line.strip().startswith('-'):
            # Get text before em dash
            bullet = line.strip()[1:].strip()
            key_concept = bullet.split('—')[0].split('--')[0].strip()
            if not key_concept:
                key_concept = bullet.split(':')[0].strip()
            break
        if learned_section and line.startswith('##'):
            break

    # Fallback: use folder name
    if not key_concept:
        key_concept = path.parent.name.replace('-', ' ').title()

    return {
        'title': title,
        'folder': path.parent.name,
        'platform': platform,
        'difficulty': difficulty,
        'flag': flag,
        'key_concept': key_concept,
        'path': str(path.parent.relative_to(REPO_ROOT)).replace('\\', '/'),
    }


def scan_challenges() -> Dict[str, List[Dict]]:
    """Scan repository for challenge directories and parse their READMEs."""
    categories = {}

    # Known category folder mappings (actual folder -> display name)
    CATEGORY_FOLDERS = {
        'Forensics': 'Forensics',
        'osint': 'OSINT',
        'reverse-engineering': 'Reverse Engineering',
        'web': 'Web',
        'general-skills': 'General Skills',
        'crypto': 'Crypto',
        'pwn': 'Pwn',
    }

    for item in REPO_ROOT.iterdir():
        if not item.is_dir() or item.name in EXCLUDE_DIRS or item.name.startswith('.'):
            continue

        # Use mapped display name or title-case the folder name
        display_name = CATEGORY_FOLDERS.get(item.name, ' '.join(w.capitalize() for w in item.name.split('-')))
        actual_folder = item.name

        challenges = []
        for chal_dir in item.iterdir():
            if not chal_dir.is_dir():
                continue
            readme = chal_dir / 'README.md'
            if readme.exists():
                parsed = parse_challenge_readme(readme)
                if parsed:
                    challenges.append(parsed)

        if challenges:
            # Sort by difficulty (Easy first) then title
            diff_order = {'Easy': 0, 'Medium': 1, 'Hard': 2}
            challenges.sort(key=lambda c: (diff_order.get(c['difficulty'], 99), c['title']))
            categories[display_name] = challenges

    return categories


def progress_bar(count: int, total: int = 10, width: int = 16) -> str:
    """Generate a visual progress bar."""
    filled = min(int((count / max(total, 1)) * width), width)
    bar = '█' * filled + '░' * (width - filled)
    return f'`{bar}` {count}'


def generate_tree(categories: Dict[str, List[Dict]]) -> str:
    """Generate hacker-style tree structure."""
    lines = ['```', 'sidharth-ctf/']
    cat_names = sorted(categories.keys())

    for i, cat in enumerate(cat_names):
        is_last_cat = i == len(cat_names) - 1
        prefix = '└── ' if is_last_cat else '├── '
        emoji = CATEGORY_EMOJI.get(cat, '📁')
        lines.append(f'{prefix}{emoji} {cat}/')

        challenges = categories[cat]
        for j, chal in enumerate(challenges):
            is_last_chal = j == len(challenges) - 1
            if is_last_cat:
                chal_prefix = '    └── '
            else:
                chal_prefix = '│   └── ' if is_last_chal else '│   ├── '

            diff_emoji = DIFF_EMOJI.get(chal['difficulty'], '')
            lines.append(f'{chal_prefix}{chal["folder"]}/  ▸ {chal["platform"]}  ▸ {diff_emoji} {chal["difficulty"]}')

    lines.append('```')
    return '\n'.join(lines)


def generate_category_table(category: str, challenges: List[Dict], show_flag: bool = False) -> str:
    """Generate markdown table for a category."""
    emoji = CATEGORY_EMOJI.get(category, '📁')
    lines = [f'### {emoji} {category.upper()}']

    if show_flag:
        lines.append('| Challenge | Platform | Diff | Key Concept | Flag |')
        lines.append('|-----------|----------|------|-------------|------|')
        for c in challenges:
            diff_emoji = DIFF_EMOJI.get(c['difficulty'], '')
            lines.append(f'| [{c["title"]}]({c["path"]}/) | {c["platform"]} | {diff_emoji} {c["difficulty"]} | {c["key_concept"]} | ✅ |')
    else:
        lines.append('| Challenge | Platform | Diff | Key Concept |')
        lines.append('|-----------|----------|------|-------------|')
        for c in challenges:
            diff_emoji = DIFF_EMOJI.get(c['difficulty'], '')
            lines.append(f'| [{c["title"]}]({c["path"]}/) | {c["platform"]} | {diff_emoji} {c["difficulty"]} | {c["key_concept"]} |')

    return '\n'.join(lines)


def generate_root_readme(categories: Dict[str, List[Dict]]) -> str:
    """Generate the root README with hacker theme."""
    total_solved = sum(len(c) for c in categories.values())
    cat_names = sorted(categories.keys())

    lines = [
        f'```',
        BANNER.strip(),
        '```',
        '',
        '## ▓▓▓▓▓▓▓▓▓▓ PROGRESS MATRIX ▓▓▓▓▓▓▓▓▓▓',
        '',
    ]

    # Progress bars for each category
    for cat in cat_names:
        count = len(categories[cat])
        emoji = CATEGORY_EMOJI.get(cat, '📁')
        bar = progress_bar(count)
        lines.append(f'{emoji} **{cat}** {bar}')

    lines.extend([
        '',
        f'**TOTAL: {total_solved} CHALLENGES SOLVED**',
        '',
        '## ▓▓▓▓▓▓▓▓▓▓ REPO TREE ▓▓▓▓▓▓▓▓▓▓',
        '',
        generate_tree(categories),
        '',
        '## ▓▓▓▓▓▓▓▓▓▓ CHALLENGES ▓▓▓▓▓▓▓▓▓▓',
        '',
    ])

    # Challenge tables per category
    for cat in cat_names:
        lines.append(generate_category_table(cat, categories[cat], show_flag=False))
        lines.append('')

    lines.extend([
        '---',
        '',
        f'*Last updated: {datetime.now().strftime("%Y-%m-%d")} • Auto-generated on push*',
        ''
    ])

    return '\n'.join(lines)


def generate_category_readme(category: str, challenges: List[Dict]) -> str:
    """Generate a category README (Forensics, OSINT, etc.)."""
    emoji = CATEGORY_EMOJI.get(category, '📁')
    intro = CATEGORY_INTROS.get(category, f'{category} challenges.')

    lines = [
        f'# {emoji} {category}',
        '',
        intro,
        '',
        '---',
        '',
        '## 📋 Challenges',
        '',
        generate_category_table(category, challenges, show_flag=True),
        '',
    ]

    return '\n'.join(lines)


def write_if_changed(path: Path, content: str) -> bool:
    """Write file only if content changed. Return True if written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    old_content = path.read_text(encoding='utf-8') if path.exists() else ''
    if old_content.strip() != content.strip():
        path.write_text(content, encoding='utf-8')
        print(f'Updated: {path}')
        return True
    return False


def main():
    print('Scanning challenges...')
    categories = scan_challenges()

    if not categories:
        print('No challenges found!')
        return 1

    print(f'Found categories: {", ".join(categories.keys())}')

    any_changed = False

    # Root README
    root_readme = REPO_ROOT / 'README.md'
    root_content = generate_root_readme(categories)
    if write_if_changed(root_readme, root_content):
        any_changed = True

    # Category READMEs - map display name to actual folder
    FOLDER_MAP = {
        'Forensics': 'Forensics',
        'OSINT': 'osint',
        'Reverse Engineering': 'reverse-engineering',
        'Web': 'web',
        'General Skills': 'general-skills',
        'Crypto': 'crypto',
        'Pwn': 'pwn',
    }

    for cat_name, challenges in categories.items():
        folder_name = FOLDER_MAP.get(cat_name, cat_name.lower().replace(' ', '-'))
        cat_readme = REPO_ROOT / folder_name / 'README.md'
        cat_content = generate_category_readme(cat_name, challenges)
        if write_if_changed(cat_readme, cat_content):
            any_changed = True

    if any_changed:
        print('READMEs updated!')
        return 1
    else:
        print('No changes needed.')
        return 0


if __name__ == '__main__':
    sys.exit(main())