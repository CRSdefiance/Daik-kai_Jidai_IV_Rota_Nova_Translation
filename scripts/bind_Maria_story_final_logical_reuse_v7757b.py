"""Resolve cached logical-alignment lineage; preserve7757's predecessor-reference annotation."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_story_final_native_v7757b')
PRIOR=Path('work/analysis/maria_story_final_native_v7757/67_final_v3_compiled_pages_two_fresh65_exact_own_reuse.json')
V2=Path('work/analysis/maria_story_refined_v7735/67_refined_decisions_native_logical_bindings_automatic_plans_QA.json')
V1=Path('work/analysis/maria_story_logical_v7732/67_logical_paragraphs268_original_native_macro_literal_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,v2,v1=map(read,[PRIOR,V2,V1]);doc=read(prior['manuscript']);v2doc=read(v2['manuscript'])
    assert sha(Path(prior['manuscript']).read_bytes())==prior['manuscript_sha256']
    assert sha(Path(v2['manuscript']).read_bytes())==v2['manuscript_sha256']
    target=deepcopy(prior);bindings=[]
    for row in doc['records']:
        old=next(r for r in prior['logical_bindings'] if r['id']==row['id'])
        if row['id'] in prior['changed_record_IDs']:
            binding=deepcopy(old);binding.update(actual_fresh_execution_proof=str(PRIOR),actual_fresh_execution_proof_sha256=sha(PRIOR.read_bytes()))
        else:
            previous=next(r for r in v2doc['records'] if r['id']==row['id'])
            assert previous['english']==row['english'] and previous['source_selector']==row['source_selector']
            ref=next(r for r in v2['logical_bindings'] if r['id']==row['id'])
            assert ref['logical_body_hex']==row['english'].encode('cp932').hex()
            if ref['mode']=='four-fresh-alignments':
                pipeline=ref['native_alignment'];path=V2
            else:
                assert ref['mode']=='four-exact-own-current-alignments-reused' and ref['original_proof_sha256']==sha(V1.read_bytes())
                original=next(r for r in v1['records'] if r['id']==row['id'])
                assert original['logical_body_hex']==ref['logical_body_hex'] and original['source_selector']==row['source_selector']
                pipeline=original['native_alignment'];path=V1
            binding=dict(id=row['id'],mode='four-exact-v2-own-current-logical-alignments-reused',logical_hex=ref['logical_body_hex'],
                source_selector=row['source_selector'],native_alignment=deepcopy(pipeline),exact_alignment_proof=str(path),exact_alignment_proof_sha256=sha(path.read_bytes()),
                v2_binding_proof=str(V2),v2_binding_proof_sha256=sha(V2.read_bytes()),historical7757_predecessor_reference_annotation=old)
        expected=row['english'].encode('cp932').replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
        assert binding['native_alignment']['original_selector']==row['source_selector'] and len(binding['native_alignment']['cases'])==4
        assert all(c['output_hex']==expected.hex() for c in binding['native_alignment']['cases']);bindings.append(binding)
    assert len(bindings)==67;target['logical_bindings']=bindings
    target.update(previous_native_proof=str(PRIOR),previous_native_proof_sha256=sha(PRIOR.read_bytes()),
        all65_cached_logical_proofs_resolved_to_actual_native_alignment_rows=True,
        predecessor_effective_body_reference_not_mistaken_for_v2_logical_alignment_evidence=True,
        no_native_check_orfont_render_replayed=True)
    ROOT.mkdir(parents=True);out=ROOT/'67_final_v3_native_pages_andfully_bound_logical_lineage.json';save(out,target)
    save(ROOT/'logical_reuse_binding_receipt.json',dict(previous=str(PRIOR),previous_sha256=sha(PRIOR.read_bytes()),corrected_native_proof=str(out),corrected_native_proof_sha256=sha(out.read_bytes()),
        eight_fresh_logical_andcompiled_cases_reused_from7757=True,exact_cached_logical_cases=260,
        old_provenance_annotation_preserved_not_used_as_native_alignment_proof=True,no_ROM_capture_native_font_orcredit_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,V2,V1,Path(__file__)]},full_goal_complete=False))
    print('All67final logical lineages bound:8fresh cases from7757 plus260 exact earlier own-current cases.65cached rows nowpoint toactual alignment evidence.No native replay orcredit.')
