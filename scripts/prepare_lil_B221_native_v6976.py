"""Prepare source-locked B221 display checks and a complete source-content capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text, derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B221_native_tools_v6976')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[
        ('scripts/native_B206_menu_backing_v6285.py','scripts/native_B221_menu_backing_v6976.py',{
            '4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':
            'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'}),
        ('scripts/plan_lil_B220_layout_v6927b.py','scripts/plan_lil_B221_layout_v6976.py',{
            'B220':'B221','layout_v6927b':'layout_v6976','[26,199]':'[2,17,85]',
            '''PAIRS={('empress','gown'),('chinese','empress'),("wasn't",'it'),("aren't",'you'),("don't",'you'),('just','like'),('just','the'),('right','amount'),('every','time'),('present','out'),('out','of')}''':
            '''PAIRS={('holy','land'),('islamic','history'),('peace','terms'),('come','to'),('think','of'),('of','it'),('anything','went'),('gone','missing'),('our','true'),('true','hero'),('good','person'),('dirty','tricks')}''',
            "            if row['id']=='DK4_MES_B220_R0035' and pair==('chinese','empress'):weak=0\n":'',
            'seventeen_whole_paragraph_plans_no_macros_no_prose_changes':'fourteen_whole_paragraph_plans_no_macros_no_prose_changes',
            'all17_formatting_gates_remain_false':'all14_formatting_gates_remain_false'}),
        ('scripts/research_lil_B220_source_fixture_v6930.py','scripts/research_lil_B221_source_fixture_v6978.py',{
            'B220':'B221','v6930':'v6978',
            'source_v6921/seventeen_clean_current_empress_gown_exchange_source_references':
            'source_v6967/sixteen_clean_current_Crusades_Saladin_context_four_relative_sites_one_choice',
            'blocks[220]':'blocks[221]','source_block=220':'source_block=221',
            'len(jp)==1280 and end==1280':'len(jp)==1208 and end==1208',
            'len(commands)==29 and len(speeches)==17':'len(commands)==30 and len(speeches)==14',
            'all29_stored_fixture_commands':'all30_stored_fixture_commands',
            'all20_source_commands_plus9_original_initializers_stored':'all21_source_commands_plus9_original_initializers_stored',
            'source_event220_not_naturally_activated':'source_event221_not_naturally_activated',
            'Complete B220 clean-source17-speech empress-gown flirtation with all20 commands,no relatives/predicates,original A000,C200,zero macros and complete normal end.':
            'Complete B221 clean-source14-speech Crusades/Saladin exchange with both original choice labels,all21 commands,four relatives,one2100,original A000,zero macros and complete normal end.',
            '20 original+9 initializer commands;17 speeches,zero macros,no predicate/relative/typed commands,original A000,C200 and complete normal end.':
            '21 original+9 initializer commands;14 speeches,both original choice labels,four relatives,one2100,original A000 and complete normal end.'}),
        ('scripts/run_lil_B220_source_v6931.py','scripts/run_lil_B221_source_v6979.py',{
            'B220':'B221','source_fixture_v6930':'source_fixture_v6978',
            'source_run_v6931':'source_run_v6979','source_v6931':'source_v6979',
            "source_block']==220":"source_block']==221",
            "'source_event220_not_naturally_selected':True,'displayed_original_source_block':220,'all20_source_commands_retained':True":
            "'source_event221_not_naturally_selected':True,'displayed_original_source_block':221,'all21_source_commands_retained':True"}),
        ('scripts/verify_lil_B220_native_pages_v6928.py','scripts/verify_lil_B221_native_pages_v6980.py',{
            'B220':'B221','layout_v6927/seventeen_whole_paragraph_plans_no_macros_no_prose_changes':
            'layout_v6976/fourteen_whole_paragraph_plans_no_macros_no_prose_changes',
            'current_V6910_native_v6920':'current_V6956_native_v6966','native_pages_v6928':'native_pages_v6980',
            "len(plan['records'])==17":"len(plan['records'])==14",'[26,199]':'[2,17,85]',
            'len(cases)==len(pictures)==17 and alignments==136':'len(cases)==len(pictures)==14 and alignments==112',
            'all17_complete_pages_sheet':'all14_complete_pages_sheet',
            'all17_paragraphs17_complete_native_pages136_alignments':'all14_paragraphs14_complete_native_pages112_alignments',
            'complete_native_pages=17':'complete_native_pages=14',
            'logical_compiled_input_alignment_cases=136':'logical_compiled_input_alignment_cases=112',
            'all17_single_pages':'all14_single_pages',
            'only_original_static_selectors26_199':'only_original_static_selectors2_17_85',
            'all17_formatting_gates_remain_false':'all14_formatting_gates_remain_false',
            '17 complete single native pages/136 alignments':'14 complete single native pages/112 alignments'}),
    ]
    for source,target,changes in jobs:
        assert not Path(target).exists()
        checked_text(Path(source).read_text('utf-8'),changes)
    rows=[derive(source,target,changes) for source,target,changes in jobs]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_B221_layout_menu_source_fixture_and_native_pages.json',dict(
        derivations=rows,source_choice_and_four_relative_sites_preserved_in_complete_fixture=True,
        no_inherited_empress_C200_or_Chinese_empress_boundary_exception=True,
        menu_helper_only_exact_ARM9_hash_updated_same_native_geometry=True,
        original_216x64_body_and_256x36_menu_backing_limits_preserved=True,
        no_ROM_or_run_or_review_credit_by_preparer=True,full_goal_complete=False))
    print('Five source-locked B221 tools prepared; no ROM, run or credit from preparation.')
