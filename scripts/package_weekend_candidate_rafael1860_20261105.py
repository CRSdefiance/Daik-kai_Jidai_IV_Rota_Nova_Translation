"""Verify and package the registered Rafael1860 candidate for weekend testing."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


PARENT = Path(__file__).with_name('package_weekend_candidate_rafael1607_20261105.py')
source = checked_text(PARENT.read_text(encoding='utf-8'), {
    'Test_2026-11-05_Rafael1607': 'Test_2026-11-05_Rafael1860',
    'Weekend_testing_package_Rafael1607_20261105': 'Weekend_testing_package_Rafael1860_20261105',
    'Rafael1607_extended_release_verified_v1_20261105': 'Rafael1860_extended_release_verified_v1_20261105',
    "PREVIOUS_REFRESH=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael1424.zip')":
        "PREVIOUS_REFRESH=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael1424.zip')\n"
        "LAST_PACKAGE=Path('out/Translation_DS_Weekend_Test_2026-11-05_Rafael1607.zip')\n"
        "LAST_PACKAGE_REPORT=Path('work/analysis/Weekend_testing_package_Rafael1607_20261105/package_verification.json')\n"
        "CREDIT=RELEASE.with_name('completion_checkpoint.json')",
    'base,clean,PREVIOUS_ZIP,PREVIOUS_REFRESH]':
        'base,clean,PREVIOUS_ZIP,PREVIOUS_REFRESH,LAST_PACKAGE,LAST_PACKAGE_REPORT,CREDIT]',
    "    assert original[candidate]==release['candidate_sha256']":
        "    prior_package=load(LAST_PACKAGE_REPORT)\n"
        "    assert original[LAST_PACKAGE]==prior_package['zip_sha256']\n"
        "    credit=load(CREDIT)\n"
        "    assert credit['new_credit']==186 and credit['counts']==dict(completed=13705,revised=7848,retained=5857)\n"
        "    assert original[candidate]==release['candidate_sha256']",
    'bffc7d64a1acd3ac28344faec6e43063b6f258885e559366fe99ea74583f1d58':
        'b68173a552cd2ce69a062766976d7befedb652527728bd558a5c7725fe076473',
    "release['complete_stack_entries']==683": "release['complete_stack_entries']==685",
    'integrated_editorial_records=13452,newly_included_B177_B180_reviews=183,\n        pending_B161_B176_revisions_included=False,':
        'integrated_editorial_records=13705,newly_included_B161_B167_reviews=253,\n        newly_included_revisions=197,newly_included_justified_retentions=56,\n        pending_B168_B176_revisions_included=False,',
    'This is an experimental combined build with all four story routes. It includes 13,452 integrated editorial reviews. The previous weekend ZIP and the designated main build are preserved.':
        'This experimental combined build contains all four story routes and 13,705 integrated editorial reviews.',
    'Since the Rafael1424 weekend ZIP, 183 more Rafael records passed review in B177–B180. The 133 revisions and 50 justified retentions cover ship inspection, refits, sailing instruction and nearby dialogue. The next B161–B176 editorial work is outside this package.':
        'Since the Rafael1607 weekend ZIP, 253 more Rafael records passed review in B161–B167. This includes 197 revisions and 56 justified retentions across sailing instruction, recruitment, the royal audience and letter sequences. B168–B176 editorial work is still in progress.',
    '    readme=f': '    readme=f',
    '2. Check the ship inspection, refit and sailing lessons as you reach them. Watch for awkward breaks, clipped glyphs and whether A advances pages or returns from a choice as expected.':
        '2. Check the ship inspection, refit and sailing lessons as you reach them. Watch for awkward breaks, clipped glyphs and whether A advances pages or returns from a choice as expected. Later, check the royal audience and letter for readable page turns and speaker labels.',
    '683-entry build stack': '685-entry build stack',
    '26 release checks. Packaging': '26 release checks. Packaging',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::registered-weekend-package', 'exec'), globals())