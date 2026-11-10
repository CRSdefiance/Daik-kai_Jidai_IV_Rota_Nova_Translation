"""Source-lock B230's complete source fixture and unchanged observation tools."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_capture_tools_v7435')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B229':'B230','source_v7381/seventeen_clean_current_giant_tortoise_callback_source_references':'source_v7428/seventeen_clean_current_phoenix_bascinet_callback_source_references','source_fixture_v7387':'source_fixture_v7435','source_v7387':'source_v7435','source_run_v7388':'source_run_v7436','source_v7388':'source_v7436','source_pages_v7389':'source_pages_v7437','source_actual_v7390':'source_actual_v7438','name_planes_v7386':'name_planes_v7433','consumers_v7382':'consumers_v7429','giant-tortoise-shield-callback':'phoenix-bascinet-callback','giant-tortoise-shield callback':'phoenix-bascinet callback','source_event229':'source_event230','event229':'event230'}
    jobs=[]
    plans=[('research_lil_B229_source_fixture_v7387b','research_lil_B230_source_fixture_v7435',{'blocks[229]':'blocks[230]','source_block=229':'source_block=230','len(jp)==944 and end==944':'len(jp)==988 and end==988'}),('run_lil_B229_source_v7388','run_lil_B230_source_v7436',{"selected['source_block']==229":"selected['source_block']==230","'displayed_original_source_block':229":"'displayed_original_source_block':230"}),('prove_lil_B229_source_pages_v7389','prove_lil_B230_source_pages_v7437',{}),('audit_lil_B229_source_v7390','audit_lil_B230_source_v7438',{"p['source_offset']==932":"p['source_offset']==976",'original_A000_at932':'original_A000_at976'})]
    for a,b,extra in plans:
        src=Path('scripts/'+a+'.py').read_text('utf8');changes={k:v for k,v in common.items() if k in src};changes.update(extra);assert not Path('scripts/'+b+'.py').exists();checked_text(src,changes);jobs.append(('scripts/'+a+'.py','scripts/'+b+'.py',changes))
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_capture_tools.json',dict(tools=rows,source988_logical988_tail0=True,all19_source_commands17_speeches_and9_original_initializers=True,ordinary16001_frame_input_schedule_unchanged=True,no_forced_completion229_ororiginal_eligibility_claim=True,new_credit=0,full_goal_complete=False))
