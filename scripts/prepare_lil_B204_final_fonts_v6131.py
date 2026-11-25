"""Recheck changed native inputs;reuse only exactly identical current-native cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_final_font_tools_v6131')
if __name__=='__main__':
    assert not ROOT.exists()
    setup='''cases=[];qa_reports=[];pictures=[];macro_calls=0
    priorpath=Path('work/analysis/lil_B204_fonts_v6127/all20_progressive_FE_native_planes_and160_alignment_cases.json');prior=read(priorpath)
    olddoc=read('translations/lil_B204_editorial_manuscript_v3.json');oldrows={r['id']:r for r in olddoc['records']};oldcases={r['id']:r for r in prior['cases']};reused=[];fresh=[]
    assert prior['candidate_sha256']==doc['current_ROM_sha256']==olddoc['current_ROM_sha256'] and olddoc['current_strict_native_input_sha256']==doc['current_strict_native_input_sha256']
    assert prior['ARM9_sha256']==sha(arm) and prior['COMMON_sha256']==sha(common)
    assert sha(Path(prior['manuscript']).read_bytes())==prior['manuscript_sha256']'''
    reuse='''        previous=oldrows[row['id']];oldcase=oldcases[row['id']]
        assert row['english']==previous['english'] and row['source_hex']==previous['source_hex'] and row['source_selector']==previous['source_selector'] and row['kind']==previous['kind']
        if encoded.encoded.hex()==previous['compiled_hex']:
            assert oldcase['encoded_hex']==encoded.encoded.hex() and oldcase['formatted_markup']==encoded.formatted_markup and oldcase['one_native_page_consumes_complete_target']
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            reused.append(row['source_record_index']);case=dict(oldcase,native_case_reused_only_for_exact_same_whole_ROM_source_selector_logical_and_compiled_inputs=True)
            cases.append(case);pictures.append((row['id'],row['speaker'],Image.open(oldcase['preview']).convert('RGB')));macro_calls+=8
            print(row['id']+' exact current-native input reused',flush=True);continue
        fresh.append(row['source_record_index'])
'''
    tool=derive('scripts/verify_lil_B204_fonts_v6127.py','scripts/verify_lil_B204_fonts_v6131.py',{
        'fonts_v6127':'fonts_v6131','lil_B204_layout_v2':'lil_B204_layout_v4','manuscript_v3':'manuscript_v5',
        'cases=[];qa_reports=[];pictures=[];macro_calls=0':setup,
        "        logical=row['english'].split('}',1)[1]":reuse+"        logical=row['english'].split('}',1)[1]",
        "    assert sum(c['kind']=='system-FE' for c in cases)==4":"    assert sum(c['kind']=='system-FE' for c in cases)==4\n    assert fresh==[16,33,45,55,69] and len(reused)==15",
        'current_original_macro_alignment_calls=160':'current_original_macro_alignment_calls=160,new_native_alignment_calls=len(fresh)*8,exact_input_byte_identical_reused_native_alignment_cases=len(reused)*8,changed_source_indices=fresh,reused_source_indices=reused,prior_native_proof=str(priorpath),prior_native_proof_sha256=sha(priorpath.read_bytes())',
        'All20 current-font native planes,160 alignment cases and24 source-consumer negatives pass;three sheets need visual review.':'All20 current-font native planes and160 covered alignment cases pass:40 fresh/120 exact input reuses.24 source-consumer negatives;three sheets need visual review.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_native_reuse_derivation.json',dict(tool=tool,only_byte_identical_current_ROM_selector_logical_compiled_native_inputs_reused=True,all_changed_inputs_receive_fresh_eight_alignment_cases_and_full_native_plane=True,old_producers_and_planes_preserved=True,full_goal_complete=False));print('Final B204 native verifier prepared:five changed inputs rerun,fifteen exact inputs reused,24 controls rerun.')
