"""Reuse eleven exact paragraph proofs; freshly check only the refined payment explanation."""
from copy import deepcopy
from pathlib import Path
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B45_logical_refined_v7876b')
PREVIOUS=Path('work/analysis/Rafael_B45_logical_v7874/12_logical_paragraphs48_original_native_alignments_distinct_FE.json')
MANUSCRIPT=Path('translations/rafael_B45_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,doc=map(read,[PREVIOUS,MANUSCRIPT])
    old_doc=read(prior['manuscript']);assert sha(Path(prior['manuscript']).read_bytes())==prior['manuscript_sha256']
    names=read(prior['names_proof']);ROOT.mkdir(parents=True)
    ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    env=dict(expand.__globals__);exec(compile(prior['source_owned_progressive_adapter'],__file__+'::same-original-captain0-adapter','exec'),env)
    rows=[];reused=[];fresh=[]
    for row,old in zip(doc['records'],old_doc['records'],strict=True):
        assert row['id']==old['id'];p=deepcopy(next(r for r in prior['records'] if r['id']==row['id']))
        if row==old:
            assert p['logical_body_hex']==row['english'].encode('cp932').hex()
            reused.append(row['id'])
        else:
            assert row['source_record_index']==29 and row['source_selector']==6 and row['source_hex']==old['source_hex']
            body=row['english'].encode('ascii');result=ctx.execute(env['expand'],body,6);ctx.machines.pop()
            assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])
            p.update(logical_body_hex=body.hex(),expected_expanded_hex=body.hex(),native_alignment=result)
            fresh.append(row['id'])
        rows.append(p)
    assert len(reused)==11 and fresh==['DK4_MES_B45_R0029'] and not ctx.machines
    save(ROOT/'12_refined_logical_bindings44_reused4_fresh_alignments.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),names_proof=prior['names_proof'],names_proof_sha256=prior['names_proof_sha256'],
        records=rows,total_bound_alignment_cases=48,fresh_native_alignment_cases=4,exact_reused_alignment_cases=44,
        reused_ids=reused,fresh_ids=fresh,prior_proof=str(PREVIOUS),prior_proof_sha256=sha(PREVIOUS.read_bytes()),
        source_owned_progressive_adapter=prior['source_owned_progressive_adapter'],source_owned_FE_adapter=prior['source_owned_FE_adapter'],
        same_current_ROM_context_code_macros_andliteral_guards=True,all11_unchanged_record_objects_andlogical_bytes_exact=True,
        all12_formatting_false=True,no_actual_orfont_orrelease_approval=True,new_credit=0,new_emulator_runs=0,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),full_goal_complete=False))
    print('48 logical alignments bound:44 exact unchanged cases reused;four fresh R29 cases pass.')
