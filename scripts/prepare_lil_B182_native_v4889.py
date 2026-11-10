"""Freeze exact B182 controls and reuse unchanged measured display geometry."""
from pathlib import Path
import re
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B182_native_tools_v4889')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B182_editorial_manuscript_v1.json');source=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof','current_C200_source_ownership_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    for p in [Path('work/analysis/lil_B182_predicate500_v4883/all16_original500_predicate_RNG_ownership_cases.json'),
              Path('work/analysis/lil_B182_C200_v4883/source_fleet_descriptor_two_C200_contracts.json')]:
        assert read(p)['source_context_sha256']==doc['source_context_sha256'];deps[str(p)]=sha(p.read_bytes())
    hashes=sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    original=Path('dk4tool/dialogue/lil_B180_profile.py').read_text(encoding='utf-8')
    a=original.index('ARM9_SHA=');b=original.index('\ndef profile_for',a)
    text=original[:a]+'ARM9_SHA='+repr(source['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({166,167})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n'+original[b:]
    changes={
        'B180':'B182','ten progressive speeches':'seven progressive speeches','len(cases)!=22':'len(cases)!=16',
        'All eleven source/current dispatch pairs required':'All eight source/current dispatch pairs required',
        ';ten original54020 speeches,Lady166/Lady167,four read-only name paths. No inferred noble rank,marriage or third-person gender.28 commands,ten relative sites,two original500 threshold/RNG predicates,three alternative opaque effects,C200570,end572. Current V4766 font and guards;native planes still need fresh approval.':
        ';seven original54020 speeches,Lady166/Lady167,four read-only name paths. Source-explicit princess,duke and his son;no guessed personal names,marriage date or gemstone identity.25 commands,ten relative sites,two original500 threshold/RNG predicates,three alternative opaque effects,C200630,end632. Current V4867 font and guards;native planes still need fresh approval.',
        ';one prospective Lisbon Scents-category notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs fresh approval.':
        ';one prospective London Gems-category notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs fresh approval.'}
    for k in changes:assert k in text,k
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    profile=Path('dk4tool/dialogue/lil_B182_profile.py');assert not profile.exists();compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B180_layout_v1.py','dk4tool/dialogue/lil_B182_layout_v1.py',{'B180':'B182'})]
    tools.append(derive('scripts/plan_lil_B181_layout_v4843.py','scripts/plan_lil_B182_layout_v4890.py',{
        'B181':'B182','layout_v4843':'layout_v4890','Plan10':'Plan8','all10_paragraph':'all8_paragraph','len(reports)==10':'len(reports)==8','plans=10':'plans=8'}))
    tools.append(derive('scripts/verify_lil_B180_fonts_v4794.py','scripts/verify_lil_B182_fonts_v4891.py',{
        'B180':'B182','fonts_v4794':'fonts_v4891','voices_v4775':'voices_v4879',
        'len(cases)==len(qa_reports)==11 and macro_calls==88':'len(cases)==len(qa_reports)==8 and macro_calls==64',
        'blocks[180]':'blocks[182]','blocks[179]':'blocks[181]',
        'all11_progressive_FE_native_planes_and88_alignment_cases':'all8_progressive_FE_native_planes_and64_alignment_cases',
        'current_original_macro_alignment_calls=88,progressive_alignment_calls=80':'current_original_macro_alignment_calls=64,progressive_alignment_calls=56',
        'complete_progressive_planes=10':'complete_progressive_planes=7',
        '11 current-font native planes,88 alignment cases and18':'8 current-font native planes,64 alignment cases and18',
        'planes and88 native alignment cases':'planes and64 native alignment cases',
        'two sheets need visual review':'one sheet needs visual review'}))
    tools.append(derive('scripts/approve_lil_B181_native_v4845.py','scripts/approve_lil_B182_native_v4892.py',{
        'B181':'B182','native_approval_v4845':'native_approval_v4892','fonts_v4844':'fonts_v4891',
        'all10_progressive_FE_native_planes_and80_alignment_cases':'all8_progressive_FE_native_planes_and64_alignment_cases',
        "len(font['cases'])==10":"len(font['cases'])==8","font['current_original_macro_alignment_calls']==80":"font['current_original_macro_alignment_calls']==64",
        '==(9,1)':'==(7,1)',"len(font['negative_controls'])==20":"len(font['negative_controls'])==18",'blocks[181]':'blocks[182]',
        "len(font['review_sheets'])==2":"len(font['review_sheets'])==1",
        "{'revise':5,'retain-wording':5}":"{'revise':6,'retain-wording':2}",
        'all10':'all8','all80':'all64','source_consumer_negatives=20':'source_consumer_negatives=18',
        'on_two_sheets':'on_one_sheet','five_revisions_and_five_individually_justified_retentions':'six_revisions_and_two_individually_justified_retentions',
        'explicit_wistful_wish_and_three_audible_sighs_refined':'reported_engagement_explicit_rank_and_son_ring_hyperbole_and_unknown_gem_joke_preserved',
        'viewed10-panel':'viewed8-panel','All10':'All8','5 revisions/5 justified retentions,80 alignments,20':'6 revisions/2 justified retentions,64 alignments,18'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),tools=tools,dependencies=deps,
        no_shared_metric_guard_phrase_exception_or_manual_break_change=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B182 exact profiles and eight-paragraph native tools prepared; source conditionals and unchanged geometry retained.')
