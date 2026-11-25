"""Bind one new logical introduction and15 exact prior own-current native proofs."""
from copy import deepcopy
from pathlib import Path
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_confrontation_refined_logical_v7797')
MANUSCRIPT=Path('translations/maria_B36_editorial_manuscript_v2.json')
PREVIOUS=Path('translations/maria_B36_editorial_manuscript_v1.json')
PRIOR=Path('work/analysis/maria_confrontation_logical_v7792/16_logical_paragraphs64_original_native_macro_literal_alignments.json')
NAMES=Path('work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,old,prior,names=map(read,[MANUSCRIPT,PREVIOUS,PRIOR,NAMES])
    assert prior['manuscript_sha256']==sha(PREVIOUS.read_bytes()) and prior['fresh_native_alignment_cases']==64
    inp=Path(names['current_native_input']);assert sha(inp.read_bytes())==names['current_native_input_sha256']
    adapter=prior['source_owned_Maria_adapter'];ns={**expand.__globals__,'EXPECTED_CAPTAIN':3};exec(compile(adapter,__file__+'::unchanged-Maria-native-adapter','exec'),ns)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');rows=[];fresh=reused=0
    for row in doc['records']:
        before=next(r for r in old['records'] if r['id']==row['id']);proof=next(r for r in prior['records'] if r['id']==row['id'])
        body=row['english'].encode('cp932');expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
        if row['english']==before['english']:
            assert proof['logical_body_hex']==body.hex() and proof['source_selector']==row['source_selector']
            result=deepcopy(proof['native_alignment']);reused+=4;mode='exact-own-current-logical-body-selector-andinput-reuse'
        else:
            assert row['source_record_index']==23 and row['source_hex']==before['source_hex']
            result=ctx.execute(ns['expand'],body,row['source_selector']);ctx.machines.pop();fresh+=4;mode='fresh-FO-before-FI-introduction'
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],source_selector=row['source_selector'],logical_body_hex=body.hex(),
            expected_expanded_hex=expected.hex(),native_alignment=result,proof_mode=mode,
            exact_prior_proof=str(PRIOR) if mode.startswith('exact') else None,exact_prior_proof_sha256=sha(PRIOR.read_bytes()) if mode.startswith('exact') else None))
    assert fresh==4 and reused==60 and len(rows)==16 and not ctx.machines
    save(ROOT/'16_final_logical_paragraphs4_fresh60_exact_reused_alignments.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),records=rows,
        fresh_native_alignment_cases=4,exact_own_current_alignment_cases_reused=60,final_native_alignment_coverage=64,
        source_owned_Maria_adapter=adapter,all_original_ABI_input_output_canary_scratch_andunowned4MiB_guards_preserved=True,
        original_FO_before_FI_order_preserved=True,no_global_macro_guard_orfont_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,PREVIOUS,PRIOR,NAMES,inp,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('Final logical paragraphs:4fresh introduction alignments/60exact prior alignments;all16complete.FO-before-FI intact.')
