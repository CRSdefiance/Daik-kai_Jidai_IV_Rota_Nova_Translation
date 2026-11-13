"""Keep the tease and reading admission intact;reuse only identical native inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B203_wrap_tools_v6029')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B203_layout_v1.py','dk4tool/dialogue/lil_B203_layout_v2.py',{
        '# B203 needs no inherited B201 sale-specific phrase or boundary exceptions.':"# Preserve the complete teasing clause and Mikhail reading phrase.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('your','companion'),('companion','seems'),('seems','to'),('to','want'),('want','it'),('wanted','to'),('to','read'),('read','that'),('that','book')})",
    })]
    tools.append(derive('scripts/plan_lil_B203_layout_v6027.py','scripts/plan_lil_B203_layout_v6029.py',{
        'layout_v6027':'layout_v6029','lil_B203_layout_v1':'lil_B203_layout_v2',
        "INPUT=Path('translations/lil_B203_editorial_manuscript_v1.json')":"INPUT=Path('translations/lil_B203_editorial_manuscript_v2.json')",
        "OUTPUT=Path('translations/lil_B203_editorial_manuscript_v2.json')":"OUTPUT=Path('translations/lil_B203_editorial_manuscript_v3.json')",
    }))
    reuse='''        oldcase=oldcases[row['id']]
        if encoded.encoded.hex()==oldcase['encoded_hex']:
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            if isFE:assert sha(Path(oldcase['native_plane']).read_bytes())==oldcase['whole_native_plane_sha256']
            cases.append(dict(oldcase));pictures.append((row['id'],row['speaker'],Image.open(oldcase['preview']).convert('RGB')))
            macro_calls+=8;reused+=8;reuse_ids.append(row['id']);continue
        fresh+=8
        logical=row['english'].split('}',1)[1]'''
    tools.append(derive('scripts/verify_lil_B203_fonts_v6028.py','scripts/verify_lil_B203_fonts_v6030.py',{
        'fonts_v6028':'fonts_v6030','manuscript_v2.json':'manuscript_v3.json','lil_B203_layout_v1':'lil_B203_layout_v2',
        'cases=[];qa_reports=[];pictures=[];macro_calls=0':'''cases=[];qa_reports=[];pictures=[];macro_calls=0;fresh=0;reused=0;reuse_ids=[]
    priorpath=Path('work/analysis/lil_B203_fonts_v6028/all22_progressive_FE_native_planes_and176_alignment_cases.json');old=read(priorpath);oldcases={r['id']:r for r in old['cases']};olddoc=read(old['manuscript'])
    assert old['ARM9_sha256']==sha(arm) and old['COMMON_sha256']==sha(common) and old['candidate_sha256']==doc['current_ROM_sha256']
    assert [(r['id'],r['english'],r['source_hex'],r['current_hex']) for r in doc['records']]==[(r['id'],r['english'],r['source_hex'],r['current_hex']) for r in olddoc['records']]''',
        "        logical=row['english'].split('}',1)[1]":reuse,
        'assert len(cases)==len(qa_reports)==22 and macro_calls==176 and not ctx.machines':'assert len(cases)==len(qa_reports)==22 and macro_calls==176 and fresh==16 and reused==160 and len(reuse_ids)==20 and not ctx.machines',
        'current_original_macro_alignment_calls=176,progressive_alignment_calls=168':'current_original_macro_alignment_calls=176,new_native_alignment_calls=fresh,exact_input_byte_identical_reused_native_alignment_cases=reused,prior_native_proof=str(priorpath),prior_native_proof_sha256=sha(priorpath.read_bytes()),input_identical_reused_IDs=reuse_ids,progressive_alignment_calls=168',
        'All22 current-font native planes,176 alignment cases and22 source-consumer negatives pass;three sheets need visual review.':'All22 final planes/176 covered alignments:16 fresh for R67/R70,160 exact-input reuse.22 consumer negatives fresh;changed sheet needs review.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_phrase_and_native_reuse_tools.json',dict(tools=tools,unchanged22_prose_wordings_source_controls_metrics_guards_phase_and_four_row_limits=True,changed_phrase_indices=[67,70],no_weak_boundary_or_other_safety_waiver=True,full_goal_complete=False))
    print('Teasing-clause/reading-phrase successor prepared;no prose shortening,native geometry change or safety waiver.')
