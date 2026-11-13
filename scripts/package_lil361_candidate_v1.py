"""Package the registered cumulative successor with an exact clean-input testing copy."""
import re
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

parent = Path('scripts/package_lil269_candidate_v1.py').read_text(encoding='utf-8')
start = parent.index("    text = f'''# Cumulative testing candidate")
end = parent.index("    (OUT / 'README.md')", start)
notes = """    text = f'''# Cumulative testing candidate — Lil361

Local ROM: `{rom}`, with its adjacent manifest. This registered successor preserves every727 predecessor entry and114 accepted layers, including Rafael/tutorial localization, prior storyline/shared work, the Market Trade-screen correction, names/glyph fixes and ASCII right bounds. Main stays V4701 pending your cold-boot testing and explicit acceptance. All earlier ROMs and translations remain preserved.

Apply `translation.xdelta` to clean Japanese ROM SHA-256 `{release['clean_input_sha256']}`. Expected output SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. Both clean-input reconstructions match the registered candidate byte for byte. The patch works independently of old work folders. Exact build-time manifest and registry are included losslessly as gzip files.

The new361 contextual reviews cover16 complete Lil SC2 groups B283–B298:178 revisions,183 individually justified retentions and15 scoped names. They review the forest bear, London wine delivery, cave encounter, Angkor riddle, foggy mountain route, cliff settlement and Heavenly Wristband exchanges from clean Japanese. Facts, uncertainty, humor, characterization, controls and substitutions remain source-bound. Three stale Constantinople references become Istanbul; no new relationship, rank or event outcome is invented. B294's previously credited R73 remains exact context and receives no duplicate credit.

Nine final layouts improve without changing the reviewed prose or353-page total. Seven phrase wraps and one cliff page boundary improve continuity; a real FE extra blank row is removed. Complete first/internal/final glyphs remain present, so this is a blank-row correction, not a truncation claim. The record-specific reserve uses the unchanged228px native width, font and runtime. Every353 body page, allnine captions and19 distinct name strings pass native and direct visual review.

Stored validation passes353 pages,875 native relative cases,352 complete-buffer lookups,336 SC2 loads/cache hits and672 parent handoffs. Whole clean/current/block/archive/serialized-NDS inverses pass; every other internal file/component matches the registered Lil269 parent. Five context-helper negatives and eight production-scope negatives pass.

Three initialized ordinary-input samples observe199 bodies/200 unique pages,24 current personality selections, allfour menus/nine captions, one page turn and15 FE returns. All18 body sheets andthree menu sheets are directly viewed and exactly bound to their original captures. The153 remaining personality alternatives are offline-only. A separate unchanged-ROM longer-tail sample repeats42 already-viewed pages exactly, then observes crew joining, resupply and the following steering tutorial. Its transition sheet is directly viewed. The original schedule stopped too early; extra ordinary A presses resolve the test timing without ROM changes. Total:four runs/86,324 frames,242 page occurrences,22 viewed sheets. Only the focused fourth run claims the complete host exit.

These samples concatenate conditional alternatives in a native B22 QA host. Original optional events, locations, chronology, branch outcomes, rewards/stats, full-route playthroughs, catalogue UI, future role assignments and hardware remain unvisited. Offline native return/cancellation checks remain distinct from observed menu display/A returns. No savestate, battery, RAM, roster, RNG or conditional-result override was used for the Lil samples. No guide photos are required.

The exact cumulative candidate separately passes its own31,000-frame Maria/Hangzhou cold boot, six directly viewed captures,24 protected name getters,63 registered release checks and27 fresh repository tests. The startup's existing isolated system unlock is disclosed and unearned.

Integrated:25,105 contextual reviews,14,882 revisions and10,223 retentions. Native Lil:5,927/6,720 positions reviewed,793 remaining. Maria remains5,129/5,129. The full unfinished contextual storyline/shared/shop/town/random/player-facing/name review stays active; deferred graphics artwork and the later older-record technical re-audit remain separate.

After cloning, run `git lfs pull` for the coverage ledger. Cold-boot this exact filename and test title/New Game, Rafael/tutorial, town/Market Trade, names, wraps, pagination and transitions. Report this build filename with any issue.
'''
"""
source = checked_text(parent, {
    parent[start:end]: notes,
    'lil269': 'lil361',
    'Lil269': 'Lil361',
    'B243_B282': 'B283_B298',
    'Packaged727-entry': 'Packaged728-entry',
})
counts = {'727': '728', '62': '63', '24744': '25105', '14704': '14882', '10040': '10223'}
pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(sorted(counts, key=len, reverse=True)) + r')(?![A-Za-z0-9_])')
source = pattern.sub(lambda m: counts[m[0]], source)

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-registration-clean-input-manifest-test-andretention-guards', 'exec'), globals())
