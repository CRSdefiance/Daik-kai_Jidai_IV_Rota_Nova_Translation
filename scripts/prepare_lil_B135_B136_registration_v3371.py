"""Prepare one registered manuscript stage andmeaningful compiler rejections."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/register_lil_B131_B133_v3337b.py');new=Path('scripts/register_lil_B135_B136_v3371b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    t=t.replace('all-routes-unified-v3338','__NEW__').replace('all-routes-unified-v3300','all-routes-unified-v3338').replace('__NEW__','all-routes-unified-v3372')
    changes={
      'lil_B131_B133_editorial_manuscript_v5':'lil_B135_B136_editorial_manuscript_v6',
      "MENU=Path('translations/lil_B131_B133_choice_manuscript_v6.json')":"MENU=None",'lil_B131_B133_registration_v3337b':'lil_B135_B136_registration_v3371b',
      'all_routes_combined_v3300_candidate':'all_routes_combined_v3338_candidate',
      'lil_B131_B133_reference_approval_v3335b':'lil_B135_B136_reference_approval_v3368',
      'lil_B131_B133_loader_v3331':'lil_B135_B136_loader_v3365b','editorial_handoff_verification_v3328':'editorial_handoff_verification_v3362',
      "'whole_typed_speech_proof','native_progressive_proof','native_FE_proof','native_choice_proof'":"'native_progressive_proof'",
      'lil_B131_B133_relocation_v3329b':'lil_B135_B136_relocation_v3363c',
      'lil_B131_B133':'lil_B135_B136','B131-B133':'B135-B136','B131/B133':'B135/B136',
      'str(DOC),str(MENU),str(MAP)':'str(DOC),str(MAP)',"choices=str(MENU)":"choices=None",
      "len(proof['changed_records'])==63":"len(proof['changed_records'])==35",
      "for doc_key,original_path in [('manuscript',DOC),('choices',MENU)]:":"for doc_key,original_path in [('manuscript',DOC)]:",
      "for more_key in ('manuscript', 'choices'):":"for more_key in ('manuscript',):",
      'release_stack_v3337b_pending':'release_stack_v3371b_pending',
      'B135/B136 must run once after the complete V3300 stack':'B135/B136 must run once after the complete V3338 stack',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    a=t.index('    deps.update([\'scripts/research_');z=t.index('    for path in list(deps):',a)
    names=['research_lil_B135_B136_relocation_v3363c','prepare_lil_B135_B136_research_v3364b','verify_lil_B135_B136_loader_v3365c','verify_lil_B135_B136_references_v3366b','prove_lil_B135_B136_relocated_controls_v3367b','seal_lil_B135_B136_references_v3368','verify_lil_B135_B136_fonts_v3359b','approve_lil_B135_B136_native_v3360','author_lil_B135_B136_v3355','lil_Espinosa_tablet_prose_v3354','read_lil_B135_B136_clean_context_v3349','reconcile_lil_B135_B136_terms_v3352','refine_lil_B135_B136_phrase_flow_v3358','refine_lil_B135_conditional_v3358c']
    t=t[:a]+'    deps.update('+repr(['scripts/'+n+'.py' for n in names])+')\n'+t[z:]
    t='\n'.join(line for line in t.split('\n') if not any(s in line for s in ["for p in read(doc['native_FE_proof'])","    def modal(","    def choice(","    def zero("]))
    t=t.replace("if '{MACRO:FI}' in r['english']","if '{MACRO:FO}' in r['english']")
    a=t.index('    changes=[\n');z=t.index('    for label,path,key,mutate in changes:',a)
    t=t[:a]+"""    changes=[
      ('missing_format_review',DOC,'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
      ('wrong_Japanese_source',DOC,'manuscript',lambda d:d['records'][0].update(source_hex='00')),
      ('wrong_current_body',DOC,'manuscript',lambda d:d['records'][0].update(current_hex='00')),
      ('wrong_consumer',DOC,'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
      ('missing_actor_state',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english'].split('}',1)[1])),
      ('wrong_actor_state',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english'].replace('SPEAKER:60','SPEAKER:02'))),
      ('invented_macro',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
      ('changed_approved_prose',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' Fine.')),
      ('missing_source_FO',DOC,'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FO}','Argot Co.'))),
      ('wrong_complete_preamble',DOC,'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff0002')),
      ('wrong_formatter',DOC,'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py')),
      ('missing_speech',DOC,'manuscript',lambda d:d['records'].pop()),
      ('source00_outside_scope',DOC,'manuscript',lambda d:d['records'][0].update(source_selector=0)),
      ('manual_layout',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{LB}')),
      ('embedded_NUL',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{HEX:00}')),
      ('missing_reference_approval',MAP,'reference_map',lambda d:d.update(external_references_complete=False)),
      ('wrong_mapped_command',MAP,'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
      ('wrong_relative_target',MAP,'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
      ('missing_predicate_gate',MAP,'reference_map',lambda d:d.update(all1_relocated_predicate_pair_preserves_source_operands_results_and_unowned_RAM=False)),
      ('false_speech_scope',MAP,'reference_map',lambda d:d.update(all35_active_speech_targets_preserved=False)),
      ('false_source_kind_scope',MAP,'reference_map',lambda d:d.update(no_FE_source00_2100_2000_dynamic_or4100_objects=False)),
      ('invented_query',MAP,'reference_map',lambda d:d.update(original_event_queries=[dict(event=1)])),
      ('wrong_entry',MAP,'reference_map',lambda d:d.update(entry_point_offset=12)),
      ('wrong_target_hash',MAP,'reference_map',lambda d:d.update(target_SC2_sha256='0'*64)),
    ]
"""+t[z:]
    t=t.replace('assert len(changes)==46 and len(negatives)==50','assert len(changes)==24 and len(negatives)==28').replace('negative_cases=50','negative_cases=28')
    a=t.index('    profile.update(');z=t.index("    registry['profiles'][PROFILE]",a)
    t=t[:a]+"    profile.update(lil_B135_B136_editorial=owned.CONFIG,description='Complete V3338 cumulative stack plus35 contextual Lil B135/B136 reviews.',note='16revisions/19justified retentions;35progressive speeches,sixstaticactors/FO1/onepredicate/61commands/fourspans/20targetskips.35nativeplanes/280logical-compiled/140finalmacrocases;all5sheets viewed orhash-exact,15rowcount-only notes. OneeffectiveCamille replacement retained. Sharedactual display rules inherited byexactcode/assets;no selectednewscene/nameplate/earnedprogress. Registeredbuild/exactcleanpatch/freshstartup pending. Experimental,preserveeveryROM/translation,no promotion.')\n"+t[z:]
    t=t[:t.rindex('    print(')]+"    print('RegisteredV3372 one-manuscript35-object stage;28compiler negatives reject beforemutation. FullV3338/114acceptedlayers/V1492 promotion preserved.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B135_B136_registration_tools_v3371');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
