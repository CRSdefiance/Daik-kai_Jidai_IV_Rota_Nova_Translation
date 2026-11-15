"""Register the ready37-article successor without changing any accepted layer oreight-stage contract."""
from scripts import prepare_town_HELP23_release as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
 'dk4tool.patch.town_help23_release_v1':'dk4tool.patch.shipyard_help37_release_v1',
 'dk4tool/patch/town_help23_release_v1.py':'dk4tool/patch/shipyard_help37_release_v1.py',
 "ROOT=Path('work/analysis/Town_HELP23_release_20261104')":"ROOT=Path('work/analysis/Shipyard_HELP37_release_20261104')",
 'Shared_HELP_T21_T43_formatting_20261104':'Shared_HELP_T44_T80_formatting_20261104',
 'Early_HELP23_release_verified_20261104':'Town_HELP23_release_verified_20261104',
 "OLD='all-routes-early-help23-20261104'":"OLD='all-routes-town-help23-20261104'",
 "PROFILE='all-routes-town-help23-20261104'":"PROFILE='all-routes-shipyard-help37-20261104'",
 'translations/town_help23_editorial_release_v1.json':'translations/shipyard_help37_editorial_release_v1.json',
 '_town_HELP23_release_v1.json':'_shipyard_HELP37_release_v1.json',
 'b185a1992d60d6149650df2c59f486b6ce0bf5cae301df06054889883cdc9bc6':'013b1aa0698652ea044c609de66d661f2d3460d1478c6e2a91519bd354b588aa',
 'translations/help_town23_contextual_final_review_v2.json':'translations/help_shipyard37_contextual_final_review_v2.json',
 'preview_qualification_v2':'preview_qualification_v1',
 'refined_native_v2/native_help_pages.json':'native_pages_v1/native_help_pages.json',
 'dk4tool/dialogue/reviewed_help_pages_v3.py':'dk4tool/dialogue/reviewed_help_pages_v5.py',
 "Path('dk4tool/dialogue/help_source_links.py'),":
 "Path('dk4tool/patch/town_help23_release_v1.py'),Path('dk4tool/dialogue/reviewed_help_pages_v3.py'),Path('dk4tool/dialogue/reviewed_help_pages_v4.py'),Path('scripts/check_HELP_T44_T80_native_pages.py'),Path('scripts/bind_HELP51_native_refit_controls.py'),Path('dk4tool/dialogue/help_source_links.py'),",
 "len(doc['records'])==23":"len(doc['records'])==37",
 'record_count=23':'record_count=37',
 "len(proof['changed_records'])==23":"len(proof['changed_records'])==37",
 "id='town-help23'":"id='shipyard-help37'",
 'dk4-town-help23-release-v1':'dk4-shipyard-help37-release-v1',
 'Experimental cumulative town Help23:19 revisions/4 retentions;28 complete native/viewed pages,15 actual/13 offline-only,all five continuation cases/history returns checked. Preserve all earlier Help/Rafael work,114 accepted layers/all eight final stages. No main promotion;full scope active;no guide photos.':
 'Experimental cumulative shipyard-to-ruins Help37:27 revisions/10 retentions;38 fresh native/viewed pages,17 actual/21 offline-only,one continuation andseven returns checked. Refit51 A/X controls arebound. Preserve all earlier Help/Rafael work,114 accepted layers/all eight final stages. No main promotion;full scope active;no guide photos.',
 'release_stack.town_HELP23.pending.json':'release_stack.shipyard_HELP37.pending.json',
 'rom_retention_pins.town_HELP23.pending.json':'rom_retention_pins.shipyard_HELP37.pending.json',
 'Registered Help23 experimental successor':'Registered Help37 experimental successor',
})
exec(compile(source,__file__+'::same-full-prefix-accepted-layer-andall-eight-stage-preservation-for37-articles','exec'),globals())
