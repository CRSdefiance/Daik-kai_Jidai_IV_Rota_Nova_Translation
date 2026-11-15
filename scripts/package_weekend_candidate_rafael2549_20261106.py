"""Package the already registered Rafael2549 ROM for weekend testing."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent = Path(__file__).with_name('package_weekend_candidate_rafael1607_20261105.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'Test_2026-11-05_Rafael1607': 'Test_2026-11-06_Rafael2549',
    'Weekend_testing_package_Rafael1607_20261105': 'Weekend_testing_package_Rafael2549_20261106',
    'Rafael1607_extended_release_verified_v1_20261105': 'Rafael2549_extended_release_verified_v1_20261106',
    "PREVIOUS_REFRESH=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael1424.zip')":
        "PREVIOUS_REFRESH=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael2165.zip')\n"
        "PREVIOUS_REPORT=Path('work/analysis/Weekend_testing_package_Rafael2165_20261105/package_verification.json')\n"
        "CREDIT=RELEASE.with_name('completion_checkpoint.json')",
    'base,clean,PREVIOUS_ZIP,PREVIOUS_REFRESH]':
        "base,clean,PREVIOUS_ZIP,PREVIOUS_REFRESH,PREVIOUS_REPORT,CREDIT,Path(release['parent'])]",
    "    assert original[candidate]==release['candidate_sha256']=='bffc7d64a1acd3ac28344faec6e43063b6f258885e559366fe99ea74583f1d58'":
        "    previous=load(PREVIOUS_REPORT)\n"
        "    assert Path(previous['zip'])==PREVIOUS_REFRESH and original[PREVIOUS_REFRESH]==previous['zip_sha256']\n"
        "    assert original[Path(release['parent'])]==release['parent_sha256']==previous['ROM_sha256']\n"
        "    assert release['only_owned_SC0_blocks_changed']==list(range(181,201))\n"
        "    assert release['changed_internal_files']==['/data/SC0.DK4'] and not release['changed_components']\n"
        "    credit=load(CREDIT)\n"
        "    assert credit['new_credit']==384 and credit['counts']==dict(completed=14394,revised=8407,retained=5987)\n"
        "    assert original[candidate]==release['candidate_sha256']=='989e53a0438c3bf5f37161129787771dd7e47eebb36462b3551433f289ae9202'",
    "release['complete_stack_entries']==683": "release['complete_stack_entries']==688",
    'integrated_editorial_records=13452,newly_included_B177_B180_reviews=183,\n        pending_B161_B176_revisions_included=False,':
        'integrated_editorial_records=14394,newly_included_B181_B200_reviews=384,\n'
        '        newly_included_revisions=317,newly_included_justified_retentions=67,\n'
        '        pending_B201_B220_revisions_included=False,',
    'This is an experimental combined build with all four story routes. It includes 13,452 integrated editorial reviews. The previous weekend ZIP and the designated main build are preserved.':
        'This experimental combined build includes all four story routes, the shared tutorial updates and 14,394 integrated editorial reviews.',
    'Since the Rafael1424 weekend ZIP, 183 more Rafael records passed review in B177–B180. The 133 revisions and 50 justified retentions cover ship inspection, refits, sailing instruction and nearby dialogue. The next B161–B176 editorial work is outside this package.':
        'This ZIP adds 384 reviewed Rafael and town dialogue records since Rafael2165. The batch contains 317 revisions and 67 justified retentions, including fixes for early wraps, two full-width I glyphs and six wine conversations. The B201–B220 editorial work is still in progress and those scenes use the earlier text here.',
    '2. Check the ship inspection, refit and sailing lessons as you reach them. Watch for awkward breaks, clipped glyphs and whether A advances pages or returns from a choice as expected.':
        '2. Check the early ship, crew and sailing tutorials as you reach them. Watch for short first lines, split phrases, clipped letters and whether A advances pages or returns from a choice.',
    '3. Visit a town shop and try the Lisbon Guild. Look for premature wraps, awkward speaker labels, missing letters and blank or stuck pages. If you find something, note the route, location and exact line so it can be traced.':
        '3. Visit shops and taverns and try the Lisbon Guild. Look for premature wraps, awkward speaker labels, missing letters and blank or stuck pages. To report a finding, note the route, location and exact line.',
    '683-entry build stack': '688-entry build stack',
    'The targeted scene fixtures covered selected dialogue, pagination and menus.':
        'Focused B181–B200 emulator fixtures showed 148 dialogue pages. The other 236 speeches were checked offline.',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::registered-weekend-package', 'exec'), globals())

