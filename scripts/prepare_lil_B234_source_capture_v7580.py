"""Freeze B234 source-display tools without changing native instructions or input timing."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_capture_tools_v7580')
if __name__=='__main__':
    assert not ROOT.exists()
    common={
        'B233':'B234',
        'source_v7526/eleven_clean_current_chisel_library_fragment_tools_joke_source_references':'source_v7574/eighteen_clean_current_familiar_banter_papal_trade_andconditional_discovery_source_references',
        'source_fixture_v7532':'source_fixture_v7580','source_v7532':'source_v7580',
        'source_run_v7533':'source_run_v7581','source_v7533':'source_v7581',
        'source_pages_v7534b':'source_pages_v7582','source_actual_v7535b':'source_actual_v7583',
        'name_planes_v7531/two_actors_four_getters_six_literal_planes24_alignments':'name_planes_v7579/two_actors_four_getters_five_literal_planes20_alignments',
        'consumers_v7527/eleven_effective_bodies22_dispatches_two_actors_four_name_consumers':'consumers_v7575/eighteen_effective_bodies36_dispatches_two_actors_four_name_consumers',
        'all11':'all18','all13':'all20','all22':'all29','event233':'event234',
        'legendary-chisel-library-fragment':'familiar-banter-papal-trade',
        'legendary-chisel library-fragment':'familiar-banter papal-trade',
    }
    plans=[
      ('research_lil_B233_source_fixture_v7532','research_lil_B234_source_fixture_v7580',{
        'blocks[233]':'blocks[234]','source_block=233':'source_block=234',
        'len(jp)==964 and end==962 and jp[end:]==bytes(2)':'len(jp)==1468 and end==1468 and jp[end:]==b\'\'',
        'len(commands)==22 and len(speeches)==11':'len(commands)==29 and len(speeches)==18',
        'clean-source11-speech':'clean-source18-speech','13 original+9 initializer commands;11 speeches':'20 original+9 initializer commands;18 speeches',
      }),
      ('run_lil_B233_source_v7533','run_lil_B234_source_v7581',{
        "selected['source_block']==233":"selected['source_block']==234",
        "'displayed_original_source_block':233":"'displayed_original_source_block':234",
      }),
      ('prove_lil_B233_source_pages_v7534b','prove_lil_B234_source_pages_v7582',{
        'len(rows)==11':'len(rows)==18','complete_objects=11':'complete_objects=18','source_objects=11':'source_objects=18',
      }),
      ('audit_lil_B233_source_v7535b','audit_lil_B234_source_v7583',{
        "font_proof['complete_native_pages']==11":"font_proof['complete_native_pages']==18",
        'len(pairs)==22':'len(pairs)==29','len(observations)==11':'len(observations)==18',
        "p['source_offset']==950":"p['source_offset']==1456",'range(0,11,6)':'range(0,18,6)',
        'masks22_commands':'masks29_commands','actual_source_unique_speeches=11':'actual_source_unique_speeches=18',
        'original_A000_at950':'original_A000_at1456','all9_initializers_and13_original_commands':'all9_initializers_and20_original_commands',
        'actual_Japanese_speeches=11':'actual_Japanese_speeches=18','commands=22,exit=':'commands=29,exit=',
        "consumer['all22_source_current_dispatches']":"consumer['all36_source_current_dispatches']",
      }),
    ];jobs=[]
    for a,b,extra in plans:
        src=Path('scripts/'+a+'.py').read_text('utf8');changes={k:v for k,v in common.items() if k in src};changes.update(extra)
        assert not Path('scripts/'+b+'.py').exists();planned=checked_text(src,changes)
        assert 'all16_paragraphs16_complete_native_pages128_alignments' in planned or 'source_pages' not in a
        jobs.append(('scripts/'+a+'.py','scripts/'+b+'.py',changes))
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_capture_tools.json',dict(tools=rows,source1468_logical1468_tail0_all20_commands18_speeches_preserved=True,original9_initializers_andordinary16001_frame_schedule_unchanged=True,immutable_historical_B222_all16_prior_path_preserved=True,five_name_planes20_alignments_eight_fresh_twelve_exact_reuse=True,complete_source_selector68_not_ASCII_prose=True,source_ellipsis_light_gray_palette_focused_check_pending=True,no_forced_natural_activation_original_location_orfull_effect_claim=True,new_credit=0,full_goal_complete=False))
