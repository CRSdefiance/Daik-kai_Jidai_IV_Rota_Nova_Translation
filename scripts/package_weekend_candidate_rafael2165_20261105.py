"""Package the Rafael2165 weekend build using the established release checks."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent = Path(__file__).with_name('package_weekend_candidate_rafael1607_20261105.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'Test_2026-11-05_Rafael1607': 'Test_2026-11-05_Rafael2165',
    'Weekend_testing_package_Rafael1607_20261105': 'Weekend_testing_package_Rafael2165_20261105',
    'Rafael1607_extended_release_verified_v1_20261105': 'Rafael2165_extended_release_verified_v1_20261105',
    "PREVIOUS_REFRESH=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael1424.zip')":
        "PREVIOUS_REFRESH=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael1424.zip')\n"
        "LAST_PACKAGE_REPORT=Path('work/analysis/Weekend_testing_package_Rafael1860_20261105/package_verification.json')\n"
        "CREDIT=RELEASE.with_name('completion_checkpoint.json')",
    'base,clean,PREVIOUS_ZIP,PREVIOUS_REFRESH]':
        "base,clean,PREVIOUS_ZIP,PREVIOUS_REFRESH,LAST_PACKAGE_REPORT,Path(load(LAST_PACKAGE_REPORT)['zip']),CREDIT]",
    "    assert original[candidate]==release['candidate_sha256']=='bffc7d64a1acd3ac28344faec6e43063b6f258885e559366fe99ea74583f1d58'":
        "    previous=load(LAST_PACKAGE_REPORT)\n"
        "    assert original[Path(previous['zip'])]==previous['zip_sha256']\n"
        "    assert previous['ROM_sha256']=='b68173a552cd2ce69a062766976d7befedb652527728bd558a5c7725fe076473'\n"
        "    credit=load(CREDIT)\n"
        "    assert credit['new_credit']==190 and credit['counts']==dict(completed=14010,revised=8090,retained=5920)\n"
        "    assert original[candidate]==release['candidate_sha256']\n"
        "    assert release['parent_sha256']=='79d2ae069f8206f482207d4f3b5aa1a6f9619af4c530c8372295ae691f472f3f'\n"
        "    assert release['only_owned_SC0_blocks_changed']==list(range(170,177))",
    "release['complete_stack_entries']==683": "release['complete_stack_entries']==687",
    'integrated_editorial_records=13452,newly_included_B177_B180_reviews=183,\n        pending_B161_B176_revisions_included=False,':
        'integrated_editorial_records=14010,newly_included_B168_B176_reviews=305,\n'
        '        newly_included_revisions=242,newly_included_justified_retentions=63,\n'
        '        pending_B181_B200_revisions_included=False,',
    'This is an experimental combined build with all four story routes. It includes 13,452 integrated editorial reviews. The previous weekend ZIP and the designated main build are preserved.':
        'This experimental combined build contains all four story routes and 14,010 integrated editorial reviews.',
    'Since the Rafael1424 weekend ZIP, 183 more Rafael records passed review in B177–B180. The 133 revisions and 50 justified retentions cover ship inspection, refits, sailing instruction and nearby dialogue. The next B161–B176 editorial work is outside this package.':
        'Since the Rafael1860 weekend ZIP, 305 more Rafael records passed contextual review across B168–B176, with 242 revisions and 63 justified retentions. Highlights include Carlo’s account of his family, Cristina’s flamenco scene, and Jam’s missing-ship sequence. The editorial pass for B181–B200 is still underway.',
    '2. Check the ship inspection, refit and sailing lessons as you reach them. Watch for awkward breaks, clipped glyphs and whether A advances pages or returns from a choice as expected.':
        '2. Check the ship inspection, refit and sailing lessons as you reach them. Watch for awkward breaks, clipped glyphs and whether A advances pages or returns from a choice as expected. In the flamenco scene, check that the audience headings and reactions read clearly.',
    '683-entry build stack': '687-entry build stack',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::registered-weekend-package', 'exec'), globals())
