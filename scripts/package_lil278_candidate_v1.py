"""Package the registered Lil278 clean-input patch and exact testing ROM."""

import re
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent = Path('scripts/package_lil269_candidate_v1.py').read_text(encoding='utf-8')
start = parent.index("    text = f'''# Cumulative testing candidate")
end = parent.index("    (OUT / 'README.md')", start)
notes = """    text = f'''# Cumulative testing candidate — Lil278

The local ROM is `{rom}`, with its adjacent manifest. Main V4701 remains the promoted build pending cold-boot acceptance. This candidate preserves the 728-entry predecessor and all 114 accepted layers, including Rafael's tutorial revisions, the Market Trade-screen fix and the ASCII right-bound correction.

Apply `translation.xdelta` to the clean Japanese ROM with SHA-256 `{release['clean_input_sha256']}`. The expected output SHA-256 is `{release['candidate_sha256']}`. The patch SHA-256 is `{release['patch_sha256']}`. Both reconstructions match the registered image byte for byte. The gzip files preserve the exact build-time manifest and registry.

Lil B299–B311 adds 278 contextual reviews across 13 complete groups, including 170 revisions, 108 justified retentions and ten scoped name reviews. The changes restore Japanese dialogue in the temple errands, preserve the Basra delivery terms and uncertainty about injuries and the bridge, and improve 25 wraps and page boundaries without shortening the reviewed prose. All 280 pages, six captions and 11 name strings passed offline native and visual checks.

Stored verification covered 272 complete-buffer lookups, 670 relocated branch cases, 336 SC2 loads and cache hits, and 672 parent handoffs. The 25,121-frame Lil B22 emulator sample displayed 52 bodies, 55 pages and all six captions. It exercised three page turns, eight system alert returns and all three menu returns, then reached resupply and the steering tutorial. The remaining 220 bodies have offline-only coverage. The fixture combines selected native commands from conditional alternatives. Original optional activation, branch outcomes, rewards, full-route play and hardware remain unvisited.

The exact cumulative candidate passed its own 31,000-frame Maria/Hangzhou cold boot, six directly viewed startup captures, 24 protected name getters, 64 release checks and 27 repository tests. The isolated system unlock used for this startup test is unearned.

The ledger now credits 25,383 contextual reviews, including 15,052 revisions and 10,331 retentions. The Lil census covers 6,205 of 6,720 native positions, leaving 515. The wider editorial and name review remains active. Deferred artwork and the older-record technical re-audit are separate.

After cloning, run `git lfs pull` for the coverage ledger. Use the exact candidate filename when reporting testing results.
'''
"""
source = checked_text(parent, {
    parent[start:end]: notes,
    'lil269': 'lil278',
    'Lil269': 'Lil278',
    'B243_B282': 'B299_B311',
    'final_layout_delta_v2.json': 'final_layout_delta_v1.json',
    'Packaged727-entry': 'Packaged 729-entry',
})
counts = {'727': '729', '62': '64', '24744': '25383', '14704': '15052', '10040': '10331'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda match: counts[match[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
