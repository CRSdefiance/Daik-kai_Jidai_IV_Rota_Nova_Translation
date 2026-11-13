"""Source-lock independent production reconstruction to the seven exact native scopes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_reconstruction_tools_v8832');assert not root.exists()
    old="""    require(group['block'] in [31,53],'exact two-block scope')
    number=group['block'];count=2 if number==31 else 1
    require(len(rows)==count and not group['choice_commands'],'complete source speech/no-menu scope')
    require(len(packet['all_current_commands'])==9 and len(group['all_target_commands'])==9,'complete9command block')
    require(sum(c['word'] in [0x8000,0x8100] for c in packet['all_current_commands'])==(1 if number==31 else 0) and not any(c['word']==0x2100 for c in packet['all_current_commands']),'complete original query/no-menu scope')
    require([(c['offset'],c['whole_command_hex'],c['native_extent']) for c in packet['all_current_commands'] if c['word']==0]==[(192 if number==31 else 132,'00000000',4)],'complete original normal end')
    require([(c['offset'],c['whole_command_hex'],c['native_extent']) for c in group['all_target_commands'] if c['word']==0]==[(224 if number==31 else 150,'00000000',4)],'complete target normal end')"""
    new="""    scopes={54:(4,7,0,136,122,0),55:(1,3,0,100,110,0),56:(3,7,0,188,220,0),57:(8,11,0,214,234,0),58:(49,98,6,2488,2876,24),59:(7,14,0,518,608,0),60:(10,12,0,720,800,0)}
    require(group['block'] in scopes,'exact seven-block scope')
    number=group['block'];count,commands,queries,source_end,target_end,relative_sites=scopes[number]
    require(len(rows)==count and not group['choice_commands'],'complete source speech/no-menu scope')
    require(len(packet['all_current_commands'])==commands and len(group['all_target_commands'])==commands,'complete native command block')
    require(sum(c['word'] in [0x8000,0x8100] for c in packet['all_current_commands'])==queries and not any(c['word']==0x2100 for c in packet['all_current_commands']),'complete original query/no-menu scope')
    require([(c['offset'],c['whole_command_hex'],c['native_extent']) for c in packet['all_current_commands'] if c['word']==0]==[(source_end,'00000000',4)],'complete original normal end')
    require([(c['offset'],c['whole_command_hex'],c['native_extent']) for c in group['all_target_commands'] if c['word']==0]==[(target_end,'00000000',4)],'complete target normal end')"""
    receipt=derive('dk4tool/patch/hodram_B31_B53_reconstruction_v1.py','dk4tool/patch/hodram_B54_B60_reconstruction_v1.py',{
        'Hodram B31/B53 reconstruction:':'Hodram B54-B60 reconstruction:',old:new,
        "len(selected)==len(group['relative_fixups'])==(4 if group['block']==31 else 0)":"len(selected)==len(group['relative_fixups'])==relative_sites",
    })
    validation=derive('scripts/validate_Hodram_B31_B53_reconstruction_v8752.py','scripts/validate_Hodram_B54_B60_reconstruction_v8833.py',{
        'hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_reconstruction_v1':'hodram_B54_B60_reconstruction_v1',
        'Hodram_B31_B53_reconstruction_validation_v8752':'Hodram_B54_B60_reconstruction_validation_v8833',
        'translations/hodram_B31_B53_editorial_manuscript_v5.json':'translations/hodram_B54_B60_editorial_manuscript_v4.json',
        'Hodram_B31_B53_references_v8738':'Hodram_B54_B60_references_v8814',
        'Hodram_B31_B53_current_v8722':'Hodram_B54_B60_current_v8799',
        'Hodram_B31_B53_source_controls_v8718':'Hodram_B54_B60_source_controls_v8791',
        'Hodram_B31_B53_independent_v8734':'Hodram_B54_B60_independent_v8810',
        'Hodram_B31_B53_reference_v8736':'Hodram_B54_B60_reference_v8812',
        '53 if number==31 else 31':'60 if number!=60 else 54','if number==31:':'if number==58:',
        'dict(block=53,offset=8)':'dict(block=number,offset=8)',
        'if a!=b]==[31,53]':'if a!=b]==list(range(54,61))',
        'for i in [31,53]:':'for i in range(54,61):',
        "len(positives)==2 and len(cases)==51 and len({(c['block'],c['label']) for c in cases})==51":"len(positives)==7 and len(cases)==161 and len({(c['block'],c['label']) for c in cases})==161",
        'complete18commands3preambles4relatives_query8opaquecontrols_fullends_separate_tail_andallinverses_preserved':'complete152commands82preambles24relatives6queries33nonprosecontrols_fullends_separate_tails_andallinverses_preserved',
        'Production reconstruction:2blocks/wholearchive/wholeNDS equalindependent reviewedreference;51changed semantic defects reject withfrozen guardsactive. No ROMcommit orcredit.':'Production reconstruction:7blocks/wholearchive/wholeNDS equalindependent reviewedreference;161changed semantic defects reject withfrozen guardsactive. No ROMcommit orcredit.',
    })
    mapping=read('work/analysis/Hodram_B54_B60_references_v8814/source_current_final_map.json')
    assert [(g['block'],len(g['text_records']),len(g['all_current_commands']),g['all_current_commands'][-1]['offset'],g['all_target_commands'][-1]['offset'],len(g['relative_fixups'])) for g in mapping['groups']]==[(54,4,7,136,122,0),(55,1,3,100,110,0),(56,3,7,188,220,0),(57,8,11,214,234,0),(58,49,98,2488,2876,24),(59,7,14,518,608,0),(60,10,12,720,800,0)]
    root.mkdir(parents=True);save(root/'source_locked_production_reconstruction.json',dict(module=receipt,validation=validation,
        all_source_owned_sparse_inverse_relative_mapping_separate_tails_cachebounds_andfull_opcode_guards_preserved=True,
        native_scope_counts_andboth_end_locations_bound_to_completed_independent_map=True,
        validation_expected_count=161,base_cases_per_block=21,relative_extra_cases_for_B58=8,invented_relative_case_other_blocks=1,
        new_credit=0,no_ROM_registry_orledger_change=True,full_goal_complete=False))
