"""Derive a production comparison reader retaining long divergence and focused agreement."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root=Path('work/analysis/Hodram_B52_comparison_tools_v8684');assert not root.exists()
    source=Path('dk4tool/patch/hodram_B51_comparison_v1.py').read_text(encoding='utf-8')
    line=next(line for line in source.splitlines() if "require(declared['source_has_no_picture_orhide_sites']" in line)
    changes={
        'B51':'B52',
        "comparison=data['comparison'];require(len(comparison['groups'])==1,'one complete B51 exchange comparison')": "comparison=data['comparison'];require(len(comparison['groups'])==2 and len(data['focus_comparison']['groups'])==1,'two long path comparisons andone focused withdrawal comparison')",
        "for choice,declared in zip(['whole'],comparison['groups'],strict=True):": "for choice,declared in zip(['withdrawal','opposition','withdrawal-postreturn-focus'],comparison['groups']+data['focus_comparison']['groups'],strict=True):",
        'number=51':'number=52',
        "require(declared['block']==number and (choice=='whole' or declared['choice']==choice),'exact paired B51 comparison membership');groups=data['actual']['groups'] if choice=='whole' else [g for g in data['tail_actual']['groups'] if g['choice']==choice];old,new=groups": "require(declared['block']==number and declared['case']==choice and declared['ordinary_menu_selection']==(1 if choice=='opposition' else 0),'exact paired B52 comparison membership');groups=data[{'withdrawal':'actual','opposition':'opposition_actual','withdrawal-postreturn-focus':'focus_actual'}[choice]]['groups'];old,new=groups\n        return_key='script_return' if choice=='opposition' else 'normal_return'",
        "declared['normal_returns']==[g['normal_return'] for g in groups]": "declared['script_returns']==[g[return_key] for g in groups]",
        "max(g['normal_return']['frame'] for g in groups)": "max(g[return_key]['frame'] for g in groups)",
        line: "        require(declared['source_has_no_picture_orhide_sites'] and declared['unvisited_conditional_text_IDs']==old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']==['DK4_MES_B52_R0021' if choice=='opposition' else 'DK4_MES_B52_R0033'],'exact case-specific selected andunvisited source membership')",
        "require(unequal==[],'all measured script-boundary PRNG differences preserved')": "require(unequal==([68,104,108,174,178,200,208,216,224] if choice=='opposition' else [68,104,112,164,166]),'all measured menu-andlater script-boundary PRNG differences preserved')",
        "require(total_rgb==89 and [s['later_RGB_samples'] for s in summaries]==[89] and all(s['final_captain_IDs']==[1,1] for s in summaries),'89laterRGBpairs andboth initialized Hodram captain1 tails')": "require(total_rgb==199 and [s['later_RGB_samples'] for s in summaries]==[93,93,13] and all(s['final_captain_IDs']==[1,1] for s in summaries),'199laterRGBpairs andall initialized Hodram captain1 contexts')",
        "proof['total_actual_frames']==20002": "proof['total_actual_frames']==40004 and data['focus_comparison']['total_actual_frames']==10402",
        "for sheet in proof['review_sheets']:": "for sheet in proof['review_sheets']+data['focus_comparison']['review_sheets']:",
        "[g['later_RGB_differences'] for g in result['groups']]==[3] and [g['duration_differences'] for g in result['groups']]==[2]": "[g['later_RGB_differences'] for g in result['groups']]==[46,13,0] and [g['duration_differences'] for g in result['groups']]==[1,1,1]",
        'all three laterRGB differences andtwo command-duration differences retained':'all long/focused laterRGB differences andeach original menu-duration difference retained',
        "[list(map(int,['2294662370','3116913577']))]": "[list(map(int,pair)) for pair in [['2571928604','1941737819'],['1611048932','1190801271'],['613908813','613908813']]]",
        'unequal final PRNG retained despiteequal source-script boundary values without future-outcome inference':'all unequal long-run andequal focused final PRNG retained without future-outcome inference',
        'all_source_qualified_query_branch_path_andunvisited_Charles_scope_checked=True':'all_source_qualified_both_choice_paths_andcase_specific_unvisited_scope_checked=True',
    }
    receipt=derive('dk4tool/patch/hodram_B51_comparison_v1.py','dk4tool/patch/hodram_B52_comparison_v1.py',changes)
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=receipt,
         existing_final_RAM_native_component_queries_and199_whole_RGB_pairs_independent=True,
         all_long_withdrawal_divergence_andfocused_agreement_retained=True,
         no_new_capture_orold_comparison_producer_replay=True))
