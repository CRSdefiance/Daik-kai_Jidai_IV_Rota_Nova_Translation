"""Prepare exact35-speech relocation andfinal native/loader/reference tools."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B135_B136_reference_tools_v3363');assert not root.exists();pairs=[]
    def make(a,b,changes):
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8')
        for x,y in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert x in t,x;t=t.replace(x,y)
        return old,new,t
    old,new,t=make('scripts/research_lil_B131_B133_relocation_v3329b.py','scripts/research_lil_B135_B136_relocation_v3363b.py',{
      'lil_B131_B133_relocation_v3329b':'lil_B135_B136_relocation_v3363b','lil_B131_B133_editorial_manuscript_v4':'lil_B135_B136_editorial_manuscript_v5',
      "MENU=Path('translations/lil_B131_B133_choice_manuscript_v5.json')":"MENU=None","doc,menu=map(read,[DOC,MENU])":"doc,menu=read(DOC),{'records':[]}",
      'all_routes_combined_v3300_candidate':'all_routes_combined_v3338_candidate',
      "b'\\0' not in value[1:] and (b'\\0' not in value or value[0]==old[0]==0)":"b'\\0' not in value",
      "for r in results)==61":"for r in results)==35","len(r['choice_commands']) for r in results)==1":"len(r['choice_commands']) for r in results)==0",
      "len(r['relative_skip_fixups']) for r in results)==24":"len(r['relative_skip_fixups']) for r in results)==4",
      "len(r['target_native_skip_cases']) for r in results)==120":"len(r['target_native_skip_cases']) for r in results)==20",
      "len(r['command_map']) for r in results)==112":"len(r['command_map']) for r in results)==61",
      '[131,133]':'[135,136]',"choices=str(MENU),choices_sha256=sha(MENU.read_bytes())":"choices=None,choices_sha256=None",
      'one_original2100_menu_two_labels=True':'no_original2100_objects=True',
      'all61speech_two_choice_labels_and24_relative_operands_preserved':'all35speech_and4_relative_operands_preserved',
      'all120_relocated_native_skip_cases_match_original_target_mapping':'all20_relocated_native_skip_cases_match_original_target_mapping',
      "whole_typed_speech_proof=doc['whole_typed_speech_proof'],whole_typed_speech_proof_sha256=doc['whole_typed_speech_proof_sha256'],all18_source00_prefixes_preserved_without_body_NUL=True,":"no_FE_source00_or_dynamic_objects=True,"})
    t=t[:t.rindex("    print('")]+"    print('61commands/35speeches/fourspans/20targetskipcases,inversebytes and334otherblocks exact. Research only.')\n";compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=make('scripts/prepare_lil_B131_B133_research_v3330b.py','scripts/prepare_lil_B135_B136_research_v3364.py',{
      'lil_B131_B133_research_v3330b':'lil_B135_B136_research_v3364','all_routes_combined_v3300_candidate':'all_routes_combined_v3338_candidate',
      'lil_B131_B133_V3300_derived_RESEARCH_ONLY':'lil_B135_B136_V3338_derived_RESEARCH_ONLY',
      'lil_B131_B133_relocation_v3329b':'lil_B135_B136_relocation_v3363b',
      'lil_B131_B133_native_approval_v3326/all63_native_macro_font_choice_and_source00_reconciliation':'lil_B135_B136_native_approval_v3360/all35_native_macro_font_and_source_reconciliation',
      'verify_lil_B131_B133_fonts_v3324b':'verify_lil_B135_B136_fonts_v3359b',
      'lil_B131_B133_fonts_v3324b':'lil_B135_B136_fonts_v3359',
      'all61speech_two_choice_labels_and24_relative_operands_preserved':'all35speech_and4_relative_operands_preserved',
      'all120_relocated_native_skip_cases_match_original_target_mapping':'all20_relocated_native_skip_cases_match_original_target_mapping',
      '[131,133]':'[135,136]','value[0] in [0,2,5,9,20,254]':'value[0] in [2,9,14,36,47,96]',
      'len(parity)==61 and macro_calls==244':'len(parity)==35 and macro_calls==140','len(menus)==1 and len(pauses)==0':'len(menus)==0 and len(pauses)==0',
      'all61_final_targets_complete_native_planes_equal_reviewed_planes':'all35_final_targets_complete_native_planes_equal_reviewed_planes',
      'current_final_padded_macro_alignment_cases=244':'current_final_padded_macro_alignment_cases=140',
      'all1_final2100_object_two_labels_and3_selection_cancel_cases_bound=True':'no2100_objects_in_source_scope=True',
      'all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved=True':'all35_final_speech_prefixes_and_nonempty_bodies_preserved=True',
      'all61_complete_source_static_or_FE_prefixes_preserved':'all35_complete_source_static_prefixes_preserved',
      'all1_FE_final_plane_and4_macro_alignments_bound=True':'no_FE_source00_or_dynamic_objects=True',
      'all60_progressive_final_planes_and240_macro_alignments_bound':'all35_progressive_final_planes_and140_macro_alignments_bound',
      'actual_selected_B131_B133_IDs':'actual_selected_B135_B136_IDs','V3300-derived':'V3338-derived'})
    t=t.replace('from scripts.verify_lil_B131_B133_FE_v3325 import expand as expand_FE\n','').replace('from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter\n','').replace('    paint_FE,FE_calibration=make_painter(image)\n','')
    t=t.replace("            isfe=value[0]==254","            isfe=False;assert value[0]!=254")
    a=t.index('            if isfe:\n');z=t.index('            assert len(pipeline',a)
    t=t[:a]+"""            pixels,events,fontmetrics=raster(arm,expanded)
            assert pixels==expected_pixels(arm,fontmetrics,events) and sha(pixels)==case['whole_native_plane_sha256']
            assert all(0<=e['y']<=48 and e['x']<=216 for e in events if e['code']==32)
            assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32)
"""+t[z:]
    t=t.replace('pipeline=ctx.execute(expand_FE,value[1:]) if isfe else ctx.execute(expand_progressive,value[1:],value[0])','pipeline=ctx.execute(expand_progressive,value[1:],value[0])')
    t=t.replace("current_FE_calibration=FE_calibration,",'')
    t=t[:t.rindex('    print(')]+"    print('Research image changesB135/B136 only;35final nativeplanes/140macro cases and334otherblocks/allotherfiles/components exact. Not a release ornewparent.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    for a,b,changes in [
      ('scripts/verify_lil_B131_B133_loader_v3331.py','scripts/verify_lil_B135_B136_loader_v3365.py',{'prepare_lil_B131_B133_research_v3330b':'prepare_lil_B135_B136_research_v3364','lil_B131_B133_loader_v3331':'lil_B135_B136_loader_v3365','B131/B133':'B135/B136'}),
      ('scripts/verify_lil_B131_B133_references_v3332.py','scripts/verify_lil_B135_B136_references_v3366.py',{'prepare_lil_B131_B133_research_v3330b':'prepare_lil_B135_B136_research_v3364','lil_B131_B133_reference_census_v3332':'lil_B135_B136_reference_census_v3366','lil_B131_B133_loader_v3331':'lil_B135_B136_loader_v3365','[131,133]':'[135,136]','==112':'==61','==24':'==4','==120':'==20','all112_':'all61_','24_relative_sites':'4_relative_sites','native_commands_each=112,relative_sites=24,target_native_skip_cases=120':'native_commands_each=61,relative_sites=4,target_native_skip_cases=20'})]:
        old,new,t=make(a,b,changes);compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=make('scripts/prove_lil_B131_B133_relocated_controls_v3333b.py','scripts/prove_lil_B135_B136_relocated_controls_v3367.py',{
      'prepare_lil_B131_B133_research_v3330b':'prepare_lil_B135_B136_research_v3364','lil_B131_B133_relocated_controls_v3333b':'lil_B135_B136_relocated_controls_v3367',
      'lil_B131_B133_editorial_manuscript_v4':'lil_B135_B136_editorial_manuscript_v5',
      'lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census':'lil_B135_B136_reference_census_v3366/all61_commands4_relative_sites_and_shipped_entry_census',
      'lil_B131_B133_fonts_v3324b':'lil_B135_B136_fonts_v3359',
      'len(dispatches)==61':'len(dispatches)==35',"for r in dispatches)==1":"for r in dispatches)==0",'len(predicates)==5':'len(predicates)==1',
      "assert sum(r['source_selector']==0 and r['resolved_actor_ID']==0 for r in dispatches)==18":"assert all(r['source_selector']==r['resolved_actor_ID'] for r in dispatches)",
      'all61_relocated_dispatches_source00_and5_predicate_pairs':'all35_relocated_dispatches_and1_predicate_pair',
      'all61_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text':'all35_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text',
      'all1_FE_preserves_original_null_actor_before_dynamic_fallback=True':'no_FE_source00_or_dynamic_objects=True',
      'all5_predicate_current_relocated_results_and_source_operands_equal':'all1_predicate_current_relocated_result_and_source_operands_equal',
      'all18_final_source00_speeches_are_static_Rafael0_without_role_assignment=True':'all_six_static_speaker_selectors_preserved_without_role_assignment=True',
      'actual_selected_B131_B133_IDs':'actual_selected_B135_B136_IDs'})
    t=t[:t.rindex('    print(')]+"    print('35relocated static dispatches/onepredicate pair pass;source operands/results/unownedRAM preserved. No selectedgameplay/release claim.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new));root.mkdir(parents=True)
    save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],allprevious_ROMs_and_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
