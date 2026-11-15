"""Prepare six-name,70-dispatch andcomplete clean-exchange source tools."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    pairs=[]
    def generate(old,new,changes):
        old,new=Path(old),Path(new);assert not new.exists();t=old.read_text(encoding='utf-8')
        for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
        return old,new,t
    shared={'work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json':'work/analysis/lil_remaining_B135_B140_source_v3345b/next35_B135_B136_clean_current_context.json'}
    old,new,t=generate('scripts/reconcile_lil_B131_B133_voices_v3307b.py','scripts/reconcile_lil_B135_B136_voices_v3346b.py',{**shared,
      'lil_B131_B133_voices_v3307b':'lil_B135_B136_voices_v3346b',
      'chosen==[0,2,5,9,20]':'chosen==[2,9,14,36,47,96]',
      '::five_names':'::six_names','current_five_static_names_voices_selector00_and207_catalog_rebind':'current_six_static_names_voices_and207_catalog_rebind',
      'fresh_five_actor_names':'fresh_six_actor_names','source00_is_static_actor0_not_empty_text_or_dynamic_role=True':'no_source00_orFE_speeches_in_selected35=True',
      'FE_identity_and_null_actor_macro_dispatch_still_require_separate_proof=True':'all35_progressive_dispatches_still_require_separate_proof=True'})
    t=t[:t.rindex("    print('Five")]+"    print('Six current static names/voices pass;207catalog rebound byexact runtime/data. No rolefixtures,newnameplates orreviewcredit.')\n    print({r['actor_ID']:r['current_catalog_name'] for r in fresh['rows']})\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=generate('scripts/prove_lil_B131_B133_controls_v3308b.py','scripts/prove_lil_B135_B136_controls_v3347.py',{**shared,
      'lil_B131_B133_controls_v3308b':'lil_B135_B136_controls_v3347',
      'lil_B131_B133_voices_v3307b':'lil_B135_B136_voices_v3346b',
      'len(cases)==122 and sum(c[\'source_selector\']==254 for c in cases)==2':'len(cases)==70 and sum(c[\'source_selector\']==254 for c in cases)==0',
      'len(predicates)==5':'len(predicates)==1',"{'FI':6,'FA':0,'FO':1}":"{'FI':0,'FA':0,'FO':1}",
      "for c in cases)==36":"for c in cases)==0",'statics==[0,2,5,9,20]':'statics==[2,9,14,36,47,96]',
      'all61_source_current_dispatch_selector00_FE_and5_predicates':'all35_source_current_dispatches_and1_predicate',
      'all61_complete_preambles_have122_current_code_source_and_current_dispatch_cases':'all35_complete_preambles_have70_current_code_source_and_current_dispatch_cases',
      'all2_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback=True':'no_source_FE_speeches=True',
      'all5_original_predicates_preserve_source_operands_results_and_unowned4MiB':'all1_original_predicate_preserves_source_operands_results_and_unowned4MiB',
      'source00_is_static_actor0_Rafael_Castor_without_role_assignment=True':'all_six_selectors_static_without_role_assignment=True',
      'no_source2000_commands_in_next63_scope':'no_source2000_commands_in_next35_scope',
      'actual_selected_B131_B133_IDs':'actual_selected_B135_B136_IDs'})
    t=t[:t.rindex('    print(')]+"    print('70current-code source/current progressive dispatches,FO1 andone native predicate pass. No rolefixtures,newgameplay orreviewcredit;context/prose/display/release pending.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=generate('scripts/prepare_lil_B131_B133_clean_review_v3309.py','scripts/prepare_lil_B135_B136_clean_review_v3348.py',{**shared,
      'lil_B131_B133_clean_transcripts_v3309':'lil_B135_B136_clean_transcripts_v3348',
      'lil_B131_B133_branches_v3309b':'lil_B135_B136_branches_v3348b',
      'full_commands=112,source_speeches=61,typed_labels=2,all18_zero_selector_bodies_preserved_with_complete_preambles=True':'full_commands=61,source_speeches=35,typed_labels=0,all35_complete_source_preambles_preserved=True',
      'complete_clean_transcript_blocks=[131,133],source_speeches=61,labels=2,commands=112':'complete_clean_transcript_blocks=[135,136],source_speeches=35,labels=0,commands=61'})
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    root=Path('work/analysis/lil_B135_B136_native_tools_v3346');root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
