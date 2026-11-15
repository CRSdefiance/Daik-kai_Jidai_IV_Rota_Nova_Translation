"""Retain independent original command parsing and complete inverse guards for82 references."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_reference_tools_v8835');assert not root.exists()
    module=derive('dk4tool/patch/hodram_B31_B53_references_v1.py','dk4tool/patch/hodram_B54_B60_references_v1.py',{
        'both complete blocks independently.':'all seven complete blocks independently.',
        'hodram_B31_B53_reconstruction_v1':'hodram_B54_B60_reconstruction_v1',
        '[31,53]':'[54,55,56,57,58,59,60]',
        'exact owned two-block scope':'exact owned seven-block scope','complete ordered two-block source groups':'complete ordered seven-block source groups',
        "len(group['command_map'])==9 and len(cleantexts)==len(oldtexts)==len(texts)==len(rows)==(2 if number==31 else 1)":"len(group['command_map'])=={54:7,55:3,56:7,57:11,58:98,59:14,60:12}[number] and len(cleantexts)==len(oldtexts)==len(texts)==len(rows)=={54:4,55:1,56:3,57:8,58:49,59:7,60:10}[number]",
        'all9commands andcomplete speech membership':'complete native command andspeech membership',
        '(4 if number==31 else 0)':'(24 if number==58 else 0)','(20 if number==31 else 0)':'(120 if number==58 else 0)',
        "len(allrefs)==len(doc['records'])==3 and len({r['id'] for r in allrefs})==3":"len(allrefs)==len(doc['records'])==82 and len({r['id'] for r in allrefs})==82",
        'three disjoint source identities andcomplete batch coverage':'82 disjoint source identities andcomplete batch coverage',
        'all323 other blocks unchanged':'all318 other blocks unchanged',
        'editorial_references=3,speeches=3':'editorial_references=82,speeches=82',
        'commands=18,relative_sites=4,query_sites=1,unowned_blocks=323':'commands=152,relative_sites=24,query_sites=6,unowned_blocks=318',
    })
    validation=derive('scripts/validate_Hodram_B31_B53_references_v8756.py','scripts/validate_Hodram_B54_B60_references_v8836.py',{
        'hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_references_v1':'hodram_B54_B60_references_v1',
        'review_Hodram_B31_B53_actual_v8744':'review_Hodram_B54_B60_actual_v8825',
        "ROOT=Path('work/analysis/Hodram_B31_B53_reference_validation_v8756')":"PROOFS={**PROOFS,'relocation':'work/analysis/Hodram_B54_B60_references_v8814/source_current_final_map.json','current':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json','source_controls':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json'}\nROOT=Path('work/analysis/Hodram_B54_B60_reference_validation_v8836')",
        'translations/hodram_B31_B53_editorial_manuscript_v5.json':'translations/hodram_B54_B60_editorial_manuscript_v4.json',
        'B31/B53 production references:':'B54-B60 production references:',
        'Frozen Hodram-B31-B53 contract changed':'Frozen Hodram-B54-B60 contract changed',
        "{31,53} and result['summary']['editorial_references']==3 and result['summary']['commands']==18 and result['summary']['unowned_blocks']==323":"set(range(54,61)) and result['summary']['editorial_references']==82 and result['summary']['commands']==152 and result['summary']['unowned_blocks']==318",
        "nested=next(i for i,c in enumerate(data['relocation']['groups'][0]['all_target_commands'])":"nested=next(i for i,c in enumerate(data['relocation']['groups'][4]['all_target_commands'])",
        "['groups'][0]['all_target_commands'][nested]":"['groups'][4]['all_target_commands'][nested]",
        "query=next(i for i,c in enumerate(data['relocation']['groups'][0]['all_target_commands'])":"query=next(i for i,c in enumerate(data['relocation']['groups'][4]['all_target_commands'])",
        "['groups'][0]['all_target_commands'][query]":"['groups'][4]['all_target_commands'][query]",
        '    assert len(cases)==20 and':"    for ident in ['DK4_MES_B56_R0010','DK4_MES_B57_R0007','DK4_MES_B55_R0006','DK4_MES_B59_R0023','DK4_MES_B60_R0012']:\n        index=next(i for i,r in enumerate(doc['records']) if r['id']==ident)\n        reject(ident+':distinct-consumer-final-offset',lambda d,i=index:d['doc']['records'][i]['final_reference'].__setitem__('offset',d['doc']['records'][i]['final_reference']['offset']+1))\n    assert len(cases)==25 and",
        "len({r['label'] for r in cases})==20":"len({r['label'] for r in cases})==25",
        'positive_complete18command_native_inventories_and3disjoint_source_current_final_references':'positive_complete152command_native_inventories_and82disjoint_source_current_final_references',
        'positive_entire_archive_whole_reference_ROM_all323_unownedblocks_files_components_andallinverses':'positive_entire_archive_whole_reference_ROM_all318_unownedblocks_files_components_andallinverses',
        'negative_count=20':'negative_count=25',
        'Independent production references:all18commands/3canonical source-current-final refs/wholearchive/wholeNDS andinverses pass;20semantic defects reject withzero mutation.No ROMcommit orcredit.':'Independent production references:all152commands/82canonical source-current-final refs/wholearchive/wholeNDS andinverses pass;25semantic defects reject withzero mutation.No ROMcommit orcredit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_references.json',dict(module=module,validation=validation,all_independent_original_parser_source_current_final_fullpreamble_command_relative_terminal_archive_unowned_component_wholeimage_andinverse_guards_preserved=True,distinct_FE_FI_FA_multipage_andfinalblock_reference_challenges_added=True,new_credit=0,full_goal_complete=False))
