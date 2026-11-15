"""Correct only the handoff's displayed patch pathname; binaries andcounts exact."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_handoff_correction_v2016b')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    before=HANDOFF.read_bytes();(ROOT/'handoff_before.md').write_bytes(before)
    text=before.decode('utf-8')
    old='Exactclean-input patch:out\\all_routes_combined_v1986_candidate.xdelta;SHA25626fdb688b8d7a7063190e5054a68f821d07c6ea933ec59182d1fe98fb4f5b1fb'
    new=old.replace('v1986','v2013')
    assert text.count(old)==1
    assert sha(Path('out/all_routes_combined_v2013_candidate.xdelta').read_bytes())=='26fdb688b8d7a7063190e5054a68f821d07c6ea933ec59182d1fe98fb4f5b1fb'
    text=text.replace(old,new,1).replace('# Current editorial handoff - V2016','# Current editorial handoff - V2016b',1)
    HANDOFF.write_text(text,encoding='utf-8')
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['current_integrated_candidate']['patch'].replace('\\','/')=='out/all_routes_combined_v2013_candidate.xdelta'
    save(ROOT/'documentation_reference_correction.json',dict(reason='V2016 current patch display retained the earlier filename while the new hash,ledger andrelease proof already namedV2013 correctly.',
        handoff_before_sha256=sha(before),handoff_after_sha256=sha(HANDOFF.read_bytes()),
        ledger_unchanged_sha256=sha(Path('translations/editorial_review_current_v1.json').read_bytes()),
        all_ROM_patch_registry_coverage_and_final_review_bytes_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V2016b current handoff patch path matches the verified V2013 patch and ledger; all binaries/counts unchanged.')
