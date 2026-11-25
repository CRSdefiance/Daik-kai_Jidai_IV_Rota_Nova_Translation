"""Keep the read-only modal checks without redundant per-page full RAM files."""
from scripts.run_reviewed_dialogue_fixture_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

# No renderer, input, CPU filter, memory read/hash, nonmutation assertion, capture
# or original observer cleanup changes. Compatible native proofs already own the
# complete consumer snapshots. This run needs ordered calls and actual pixels.
source = checked_text(previous, {
    "        \"if target['name']=='modal_paint' and frame>=3000:\",":
        "        \"if False:  # Existing native proof reused; no redundant full RAM files.\",",
    'source_content_fixture_not_natural_story_activation=True,':
        'source_content_fixture_not_natural_story_activation=True, per_page_full_RAM_files_omitted=True, all_boundary_reads_hashes_andnonmutation_assertions_preserved=True,',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-readonly-boundaries-without-redundant-snapshot-files', 'exec'), globals())
