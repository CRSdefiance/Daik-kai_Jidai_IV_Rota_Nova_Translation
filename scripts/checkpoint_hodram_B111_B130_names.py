"""Advance the compact handoff after name ownership and native display checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B111_B130_editorial_20261101')
LEDGER=Path('translations/editorial_review_current_v1.json')
PROPOSAL=Path('work/analysis/Hodram_B111_B130_name_fields_20261101/owned_fields_proposal.json')
NATIVE=Path('work/analysis/Hodram_B111_B130_name_native_20261101/native_name_fields_verification_reviewed.json')
NAMES=Path('translations/hodram_B111_B130_speaker_name_review_v1.json')

def main():
    out=ROOT/'offline_checkpoint_v2.json';assert not out.exists()
    before_path=ROOT/'offline_checkpoint.json';prior=load(before_path);proof=load(NATIVE);names=load(NAMES)
    assert proof['offline_visual_approved'] and not proof['direct_view_pending']
    assert proof['proposal_sha256']==sha(PROPOSAL.read_bytes())
    assert len(names['records'])==18 and names['revised_name_identities']==2 and names['retained_name_identities']==16
    plan=proof['name_data_plan'];assert plan['complete_parent_inverse_exact'] and plan['owned_span_bytes']==11
    assert plan['target_ARM9_sha256']=='34884dc19ac4b2633172df84ac40dd7efa024c0a6c1076212c1f424328052737'
    registry=Path('translations/release_stack.json');assert sha(registry.read_bytes())=='b73049bf6391478aba731672b187cead93865cc59f232758d98f6b1733336e5b'
    registered=load(registry);profile=registered['profiles']['all-routes-hodram-b91-b110-names-20261101']
    assert profile['ascii_glyph_right_bounds'] and profile['owned_name_glyph'] and profile['owned_name_fields']
    checkpoint=deepcopy(prior)
    checkpoint.update(previous_checkpoint=str(before_path),previous_checkpoint_sha256=sha(before_path.read_bytes()),
        scoped_name_review=str(NAMES),scoped_name_review_sha256=sha(NAMES.read_bytes()),name_identities=18,name_identity_revisions=2,name_identity_retentions=16,
        owned_name_field_proposal=str(PROPOSAL),owned_name_field_proposal_sha256=sha(PROPOSAL.read_bytes()),
        native_name_proof=str(NATIVE),native_name_proof_sha256=sha(NATIVE.read_bytes()),
        checked_name_fields=2,owned_name_span_bytes=11,native_name_getters=8,directly_viewed_native_name_planes=10,
        proposed_name_ARM9_sha256=plan['target_ARM9_sha256'],name_ownership_andnative_offline_findings_resolved=True,
        previous_name_runtime_layers_andall_unowned_ARM9_bytes_preserved=True,
        pending=['Relocated complete 4100/2200/ordinary objects, original commands/relative branches, stored native planes and archive loaders.',
            'Compose the checked name proposal with the reviewed story research image, retaining all earlier name/runtime fixes.',
            'Representative new-English gameplay for styles, three-choice menus, actor0, FE rows, corrected names, pagination and transitions; full-catalogue UI remains unvisited.',
            'Registered cumulative release, exact clean-input patch, own startup and once-only completion credit.'],
        current_registry_sha256=sha(registry.read_bytes()),all_prior_completed_scope_andlater_audit_preserved=True)
    save(out,checkpoint)
    before=LEDGER.read_bytes();ledger=load(LEDGER);backup=ROOT/'ledger_before_name_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    assert ledger['records_editorially_completed']==8204 and not ledger['full_goal_complete']
    ledger['Hodram_B111_B130_prose_native_research_20261101']=checkpoint
    ledger['Hodram_B111_B130_clean_next_20261101'].update(offline_checkpoint=str(out),offline_checkpoint_sha256=sha(out.read_bytes()),name_ownership_andnative_offline_findings_resolved=True,new_credit=0)
    ledger['latest_checkpoint']='B111-B130:323 contextual decisions (239 revisions/84 retentions),315 viewed native pages,48 physical personality alternatives and15 three-choice captions checked offline. Seven page endings,two FE blank rows andtwo phrases fixed without prose shortening.18 scoped name decisions;Follower F/Diogo de exclusive11-byte proposals pass8 getters/10 viewed planes. Source-only2 fixtures/16502frames observed. Stored/new-English gameplay/release pending;8204/current e713/main unchanged. Full goal active;no guide photos.'
    old=load(backup);allowed={'Hodram_B111_B130_prose_native_research_20261101','Hodram_B111_B130_clean_next_20261101','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in old.items() if k not in allowed}
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    save(ROOT/'checkpoint_consistency.json',dict(checkpoint=str(out),checkpoint_sha256=sha(out.read_bytes()),ledger=str(LEDGER),ledger_sha256=sha(LEDGER.read_bytes()),
        registry_sha256=sha(registry.read_bytes()),completed=8204,source_prose_anddrafts=8207,revisions_integrated=5121,retentions_completed=3083,
        only_three_current_progress_keys_updated=True,all_completed_scope_keys_andnative_relocation_reference_exact=True,current_registered_ROM_andcanonical_main_unchanged=True,
        full_goal_complete=False,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [PROPOSAL,NATIVE,NAMES,Path(__file__)]}))
    print('Checkpoint v2 saved;18 scoped name reviews andtwo offline-verified fields. Completion8204/registered e713/registry/main unchanged; stored/new-English gameplay/release next.')

if __name__=='__main__':main()
