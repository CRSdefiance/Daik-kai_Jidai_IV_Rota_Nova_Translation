"""Register the research-complete town23 batch;reuse unchanged eight-stage preparation guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_early_HELP23_release.py').read_text(encoding='utf-8'),{
    'dk4tool.patch.early_help23_release_v1':'dk4tool.patch.town_help23_release_v1',
    'dk4tool/patch/early_help23_release_v1.py':'dk4tool/patch/town_help23_release_v1.py',
    "ROOT=Path('work/analysis/Early_HELP23_release_20261104')":"ROOT=Path('work/analysis/Town_HELP23_release_20261104')",
    'Shared_HELP_early23_formatting_20261104':'Shared_HELP_T21_T43_formatting_20261104',
    'Rafael_B61_B80_release_verified_20261104':'Early_HELP23_release_verified_20261104',
    "OLD='all-routes-rafael-b61-b80-20261104'":"OLD='all-routes-early-help23-20261104'",
    "PROFILE='all-routes-early-help23-20261104'":"PROFILE='all-routes-town-help23-20261104'",
    'translations/early_help23_editorial_release_v1.json':'translations/town_help23_editorial_release_v1.json',
    '_early_HELP23_release_v1.json':'_town_HELP23_release_v1.json',
    'e0447b467e8b6fe9f428edf2aa2c6b9f3b6b6202abe7133aaa913aab140d74fe':'b185a1992d60d6149650df2c59f486b6ce0bf5cae301df06054889883cdc9bc6',
    'translations/help_early23_contextual_final_review_v1.json':'translations/help_town23_contextual_final_review_v2.json',
    'production_plan_v1.json':'production_plan_v2.json',
    'preview_qualification_v1':'preview_qualification_v2',
    'native_pages_v2/native_help_pages.json':'refined_native_v2/native_help_pages.json',
    'ordinary_navigation_checked_v2':'focused_navigation_checked_v1',
    'dk4tool/dialogue/reviewed_help_pages_v1.py':'dk4tool/dialogue/reviewed_help_pages_v3.py',
    "Path('dk4tool/dialogue/help_source_links.py'),":
        "Path('dk4tool/patch/early_help23_release_v1.py'),Path('dk4tool/dialogue/reviewed_help_pages_v1.py'),Path('dk4tool/dialogue/reviewed_help_pages_v2.py'),Path('scripts/check_refined_town_HELP23_native_pages.py'),Path('scripts/verify_reviewed_help_navigation_v1.py'),Path('dk4tool/dialogue/help_source_links.py'),",
    "id='early-help23'":"id='town-help23'",
    'dk4-early-help23-release-v1':'dk4-town-help23-release-v1',
    'Experimental cumulative early Help23:16 revisions/7 retentions;25 full native andordinary UI pages,original links andboth continuation/history returns checked. Preserve Rafael539/all114 accepted layers/all eight final stages. No main promotion;full scope active;no guide photos.':
        'Experimental cumulative town Help23:19 revisions/4 retentions;28 complete native/viewed pages,15 actual/13 offline-only,all five continuation cases/history returns checked. Preserve all earlier Help/Rafael work,114 accepted layers/all eight final stages. No main promotion;full scope active;no guide photos.',
    'release_stack.early_HELP23.pending.json':'release_stack.town_HELP23.pending.json',
    'rom_retention_pins.early_HELP23.pending.json':'rom_retention_pins.town_HELP23.pending.json',
})
exec(compile(source,__file__+'::same-complete-prefix-andstage-contract-preservation-town23','exec'),globals())
