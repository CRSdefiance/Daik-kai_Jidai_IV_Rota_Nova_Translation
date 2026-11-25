"""Record the actual49-speech branch without claiming the two unvisited conditional asides."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael330_actual_analysis_inputs_20261105')
PARENT=ROOT/'B81_complete_bullfight_fixture.json'
PACKET=Path('work/analysis/Rafael_B81_B84_current_20261105/current_effective.json')
REBUILT=Path('work/analysis/Rafael_B81_B84_rebuilt_20261105/reconstruction.json')
TERMINAL=Path('work/analysis/Rafael_B81_complete_scene_run_v1_20261105/terminal.json')

if __name__=='__main__':
    output=ROOT/'B81_observed_branch_fixture_v2.json';assert not output.exists()
    doc=load(PARENT);packet=load(PACKET)['groups'][0];rebuilt=load(REBUILT)['groups'][0]
    terminal=load(TERMINAL);observer=load(Path(terminal['observer']))
    assert terminal['terminal'] and terminal['frames']==24001 and doc['complete_original_scene_including_transitions_andbranches_retained']
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    missing=['DK4_MES_B81_R0037','DK4_MES_B81_R0070'];findings=[]
    commands=packet['all_source_commands']
    for ident,ancestor,predicate,operand in [(missing[0],362,346,'0080ffff04fe0030'),(missing[1],680,664,'0080ffff0ffe0030')]:
        row=next(r for r in packet['records'] if r['id']==ident)
        source=next(c for c in commands if c['offset']==row['source_reference']['header_offset'])
        assert source['ancestor_0100_offsets']==[ancestor]
        guard=next(c for c in commands if c['offset']==predicate)
        assert guard['word']==0x8000 and guard['whole_command_hex']==operand
        mapping=rebuilt['first_page_reconstruction']['command_map']
        mapped=next(c['new_offset'] for c in mapping if c['old_offset']==predicate)
        target=next(c for c in rebuilt['all_target_commands'] if c['offset']==mapped)
        assert target['whole_command_hex']==operand
        selected=next(r for r in doc['selected_records'] if r['id']==ident)
        assert not any(p['kind']=='modal_paint' and p['text_hex']==selected['expected_expanded_body_hex'] for p in observer['rows'])
        findings.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_conditional_ancestor=ancestor,source_guard_offset=predicate,complete_guard_hex=operand,
            relocated_guard_offset=mapped,complete_original_guard_preserved=True,
            actual_body_unvisited_in_this_branch=True,offline_full_native_review_retained=True,
            exact_member_flag_semantics_oralternate_actual_outcome_not_newly_claimed=True))
    original=deepcopy(doc['selected_records']);doc['selected_records']=[r for r in original if r['id'] not in missing]
    expected=[r['expected_expanded_body_hex'] for r in doc['selected_records']]
    actual=[r['text_hex'] for r in observer['rows'] if r['kind']=='modal_paint' and r['frame']>=2800 and r['text_hex'] in set(expected)]
    assert expected==actual and len(actual)==49
    doc.update(expected_pages=49,ordinary_actor_IDs=sorted({r['selector'] for r in doc['selected_records'] if r['selector']!=254}),
        all_original_source_selected_records=original,original_source_speeches=51,observed_source_speeches=49,
        unvisited_conditional_records=findings,actual_branch_coverage_not_every_conditional_line=True,
        prior_analysis_fixture=str(PARENT),prior_analysis_fixture_sha256=sha(PARENT.read_bytes()),
        original_scene_ROM_all101_commands_andcontroller_inputs_preserved=True,new_credit=0)
    save(output,doc)
    save(ROOT/'B81_actual_branch_scope_v2.json',dict(findings=findings,observed_complete_ordered_calls=49,unvisited_conditional_speeches=2,
        original_scene_commands_copied=101,all51_source_speeches_still_editorially_andnative_reviewed=True,
        no_repeat_playthrough_roster_override_ornew_ROM=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PARENT,PACKET,REBUILT,TERMINAL,Path(terminal['observer']),Path(__file__)]}))
    print('Bound actual49-speech B81 branch;two original conditional asides explicitly unvisited. All51 offline reviews and101 copied commands preserved.')
