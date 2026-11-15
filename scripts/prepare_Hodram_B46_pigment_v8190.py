"""Bind original4800 rather than reuse B50's distinct4821 picture-layout assumption."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B46_pigment_tools_v8190')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/bind_Rafael_B50_pigment_v8134.py','scripts/bind_Hodram_B46_pigment_v8190.py',{
        'Rafael_B50_pigment_v8134':'Hodram_B46_pigment_v8190',
        'Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json':'Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json',
        'Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json':'Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json',
        'current_V8122_Rafael_native_v8125':'current_V8172_Hodram_native_v8187',
        "gloss['source_packet_sha256']":"gloss['source_packets']['46']['sha256']",
        "gloss['source_only_no_current_B50_English_exposed_no_localized_manuscript']":"gloss['source_only_no_current_body_orname_comparison_no_localized_manuscript']",
        "c['offset']==244 and c['whole_command_hex']=='2148b5a8'":"c['offset']==140 and c['whole_command_hex']=='0048b5a8'",
        "request['layout']==[2,0,1]":"request['layout']==[0,0,0]",
        'original_descriptor_category0_index181_andlayout2_0_1':'original_descriptor_category0_index181_andlayout0_0_0',
        'original4821_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json':'original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json',
        'original4821:descriptor[0,181,1,5]/layout[2,0,1]':'original4800:descriptor[0,181,1,5]/layout[0,0,0]',
        '0x4821':'0x4800','B50':'Hodram_B46',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared Hodram original4800 descriptor/RedDye identity proof;fresh distinct layout test required.')
