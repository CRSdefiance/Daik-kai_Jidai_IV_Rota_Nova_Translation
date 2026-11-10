"""Prepare B198 approval and complete source-preserving relocation with no menu assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B198_approval_relocation_tools_v5724')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/approve_lil_B195_native_v5557.py').read_text(encoding='utf-8')
    old=source[source.index('    retention_path='):source.index('    validate_natural_dialogue_batch(doc)')]
    new='''    refinement_path=Path('work/analysis/lil_B198_refrain_layout_v5722/one_refrain_phrase_protection_and_unchanged_prose.json')
    refinement=read(refinement_path)
    previous=read('work/analysis/lil_B198_fonts_v5721b/all17_progressive_FE_native_planes_and136_alignment_cases.json')
    before={r['id']:r for r in previous['cases']}
    changed=[r['id'] for r in font['cases'] if r['encoded_hex']!=before[r['id']]['encoded_hex']]
    assert changed==['DK4_MES_B198_R0010','DK4_MES_B198_R0014']
    assert refinement['all_words_native_metrics_width_guard_phase_bounds_pagination_and_runtime_unchanged']
    for row in doc['records']:
        if row['source_record_index'] in [10,14]:
            p=profile_for(arm,block,'FE-paper')
            qa=codec.audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],p)
            assert qa['visible_lines']==['Any naughty children here?','Any naughty children here?']
            row['native_layout_retention_reason']='Two complete repeated questions preserve the refrain; protect any/naughty without an authored break, shortened prose, width change or safety waiver.'
    doc['source_bound_wrap_retention_proof']=str(refinement_path)
    doc['source_bound_wrap_retention_proof_sha256']=sha(refinement_path.read_bytes())
'''
    rows=[derive('scripts/approve_lil_B195_native_v5557.py','scripts/approve_lil_B198_native_v5724.py',{
        'B195':'B198','native_approval_v5557':'native_approval_v5724',
        'lil_B195_layout_v1':'lil_B198_layout_v2',
        "INPUT=Path('translations/lil_B195_editorial_manuscript_v2.json')":"INPUT=Path('translations/lil_B198_editorial_manuscript_v3.json')",
        "OUTPUT=Path('translations/lil_B195_editorial_manuscript_v3.json')":"OUTPUT=Path('translations/lil_B198_editorial_manuscript_v4.json')",
        'fonts_v5553/all20_progressive_FE_native_planes_and160_alignment_cases':'fonts_v5723/all17_progressive_FE_native_planes_and136_alignment_cases',
        "len(font['cases'])==20":"len(font['cases'])==17",'alignment_calls\']==160':"alignment_calls']==136",
        '==(19,1)':'==(11,6)',"len(font['negative_controls'])==20":"len(font['negative_controls'])==18",
        'blocks[195]':'blocks[198]',"{'revise':3,'retain-wording':17}":"{'revise':12,'retain-wording':5}",
        "[('progressive',92),('FE-paper',254)]":"[('progressive',12),('FE-paper',254)]",
        old:new,'all20':'all17','viewed20-panel':'viewed17-panel','source_consumer_negatives=20':'source_consumer_negatives=18',
        'three_revisions_and_seventeen_individually_justified_retentions':'twelve_revisions_and_five_individually_justified_retentions',
        'source_unnamed_cheese_specialty_coaxing_two_chewing_beats_spreading_word_intention_and_character_popularity_claim_preserved':
        'source_Namahage_four_call_refrain_three_questions_dream_unnamed_object_and_prospective_handover_preserved',
        'all160':'all136',
        'All20 source/prose/current-native reviews approved:3 revisions/17 justified retentions,160 alignments,20 consumer/28 formatter negatives.':
        'All17 source/prose/current-native reviews approved:12 revisions/5 justified retentions,136 alignments,18 consumer/28 formatter negatives.'})]
    rows.append(derive('scripts/research_lil_B197_relocation_v5671.py','scripts/research_lil_B198_relocation_v5725.py',{
        'B197':'B198','relocation_v5671':'relocation_v5725',
        'lil_B197_editorial_manuscript_v3.json':'lil_B198_editorial_manuscript_v4.json',
        "MENU=Path('translations/lil_B197_choice_manuscript_v2.json')":"MENU=None",
        "doc,menu=read(DOC),read(MENU);voice={'records':[]}":"doc=read(DOC);menu={'records':[]};voice={'records':[]}",
        'combined_v5637':'combined_v5692','number==197':'number==198',
        "end_maps[0]['source_offset']==874":"end_maps[0]['source_offset']==540",
        'source[old_end:]==bytes(2)':'source[old_end:]==bytes(0)',
        'two_tailzeros':'zero_tailzeros',
        "text_records']) for r in results)==21":"text_records']) for r in results)==17",
        "choice_commands']) for r in results)==1":"choice_commands']) for r in results)==0",
        "relative_skip_fixups']) for r in results)==6":"relative_skip_fixups']) for r in results)==8",
        "target_native_skip_cases']) for r in results)==30":"target_native_skip_cases']) for r in results)==40",
        "command_map']) for r in results)==39":"command_map']) for r in results)==37",'in [197]':'in [198]',
        "choices=str(MENU),choices_sha256=sha(MENU.read_bytes()),":"choices=None,choices_sha256=None,",
        'one_original2200_object_three_source_ordered_proposal_refusal_delegation_labels=True':'no_original_choice_objects_or_labels=True',
        'all21speech_one_menu_and6_relative_operands':'all17speech_no_menu_and8_relative_operands',
        'all30_relocated_native_skip_cases':'all40_relocated_native_skip_cases','source_FE_system_objects=1':'source_FE_system_objects=6',
        '39commands/21speech/one2200/6spans/30targetskipcases,one common end,all880 predecessor bytes inverse and335otherblocks exact.':
        '37commands/17speech/no menu/8spans/40targetskipcases,one common end,all544 predecessor bytes inverse and335otherblocks exact.'}))
    rows.append(derive('scripts/prove_lil_B197_stored_v5672.py','scripts/prove_lil_B198_stored_v5726.py',{
        'B197':'B198','stored_v5672':'stored_v5726','relocation_v5671':'relocation_v5725',
        'lil_B197_editorial_manuscript_v3.json':'lil_B198_editorial_manuscript_v4.json',
        'voices_v5648':'voices_v5703','[21,169,254]':'[12,15,254]',
        'len(cases)==21':'len(cases)==17','fresh+reused==84':'fresh+reused==68',
        "sum(c['consumer']=='FE-paper' for c in cases)==1":"sum(c['consumer']=='FE-paper' for c in cases)==6",
        'all21':'all17','targets84_macro':'targets68_macro','current_final_stored_macro_alignment_cases=84':'current_final_stored_macro_alignment_cases=68',
        'stored_targets=21,progressive=20,FE=1,macro_cases=84':'stored_targets=17,progressive=11,FE=6,macro_cases=68'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_native_approval_and_source_locked_relocation.json',dict(tools=rows,source_commands=37,
        source_speeches=17,source_FE=6,relative_sites=8,target_native_skip_cases=40,ends=1,source_tailzeros=0,
        no_source_choices_or_style_objects=True,no_changed_native_metrics_runtime_or_authored_breaks=True,
        complete_predecessor_inverse_and_final_stored_native_checks_required=True,new_ROMs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared17-object approval,37-command relocation/eight spans/40 native skips,zero-tail inverse and68 final stored alignments. No release or credit.')
