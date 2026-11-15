"""Combine two fresh final-v3 English checks with four exact unchanged actual groups."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_final_actual_binding_v7766')
OLD=Path('work/analysis/maria_story_actual_v7752c/six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json')
NEW=Path('work/analysis/maria_story_final_actual_v7765/two_final_English_captures_actual_pages_headers_branches_returns.json')
STORED=Path('work/analysis/maria_story_final_stored_v7759/67_final_v3_stored_pages33_tails_two_new_dispatches65_exact_reuse.json')
PRIOR_STORED=Path('work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json')
if __name__=='__main__':
    assert not ROOT.exists();old,new,stored,prior=map(read,[OLD,NEW,STORED,PRIOR_STORED])
    assert not old['unresolved'] and not new['unresolved'] and len(new['groups'])==2
    groups=[];reused=[]
    for group in old['groups']:
        key=group['block'],group['version']
        if key in [(34,'English'),(108,'English')]:
            after=next(g for g in new['groups'] if (g['block'],g['version'])==key)
            assert after['input_schedule_sha256']==group['input_schedule_sha256']
            assert set(s['id'] for s in after['speech_observations'])==set(s['id'] for s in group['speech_observations'])
            groups.append(deepcopy(after))
        else:
            for keypath,keyhash in [('capture_report','capture_report_sha256'),('observer_report','observer_report_sha256')]:
                assert sha(Path(group[keypath]).read_bytes())==group[keyhash]
            fixture=group['fixture'];assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
            if group['version']=='English':
                for speech in group['speech_observations']:
                    a=next(r for r in prior['records'] if r['id']==speech['id'])
                    b=next(r for r in stored['records'] if r['id']==speech['id'])
                    assert a['final_target_hex']==b['final_target_hex'] and a['final_expanded_hex']==b['final_expanded_hex']
                    assert [p['native_plane_sha256'] for p in a['complete_pages']['pages']]==[p['native_plane_sha256'] for p in b['complete_pages']['pages']]
            groups.append(deepcopy(group));reused.append(dict(block=group['block'],version=group['version'],prior_group_sha256=sha(__import__('json').dumps(group,sort_keys=True).encode())))
    assert len(groups)==6 and len(reused)==4
    assert sum(g['actual_unique_speeches'] for g in groups)==130
    assert sum(g['actual_complete_page_panels'] for g in groups)==130
    assert all(not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows'] for g in groups)
    out=deepcopy(old);out.update(groups=groups,total_actual_speech_occurrences=130,complete_actual_page_panels=130,
        fresh_final_English_capture_groups=2,exact_unchanged_actual_groups_reused=reused,
        previous_v2_actual_proof=str(OLD),previous_v2_actual_proof_sha256=sha(OLD.read_bytes()),
        final_affected_actual_proof=str(NEW),final_affected_actual_proof_sha256=sha(NEW.read_bytes()),
        old_v2_B108_two_page_capture_preserved_not_mistaken_for_final_prose=True,
        all67_stored_positions_preserved_two_Julian_conditionals_offline_only=True,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,NEW,STORED,PRIOR_STORED,Path(__file__)]})
    ROOT.mkdir(parents=True);save(ROOT/'six_final_v3_actual_groups_two_fresh_four_exact_reused.json',out)
    print('Final actual coverage130occurrences/130pages;two fresh English groups,four exact prior groups;two Julian conditionals offline only.')
