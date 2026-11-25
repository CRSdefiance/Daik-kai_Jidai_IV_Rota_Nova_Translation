"""Qualify the observed wrap description without inventing a width-capacity explanation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_native_note_v8638')
OLD=Path('translations/hodram_B52_editorial_manuscript_v2.json')
DOC=Path('translations/hodram_B52_editorial_manuscript_v3.json')
REVIEW=Path('work/analysis/Hodram_B52_native_review_v8637/native_body_andchoice_review.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old=read(OLD);prior=read(REVIEW)
    assert prior['manuscript_sha256']==sha(OLD.read_bytes())
    new=deepcopy(old);row=new['records'][0];before=row['native_body_review_reason']
    assert row['id']=='DK4_MES_B52_R0006' and row['generated_lines']==['Are you planning to make an enemy',"of Hayreddin's outfit?"]
    reason='Two automatically generated rows use the original full216px native width. The observed complete-word boundary after enemy leaves the following of phrase together on the second row; the full question reads naturally across that ordinary boundary. All words, the apostrophe and final question mark are complete. This review records the actual planner output and does not claim that adding of alone would exceed the raw first-row cell count. No shortened prose, authored break, padding or viewport narrowing is used.'
    row['native_body_review_reason']=reason
    new.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),wrap_note_qualification=dict(prior_native_review=str(REVIEW),prior_native_review_sha256=sha(REVIEW.read_bytes()),reason='Replace an unnecessary implied capacity explanation with the observed native wrap and its readability; no compiler or prose changes.'))
    inverse=deepcopy(new);inverse['records'][0]['native_body_review_reason']=before
    for key in ['predecessor_manuscript','predecessor_manuscript_sha256']:inverse[key]=old[key]
    inverse.pop('wrap_note_qualification');assert inverse==old
    assert all(new[k]==old[k] for k in ['typed_choice_records','revised','retained','native_body_pages_sha256','native_choice_proof_sha256','compiled_plan_sha256','all_five_formatting_gates_still_false'])
    save(DOC,new);ROOT.mkdir(parents=True)
    save(ROOT/'qualified_native_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),prior_native_review=str(REVIEW),prior_native_review_sha256=sha(REVIEW.read_bytes()),before_note=before,qualified_note=reason,all_words_compiled_bytes_source_current_refs_individual_review_gates_native_planes_choice_geometry_andactual_scope_unchanged=True,exact_complete_prior_manuscript_inverse=True,original_producer_andboth_earlier_manuscripts_preserved=True,all_five_formatting_gates_still_false=True,no_new_native_probe_emulator_ROM_orcompletion_credit=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Qualified B52 first-wrap note: observed complete-word boundary/readability, no unsupported capacity claim. Manuscriptv3 preserves every word, byte, reference, gate and native result; originalv2/review preserved.')
