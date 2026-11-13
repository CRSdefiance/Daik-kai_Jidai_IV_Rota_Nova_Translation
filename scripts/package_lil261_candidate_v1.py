"""Package the registered Lil261 candidate and exact clean-input patch."""

import re

from scripts.package_lil254_candidate_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


start = previous.index("    text = f'''# Cumulative testing candidate")
end = previous.index("    (OUT / 'README.md')", start)
source = checked_text(previous[:start] + previous[end:], {
    'lil254': 'lil261',
    'Lil254': 'Lil261',
    'B312_B319': 'B323_B335',
    'lil254_repository_qa_v1_pytest.xml': 'lil261_repository_qa_v1_pytest_retry.xml',
})
counts = {'730': '731', '65': '66', '25637': '25898', '15203': '15401', '10434': '10497'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(counts) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda match: counts[match[0]], source)
start = source.index("    (OUT / 'README.md')")
source = source[:start] + "    text = f'''# Cumulative testing candidate — Lil261\n\nUse the local ROM `{rom}` and its adjacent manifest. This candidate retains all 730 predecessor entries and 114 accepted layers, including Rafael's tutorials, the Market Trade-screen fix and the ASCII right-bound correction. Main V4701 awaits user cold-boot acceptance.\n\nApply `translation.xdelta` to the clean Japanese ROM with SHA-256 `{release['clean_input_sha256']}`. Expected ROM SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`. The clean-input reconstructions match the registered image byte for byte.\n\nThe 13 Lil exchanges add 261 reviews, including 198 revisions, 63 justified retentions and nine scoped name reviews. Thirty layouts improve phrase continuity and pagination. Offline checks cover all 258 dialogue pages, six menu captions and 12 name strings. The exact native Lil story census covers all 6,720 dialogue, choice and personality positions. The wider editorial review remains active.\n\nThe initialized Lil emulator sample displayed 58 bodies and 61 pages. It exercised three page turns, 13 system-alert returns, all three menu returns and the transition into the next tutorial. The other 197 bodies have offline and stored coverage. Original optional activation, branch outcomes, full-route play and physical hardware remain unvisited.\n\nThe exact cumulative candidate passed its own 31,000-frame Maria/Hangzhou cold boot with the isolated system unlock, 24 protected name getters, 66 registered release checks and 27 repository tests.\n\nAfter cloning, run `git lfs pull` for the coverage ledger. Use the candidate filename when reporting test results.\n'''\n" + source[start:]

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
