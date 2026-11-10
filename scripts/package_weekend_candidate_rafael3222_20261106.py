"""Package the registered four-route Rafael3222 checkpoint on the C drive."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent = Path(__file__).with_name('package_weekend_candidate_rafael1607_20261105.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'out/Translation_DS_Weekend_Test_2026-11-05_Rafael1607':
        'work/Translation_DS_Weekend_Test_2026-11-06_Rafael3222',
    'work/analysis/Weekend_testing_package_Rafael1607_20261105':
        'work/Weekend_testing_package_Rafael3222_20261106',
    'work/analysis/Rafael1607_extended_release_verified_v1_20261105':
        'work/Rafael3222_extended_release_verified_v1_20261106',
    "PREVIOUS_ZIP=Path('out/Translation_DS_Weekend_Test_2026-11-05.zip')":
        "PREVIOUS_ZIP=Path('out/Translation_DS_Weekend_Test_2026-11-06_Rafael2549.zip')",
    "PREVIOUS_REFRESH=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael1424.zip')":
        "PREVIOUS_REPORT=Path('work/analysis/Weekend_testing_package_Rafael2549_20261106/package_verification.json')\n"
        "PREDECESSOR=Path('work/analysis/Rafael2952_extended_release_verified_v1_20261106/registered_release_verification.json')\n"
        "CREDIT=RELEASE.with_name('completion_checkpoint.json')",
    'base,clean,PREVIOUS_ZIP,PREVIOUS_REFRESH]':
        "base,clean,PREVIOUS_ZIP,PREVIOUS_REPORT,PREDECESSOR,CREDIT,Path(release['parent'])]",
    "    assert original[candidate]==release['candidate_sha256']=='bffc7d64a1acd3ac28344faec6e43063b6f258885e559366fe99ea74583f1d58'":
        "    previous=load(PREVIOUS_REPORT);predecessor=load(PREDECESSOR);credit=load(CREDIT)\n"
        "    assert Path(previous['zip'])==PREVIOUS_ZIP and original[PREVIOUS_ZIP]==previous['zip_sha256']\n"
        "    assert predecessor['parent_sha256']==previous['ROM_sha256']\n"
        "    assert original[Path(release['parent'])]==predecessor['candidate_sha256']==release['parent_sha256']\n"
        "    assert (predecessor['new_contextual_records'],release['new_contextual_records'],credit['new_credit'])==(403,270,270)\n"
        "    assert credit['counts']==dict(completed=15067,revised=8927,retained=6140)\n"
        "    assert release['changed_internal_files']==['/data/SC0.DK4'] and not release['changed_components']\n"
        "    assert original[candidate]==release['candidate_sha256']=='03b5462088911f0dca04bb652ccb98e700fcfbf17a34fc95a1d8029251aba39f'",
    'release[\'complete_stack_entries\']==683': 'release[\'complete_stack_entries\']==690',
    '683-entry build stack': '690-entry build stack',
    'integrated_editorial_records=13452,newly_included_B177_B180_reviews=183,\n        pending_B161_B176_revisions_included=False,':
        'integrated_editorial_records=15067,additional_reviews_since_Rafael2549=673,\n'
        '        additional_revisions=520,additional_justified_retentions=153,pending_B241_B260_revisions_included=False,',
    'This is an experimental combined build with all four story routes. It includes 13,452 integrated editorial reviews. The previous weekend ZIP and the designated main build are preserved.':
        'This experimental combined build includes all four story routes, the shared tutorial updates, and 15,067 integrated editorial reviews.',
    'Since the Rafael1424 weekend ZIP, 183 more Rafael records passed review in B177–B180. The 133 revisions and 50 justified retentions cover ship inspection, refits, sailing instruction and nearby dialogue. The next B161–B176 editorial work is outside this package.':
        'This ZIP adds 673 reviewed records across Rafael B201–B240 since Rafael2549, with 520 revisions and 153 justified retentions. '
        'The changes include town dialogue, letters, story choices, line wraps and mixed-width glyphs. Rafael B241–B260 still uses the previously integrated text.',
    '2. Check the ship inspection, refit and sailing lessons as you reach them. Watch for awkward breaks, clipped glyphs and whether A advances pages or returns from a choice as expected.':
        '2. Try the early ship, crew, trading and sailing tutorials. Check for premature wraps and whether A advances pages or returns from choices normally.',
    '3. Visit a town shop and try the Lisbon Guild. Look for premature wraps, awkward speaker labels, missing letters and blank or stuck pages. If you find something, note the route, location and exact line so it can be traced.':
        '3. Visit shops, taverns and the Lisbon Guild. Watch for odd speaker labels, clipped letters and blank or stuck pages. For any issue, note the route, location and exact line.',
    'The targeted scene fixtures covered selected dialogue, pagination and menus. Physical hardware testing and a full playthrough remain open.':
        'Initialized emulator fixtures for the newly included batches displayed 268 pages across selected scenes, with further coverage from offline checks. Physical hardware, natural activation of unvisited branches, and full playthroughs remain open.',
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::registered-weekend-package', 'exec'), globals())
