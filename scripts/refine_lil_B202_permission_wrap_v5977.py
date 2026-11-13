"""Keep the complete permission phrase intact;reuse only input-identical native cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B202_wrap_tools_v5977')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B202_layout_v1.py','dk4tool/dialogue/lil_B202_layout_v2.py',{
      '# B202 needs no inherited B201 sale-specific phrase or boundary exceptions.':'# Keep the complete source permission Use it however you like together.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({(\'use\',\'it\'),(\'it\',\'however\'),(\'however\',\'you\'),(\'you\',\'like\')})'})]
    tools.append(derive('scripts/plan_lil_B202_layout_v5975.py','scripts/plan_lil_B202_layout_v5977.py',{
      'layout_v5975':'layout_v5977','lil_B202_layout_v1':'lil_B202_layout_v2',
      "INPUT=Path('translations/lil_B202_editorial_manuscript_v1.json')":"INPUT=Path('translations/lil_B202_editorial_manuscript_v2.json')",
      "OUTPUT=Path('translations/lil_B202_editorial_manuscript_v2.json')":"OUTPUT=Path('translations/lil_B202_editorial_manuscript_v3.json')"}))
    source=Path('scripts/verify_lil_B202_fonts_v5976.py').read_text(encoding='utf-8');line=next(s for s in source.splitlines() if s.strip().startswith('encoded=encode_relocatable_dialogue'))
    head,tail=line.split(';logical=',1)
    revised=head+'''
        oldcase=oldcases[row['id']]
        if encoded.encoded.hex()==oldcase['encoded_hex']:
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            cases.append(dict(oldcase));reports.append(dict(id=row['id'],qa=qa,encoded_hex=encoded.encoded.hex(),unwaived_issues=issues,documented_waivers=row.get('qa_waivers',[])))
            pictures.append((row['id'],row['speaker'],Image.open(oldcase['preview']).convert('RGB')));macro_calls+=8;reused+=8;reuse_ids.append(row['id']);continue
        fresh+=8
        logical='''+tail
    tools.append(derive('scripts/verify_lil_B202_fonts_v5976.py','scripts/verify_lil_B202_fonts_v5978.py',{
      'fonts_v5976':'fonts_v5978','manuscript_v2.json':'manuscript_v3.json','lil_B202_layout_v1':'lil_B202_layout_v2',
      'cases=[];reports=[];pictures=[];macro_calls=0':'''cases=[];reports=[];pictures=[];macro_calls=0;fresh=0;reused=0;reuse_ids=[]
    priorpath=Path('work/analysis/lil_B202_fonts_v5976/all19_progressive_native_planes_and152_alignment_cases.json');old=read(priorpath);oldcases={r['id']:r for r in old['cases']};olddoc=read(old['manuscript'])
    assert old['ARM9_sha256']==sha(arm) and old['COMMON_sha256']==sha(common) and old['candidate_sha256']==doc['current_ROM_sha256']
    assert [(r['id'],r['english'],r['source_hex'],r['current_hex']) for r in doc['records']]==[(r['id'],r['english'],r['source_hex'],r['current_hex']) for r in olddoc['records']]''',
      line:revised,
      "assert len(cases)==len(reports)==19 and macro_calls==152 and not ctx.machines":"assert len(cases)==len(reports)==19 and macro_calls==152 and fresh==8 and reused==144 and len(reuse_ids)==18 and not ctx.machines",
      'current_original_macro_alignment_calls=152,progressive_alignment_calls=152':'current_original_macro_alignment_calls=152,new_native_alignment_calls=fresh,exact_input_byte_identical_reused_native_alignment_cases=reused,prior_native_proof=str(priorpath),prior_native_proof_sha256=sha(priorpath.read_bytes()),input_identical_reused_IDs=reuse_ids,progressive_alignment_calls=152',
      'All19 current-font progressive planes,152 alignments and21 source-consumer negatives pass;three sheets await visual review.':'All19 final planes/152 covered alignments:8 fresh for R13,144 exact-input reuse.21 consumer negatives fresh;changed sheet needs visual review.'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_permission_phrase_and_native_reuse_tools.json',dict(tools=tools,unchanged19_prose_wordings_source_controls_metrics_guards_phase_and_four_row_limits=True,permission_group=['Use','it','however','you','like'],no_weak_boundary_or_other_safety_waiver=True,full_goal_complete=False))
    print('Permission phrase successor and exact per-record native reuse prepared. No prose shortening or display-limit change.')
