"""Reuse exact B228 name-font inputs/planes; bind the new B229 getters and unchanged font/runtime."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B229_name_planes_v7386');PRIOR=Path('work/analysis/lil_B228_name_planes_v7339/two_actors_four_getters_eight_literal_planes32_alignments.json');CURRENT=Path('work/analysis/lil_B229_consumers_v7382/seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers.json')
if __name__=='__main__':
    assert not ROOT.exists();old,new=map(read,[PRIOR,CURRENT]);prior,current=[NdsImage.open(p) for p in [old['candidate'],new['candidate']]];previous=read(old['consumer_proof']);assert sha(Path(old['candidate']).read_bytes())==old['candidate_sha256'] and sha(Path(new['candidate']).read_bytes())==new['candidate_sha256']
    assert sha(Path(old['consumer_proof']).read_bytes())==old['consumer_proof_sha256'] and previous['source_name_fields']==new['source_name_fields']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert prior.read_file(path)==current.read_file(path)
    forms=lambda p:{(r['actor_ID'],r['consumer']):(r['text'],r['text_hex']) for r in p['native_four_distinct_name_consumers']['rows']};assert forms(previous)==forms(new) and len(forms(new))==4
    assert old['name_literal_alignment_count']==32 and old['complete_name_component_plane_count']==8
    for row in old['name_planes']:assert sha(Path(row['native_plane']).read_bytes())==row['native_plane_sha256']
    sheet=Path(old['review_sheet']);assert sha(sheet.read_bytes())==old['review_sheet_sha256']
    out=deepcopy(old);out.update(candidate=new['candidate'],candidate_sha256=new['candidate_sha256'],consumer_proof=str(CURRENT),consumer_proof_sha256=sha(CURRENT.read_bytes()),previous_complete_name_font_proof=str(PRIOR),previous_complete_name_font_proof_sha256=sha(PRIOR.read_bytes()),proof_mode='exact-native-code-font-source-fields-andgetter-byte-inputs-reused',fresh_native_name_font_alignment_cases=0,exact_reused_native_name_font_alignment_cases=32,all_current_B229_name_getters_freshly_bound_in_separate_consumer_proof=True,Samwell_mixed_Japanese_catalogue_plane_is_technical_evidence_not_wording_approval=True,original_prior_name_font_context_retained_as_reused_history_not_new_native_execution=True,visual_review_pending=True,new_emulator_runs=0,new_review_credit=0)
    out['evidence']={**out['evidence'],str(PRIOR):sha(PRIOR.read_bytes()),str(CURRENT):sha(CURRENT.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())};ROOT.mkdir(parents=True);save(ROOT/'two_actors_four_getters_eight_literal_planes32_alignments.json',out);print('B229 name-font proof:32 exact alignments reused by identical runtime/font/field/getter bytes;eight literal/name planes preserved. New scene headers remain pending;catalogue wording unapproved.')
