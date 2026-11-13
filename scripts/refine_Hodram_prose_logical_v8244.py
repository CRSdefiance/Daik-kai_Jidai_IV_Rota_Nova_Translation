"""Polish one formal reply after a whole-exchange reread; recheck only its four native alignments."""
from copy import deepcopy
import inspect
from pathlib import Path
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Hodram_B137_B45_B46_refinement_v8244')
OLD=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v2.json')
PRIOR=Path('work/analysis/Hodram_B137_B45_B46_logical_v8242/28_logical_paragraphs112_original_native_alignments_no_FE.json')
NAMES=Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    old,prior,names=map(read,[OLD,PRIOR,NAMES]);doc=deepcopy(old)
    assert prior['manuscript_sha256']==sha(OLD.read_bytes())
    prog=checked_text(inspect.getsource(progressive_expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==1'})
    assert prog==prior['source_owned_progressive_adapter']
    pe=dict(progressive_expand.__globals__);exec(compile(prog,__file__+'::unchanged-captain1','exec'),pe)
    selected=next(r for r in doc['records'] if r['id']=='DK4_MES_B137_R0047')
    selected['english']=selected['logical_English']="I appreciate your thoughtful apology. With someone as capable as you at her side, she can make the most of her talents."
    selected['localization_note']=selected['editorial_finding']="A whole-exchange reread replaces the inflated gracious apology/no wonder she's able wording with a clearer formal acknowledgment and direct causal praise. Thoughtful apology conveys丁重な謝罪; the capable companion still enables Lil's talents. Hodram remains courteous and restrained, Camille's modest reply remains motivated, and no new role or relationship is introduced. This is an editorial clarity revision, not a deletion of meaning to imitate a fixed allocation."
    doc.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),whole_exchange_second_read_complete=True,
        single_reply_polished_for_natural_formal_voice_not_shortened_to_fixed_allocation=True)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    body=selected['english'].encode('cp932');result=ctx.execute(pe['expand'],body,selected['source_selector']);ctx.machines.pop()
    assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases']) and not ctx.machines
    logical=[]
    for row,original in zip(doc['records'],old['records'],strict=True):
        inherited=deepcopy(next(p for p in prior['records'] if p['id']==row['id']))
        if row['id']==selected['id']:
            inherited.update(logical_body_hex=body.hex(),expected_expanded_hex=body.hex(),native_alignment=result,fresh_after_editorial_refinement=True)
        else:
            assert row==original and bytes.fromhex(inherited['logical_body_hex'])==row['english'].encode('cp932')
            inherited.update(exact_reuse_from=str(PRIOR),exact_reuse_from_sha256=sha(PRIOR.read_bytes()),unchanged_complete_record_andlogical_body=True)
        logical.append(inherited)
    save(DOC,doc)
    save(ROOT/'28_logical_paragraphs4_fresh108_exact_reused_alignments.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),prior_logical=str(PRIOR),prior_logical_sha256=sha(PRIOR.read_bytes()),
        records=logical,fresh_native_alignment_cases=4,exact_reused_native_alignment_cases=108,total_bound_alignment_cases=112,
        source_owned_progressive_adapter=prog,original_captain=1,source_macro_totals=dict(FI=0,FA=0,FO=0),
        all_native_ABI_input_output_canaries_scratch_ownership_andunowned4MiB_exact=True,
        logical_bytes_not_wrapped_fonts_bounds_stored_oractual_UI=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,PRIOR,NAMES,Path(__file__)]}))
    print('Polished Hodram formal reply;4fresh/108exact reused native alignments;formatting/actual/release remainpending.')
