"""Record direct view of own V8172 Hodram captain selection andopening snapshot."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_current_startup_view_v8189')
START=Path('work/analysis/Hodram_current_binding_v8187/own_Hodram_startup_andstrict_captain1_context.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(START)
    assert d['actual_frames']==4001 and d['actual_original_captain_ID']==1 and d['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert sha(Path(d['review_sheet']['path']).read_bytes())==d['review_sheet']['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'own_Hodram_startup_sheet_viewed.json',dict(candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],
        startup_proof=str(START),startup_proof_sha256=sha(START.read_bytes()),viewed=True,viewed_sheet=d['review_sheet'],
        findings='Captain selection shows Hodram/Joakim/Bergstrom andBergstromFleet fields;opening portrait/HodramBergstrom header andcomplete ordinary line visible. Exactcaptain1/currentpool binding independentlypasses.',
        no_optional_B137_B45_B46_activation_fullroute_orhardware_claim=True,no_new_prose_orcredit=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Own V8172 Hodram startup directlyviewed;captain1/nativecontext bound,zero extra editorial credit.')
