"""Package the exact Lil254 candidate and clean-input patch."""

import re

from scripts.package_lil278_candidate_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


start = previous.index("    text = f'''# Cumulative testing candidate")
end = previous.index("    (OUT / 'README.md')", start)
notes = """    text = f'''# Cumulative testing candidate — Lil254

Use the local ROM `{rom}` and its adjacent manifest. This candidate retains all 729 predecessor entries and 114 accepted layers, including Rafael's tutorials, the Market Trade-screen fix and the ASCII right-bound correction. Main V4701 awaits user cold-boot acceptance.

Apply `translation.xdelta` to the clean Japanese ROM with SHA-256 `{release['clean_input_sha256']}`. Expected ROM SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`. Both clean-input reconstructions match the registered image byte for byte. The compressed manifest and registry preserve their exact build-time bytes.

The eight Lil B312–B319 exchanges add 254 reviews, including 151 revisions, 103 justified retentions and ten scoped name reviews. The revised injury alert displays two contiguous rows, and Lil's company substitution supplies its own period. All 251 dialogue pages, eight captions and 13 name strings passed offline checks and visual review.

The initialized Lil emulator sample displayed 53 bodies, 58 pages and all eight captions. It exercised five page turns, seven system-alert returns and all three menu returns, then reached resupply and the steering tutorial. Both original selector-00 replies displayed Rafael Castor. The other 193 dialogue bodies have offline and stored coverage. Original optional activation and outcomes, a full route and physical hardware remain unvisited.

The exact cumulative candidate separately passed its own 31,000-frame Maria/Hangzhou cold boot with the isolated system unlock, 24 protected name getters, 65 registered release checks and 27 repository tests. The ledger credits 25,637 reviews. Lil's native census has 261 positions remaining, and the wider editorial review remains active.

After cloning, run `git lfs pull` for the coverage ledger. Use the candidate filename when reporting test results.
'''
"""
source = checked_text(previous, {
    previous[start:end]: notes,
    'lil278': 'lil254',
    'Lil278': 'Lil254',
    'B299_B311': 'B312_B319',
    'Packaged 729-entry': 'Packaged 730-entry',
})
counts = {'729': '730', '64': '65', '25383': '25637', '15052': '15203', '10331': '10434'}
start = source.index("    text = f'''# Cumulative testing candidate")
end = source.index("    (OUT / 'README.md')", start)
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')


def replace_counts(text):
    return pattern.sub(lambda match: counts[match[0]], text)


source = replace_counts(source[:start]) + source[start:end] + replace_counts(source[end:])

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
