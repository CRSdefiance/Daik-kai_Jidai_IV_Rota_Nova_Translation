"""Prepare resized storage while preserving the complete mixed-predicate prefix."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_relocation_tools_v5377')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B190_relocation_v5328.py','scripts/research_lil_B191_relocation_v5377.py',{
        'B190':'B191','relocation_v5328':'relocation_v5377','editorial_manuscript_v3':'editorial_manuscript_v4','combined_v5304':'combined_v5346',
        'Relocate all17':'Relocate all13','one500 RNG predicate':'three500/700/500 RNG predicates','six relative sites':'16 relative sites','three alternative A000s':'four alternative A000s',
        'len(source)==608 and old_end==606':'len(source)==736 and old_end==734',"len(spec['all_current_native_commands'])==29":"len(spec['all_current_native_commands'])==38",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==17":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==13",
        "sum(c['word']==0x8000 for c in spec['all_current_native_commands'])==1":"sum(c['word']==0x8000 for c in spec['all_current_native_commands'])==3",
        "sum(c['word']==0xA000 for c in spec['all_current_native_commands'])==3":"sum(c['word']==0xA000 for c in spec['all_current_native_commands'])==4",
        'number==190':'number==191','==[602]':'==[730]',"sum(len(r['text_records']) for r in results)==17":"sum(len(r['text_records']) for r in results)==13",
        "sum(len(r['command_map']) for r in results)==29":"sum(len(r['command_map']) for r in results)==38",'not in [190]':'not in [191]',
        'all17speech':'all13speech','all6_source_relative_sites_and30_native_skip_cases':'all16_source_relative_sites_and80_native_skip_cases',
        'and6_nonrelative_leaves':'and9_nonrelative_leaves','29structural commands/17speech':'38structural commands/13speech','30 target cases':'80 target cases',
    })]
    rows.append(derive('scripts/prove_lil_B190_stored_v5329.py','scripts/prove_lil_B191_stored_v5378.py',{
        'B190':'B191','stored_v5329':'stored_v5378','editorial_manuscript_v3':'editorial_manuscript_v4','relocation_v5328':'relocation_v5377','voices_v5315':'voices_v5357',
        '[119,159,254]':'[86,154,254]','len(cases)==17':'len(cases)==13','fresh+reused==68':'fresh+reused==52',
        'all17':'all13','targets68_macro':'targets52_macro','current_final_stored_macro_alignment_cases=68':'current_final_stored_macro_alignment_cases=52',
        'stored_targets=17,progressive=16':'stored_targets=13,progressive=12','macro_cases=68':'macro_cases=52',
        'predicate_three_alternatives':'three_predicates_four_alternatives_and_no_effect_paths',
    }))
    ROOT.mkdir(parents=True)
    font=Path('work/analysis/lil_B191_fonts_v5374b/all13_progressive_FE_native_planes_and104_alignment_cases.json')
    save(ROOT/'viewed_layout_retention_reasons.json',dict(native_font_proof=str(font),native_font_proof_sha256=sha(font.read_bytes()),
        all13_panels_on_two_native_sheets_viewed_after_image_return=True,
        retained_layouts=[dict(id='DK4_MES_B191_R0056',reason='Two substantial rows preserve the confirming tag,immediate-purchase condition and complete competing-shop buyout warning.'),
            dict(id='DK4_MES_B191_R0064',reason='Exact source/prose-bound ordinary wrap after be retains the whole question on the first row and uses two substantial rows without changing any word.'),
            dict(id='DK4_MES_B191_R0068',reason='Two substantial rows preserve the relaxed assertion and rhetorical sellout doubt. No isolated final word or extra page.'),
            dict(id='DK4_MES_B191_R0072',reason='Two substantial rows keep the explicit contradiction,popularity claim and rapid-depletion prediction complete.'),
            dict(id='DK4_MES_B191_R0088',reason='Three full rows preserve the cajoling request,condition of obtaining this color and character profit assurance. No kinship or joint ownership is introduced;no wording was shortened for width.')],
        no_new_completion_credit=True,full_goal_complete=False))
    save(ROOT/'prepared_complete_relocation_and_stored_checks.json',dict(tools=rows,source_stored=736,source_logical=734,source_tailzeros=2,
        commands=38,speeches=13,progressive=12,FE=1,predicates=3,relative_sites=16,effects=4,expected_target_skip_cases=80,
        expected_stored_alignment_cases=52,all_extents_to_be_measured=True,no_credit=True,full_goal_complete=False))
