"""Bind the already validated original style11 caller to both B208 source names."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_name_tools_v6405')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/prove_lil_B207_name_planes_v6354d.py','scripts/prove_lil_B208_name_planes_v6405.py',{
        'Measure full-width-F compatibility and complete current names;never normalize name bytes.':'Measure both complete B208 source names and original style11 actual header pixels.',
        'name_planes_v6354d':'name_planes_v6405','current_V6327_native_v6337':'current_V6380_native_v6389',
        'lil_B207_source_names_v6341':'lil_B208_source_names_v6393','lil_B207_source_actual_v6347':'lil_B208_source_actual_v6399',
        'all13_source_speeches_all24_commands_and_complete_return.json':'all24_source_panels_all38_commands_and_observed_return.json',
        '[2,14]':'[7,170]',"['Ｆerog','Emilio Ｆerog','Ferog','Emilio Ferog']":"['Cristina','Erneco','Cristina Erneco','Mysterious Old Man']",
        " for c in cases if 'Ｆ' in c['input_text']":" for c in cases",
        "{2:'Lil Argot',14:'Emilio Ｆerog'}":"{7:'Cristina Erneco',170:'Mysterious Old Man'}",
        'current_fullwidth_F_literal_outputs_exact':'current_all_source_name_literals_exact','plain_ASCII_F_literal_output_comparisons_measured_not_assumed':'all_ASCII_source_name_literal_outputs_measured_not_assumed',
        'pic.crop((8,272,120,291))':'pic.crop((8,272,160,291))','actual_strip.resize((448,76)':'actual_strip.resize((608,76)',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_name_proof.json',dict(tool=r,original_style11_helper='scripts/lil_B207_name_style_v6354d.py',original_style_helper_reused_without_new_name_byte_or_caller_assumption=True,full_goal_complete=False));print('B208 two-name proof prepared;original source-bound style11 helper and all native constants retained.')
