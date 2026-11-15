"""Freeze twenty logical paragraphs against exact three-role progressive and FE consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B195_native_tools_v5551')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B195_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
          'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B195_profile.py');assert not profile.exists()
    text='''"""Exact B195 cheese-specialty source/current native profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({92,103,119})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B195 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B195 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=40 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All20 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B195 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B195-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';19 original54020 speeches,Barkeep92/Patron103/PortWorker119 voice0,six original readonly names.23 linear commands,A0008,C200704,end706,two source tailzeros. Current V5531 font/guards;fresh approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B195-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C prospective Cheese/Veracruz notice.228x48logical/228x64physical,conservative216px planning. Cheese8 and both Veracruz aliases unchanged;unnamed house specialty and character popularity prediction,not narrator fact or earned fashion;fresh approval required.')
    raise ValueError('Unknown B195 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B193_layout_v1.py','dk4tool/dialogue/lil_B195_layout_v1.py',{
        'B193':'B195','frozenset({166,167,168})':'frozenset({92,103,119})'})]
    rows.append(derive('scripts/plan_lil_B193_layout_v5458.py','scripts/plan_lil_B195_layout_v5552.py',{
        'B193':'B195','layout_v5458':'layout_v5552','Plan15':'Plan20','all15':'all20','len(reports)==15':'len(reports)==20','plans=15':'plans=20'}))
    rows.append(derive('scripts/verify_lil_B193_fonts_v5459.py','scripts/verify_lil_B195_fonts_v5553.py',{
        'B193':'B195','fonts_v5459':'fonts_v5553','voices_v5448':'voices_v5542','blocks[193]':'blocks[195]','blocks[192]':'blocks[194]',
        '[166,167,168,254]':'[92,103,119,254]','167 if selector==166 else 166':'103 if selector==92 else 92',
        "r['source_selector']==166":"r['source_selector']==92","b'\\xa6Japanese','{SPEAKER:A6}Hello.'":"b'\\x5cJapanese','{SPEAKER:5C}Hello.'",
        'len(cases)==len(qa_reports)==15':'len(cases)==len(qa_reports)==20','and120 native':'and160 native',
        'macro_calls==120':'macro_calls==160','and120_alignment':'and160_alignment','alignment_calls=120':'alignment_calls=160',
        'progressive_alignment_calls=112':'progressive_alignment_calls=152','complete_progressive_planes=14':'complete_progressive_planes=19',
        'all15':'all20','All15':'All20','120 alignment cases':'160 alignment cases','two sheets need':'three sheets need'}))
    rows.append(derive('scripts/approve_lil_B193_native_v5460.py','scripts/approve_lil_B195_native_v5554.py',{
        'B193':'B195','native_approval_v5460':'native_approval_v5554','fonts_v5459':'fonts_v5553',
        "len(font['cases'])==15":"len(font['cases'])==20","font['current_original_macro_alignment_calls']==120":"font['current_original_macro_alignment_calls']==160",
        'and120_alignment':'and160_alignment','==(14,1)':'==(19,1)',"len(font['review_sheets'])==2":"len(font['review_sheets'])==3",
        'blocks[193]':'blocks[195]',"{'revise':8,'retain-wording':7}":"{'revise':3,'retain-wording':17}","('progressive',166)":"('progressive',92)",
        'all15':'all20','All15':'All20','viewed15-panel':'viewed20-panel','on_two_sheets':'on_three_sheets',
        'eight_revisions_and_seven_individually_justified_retentions':'three_revisions_and_seventeen_individually_justified_retentions',
        'source_cooking_price_concern_reported_spice_classification_teaching_offer_and_explicit_friendship_preserved':
        'source_unnamed_cheese_specialty_coaxing_two_chewing_beats_spreading_word_intention_and_character_popularity_claim_preserved',
        'all120_current_native':'all160_current_native','8 revisions/7 justified retentions,120 alignments,20 consumer':
        '3 revisions/17 justified retentions,160 alignments,20 consumer'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_source_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_three_roles23_linear_commands_no_macros_and_six_readonly_names_bound=True,no_inherited_boundary_exception=True,
        no_manual_break_or_font_width_metric_guard_change=True,no_credit=True,full_goal_complete=False))
