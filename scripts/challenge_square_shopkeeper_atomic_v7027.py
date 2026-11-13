"""Challenge real-changing source/native/display corruptions before the sole ROM write."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import square_shopkeeper_label_release_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_shopkeeper_atomic_v7027')
POSITIVE=Path('work/analysis/square_shopkeeper_atomic_v7026b')
if __name__=='__main__':
    assert not ROOT.exists();positive=read(POSITIVE/'positive_receipt.json');config=Path(positive['config']);conf=read(config)
    parent=Path(positive['parent_ROM']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');source=NdsImage.open(parent)
    require_paths={kind:Path(conf[key]) for kind,key in [('doc','manuscript'),('seal','approval'),('names','names'),('actual','actual'),('view','view')]}
    bases={'conf':conf,**{kind:read(path) for kind,path in require_paths.items()}}
    before={p:sha(Path(p).read_bytes()) for p in [*conf['dependencies'],str(config),str(parent),'translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json']}
    def target_name(n,actor=82):return next(r for r in n['versions'][1]['name_getters']['rows'] if r['actor_ID']==actor and r['consumer']=='progressive-nameplate')
    tests=[
        ('unknown-format','conf',lambda d:d.update(format='unknown')),
        ('wrong-current-runtime','conf',lambda d:d.update(source_ARM9_sha256='0'*64)),
        ('wrong-current-COMMON','conf',lambda d:d['source_files'].update({'/COMMON/MESFILE.DK4':'0'*64})),
        ('wrong-current-component','conf',lambda d:d['source_components'].update({owned.PATH:'0'*64})),
        ('wrong-canonical-runtime','conf',lambda d:d.update(canonical_ARM9_sha256='0'*64)),
        ('wrong-clean-ROM','conf',lambda d:d.update(clean_ROM_sha256='0'*64)),
        ('wrong-target-runtime','conf',lambda d:d.update(target_ARM9_sha256='0'*64)),
        ('wrong-reference-ROM','conf',lambda d:d.update(reference_ROM_sha256='0'*64)),
        ('missing-critical-helper','conf',lambda d:d['dependencies'].pop(next(p for p in d['dependencies'] if p.endswith('square_shopkeeper_exact_native_context_v7020.py')))),
        ('altered-dependency-hash','conf',lambda d:d['dependencies'].update({d['names']:'0'*64})),
        ('wrong-locale','doc',lambda d:d.update(target_locale='en-GB')),
        ('wrong-policy','doc',lambda d:d.update(translation_policy='literal')),
        ('closed207-review','doc',lambda d:d.update(all207_name_review_scope_remains_open=False)),
        ('claim-catalogue-UI-visit','doc',lambda d:d.update(full_catalogue_UI_unvisited=False)),
        ('claim-full-goal','doc',lambda d:d.update(full_goal_complete=True)),
        ('hidden-later-differences','doc',lambda d:d.update(all_measured_later_differences_preserved_for_older_record_technical_reaudit=False)),
        ('missing-tenth-actor','doc',lambda d:d['records'].pop()),
        ('wrong-source-role','doc',lambda d:d['records'][0].update(source_Japanese='店主')),
        ('invent-stall-occupation','doc',lambda d:d['records'][0].update(english='Stallkeeper')),
        ('duplicate-record-identity','doc',lambda d:d['records'][1].update(id=d['records'][0]['id'])),
        ('unreviewed-formatting','doc',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('empty-context','doc',lambda d:d['records'][0].update(context='')),
        ('duplicate-dialogue-credit','doc',lambda d:d['records'][0].update(new_dialogue_completion_credit=1)),
        ('duplicate-name-credit','doc',lambda d:d['records'][0].update(new_name_completion_credit=1)),
        ('truncated-clean-reference','doc',lambda d:d['records'][0]['source_reference'].update(terminated_hex='8d4c')),
        ('wrong-current-pointer','doc',lambda d:d['records'][0]['current_reference'].update(runtime_pointer=34984073)),
        ('wrong-complete-target-terminator','doc',lambda d:d['records'][0]['target_reference'].update(terminated_hex=b'Shopkeeper'.hex())),
        ('missing-secondary-field','doc',lambda d:d['records'][0]['all_three_source_current_name_fields'].pop(1)),
        ('altered-unused-metadata-field','doc',lambda d:d['records'][-1]['all_three_source_current_name_fields'][1].update(current_pointer=37256665)),
        ('false-sealed-manuscript-hash','seal',lambda d:d.update(manuscript_sha256='0'*64)),
        ('lost-ten-context-approval','seal',lambda d:d.update(all_ten_source_context_localization_naturalness_and_formatting_gates_true=False)),
        ('claimed-global-name-approval','seal',lambda d:d.update(full_catalogue_UI_every_conditional_nameplate_and_full207_editorial_approval_not_claimed=False)),
        ('changed-unread-tail-plan','seal',lambda d:d['source_owned_data_plan']['literal_slots'][0].update(untouched_old_tail_hex='00')),
        ('changed-other-actor-name','names',lambda d:target_name(d,0).update(text='Invented')),
        ('changed-returned-pointer','names',lambda d:target_name(d).update(pointer=34984073)),
        ('changed-voice','names',lambda d:next(r for r in d['versions'][1]['catalogue_voices']['rows'] if r['actor_ID']==82).update(original_voice_class=7)),
        ('changed-secondary-output','names',lambda d:next(r for r in d['versions'][1]['field_getters']['rows'] if r['actor_ID']==82 and r['column']==4).update(text_hex=b'European Shopkeeper'.hex())),
        ('missing-field-consumer','names',lambda d:d['versions'][1]['field_getters']['rows'].pop()),
        ('forced-dynamic-role','names',lambda d:d['versions'][1]['dynamic_roles']['rows'][0].update(resolved_actor_ID=85)),
        ('wrong-captain-object-claim','names',lambda d:d.update(original_actual_captain2_uses_special_object=False)),
        ('lost-memory-restoration','names',lambda d:d.update(all_original_scratch_or_readonly_paths_restore_all4MiB=False)),
        ('wrong-macro-count','names',lambda d:d.update(macro_alignment_cases=175)),
        ('lost-macro-first-glyph','names',lambda d:d['macro_versions'][1]['cases'][1]['native']['cases'][0].update(output_hex=b'hopkeeper'.hex())),
        ('lost-macro-memory-restoration','names',lambda d:d['macro_versions'][1]['cases'][0]['native']['cases'][0].update(source_owned_name_ring_restoration_recovers_complete4MiB=False)),
        ('wrong-first-native-glyph','names',lambda d:d['native_name_plane']['events'][0].update(code=67)),
        ('wrong-native-width','names',lambda d:d['native_name_plane'].update(native_width=102)),
        ('wrong-actual-object-count','actual',lambda d:d.update(target_speech_observations=29)),
        ('lost-actual-complete-page','actual',lambda d:d['versions'][1]['panels'][0]['complete_page_holds'][0].clear()),
        ('lost-actual-complete-header','actual',lambda d:d['versions'][1]['panels'][0]['complete_name_holds'].clear()),
        ('wrong-actual-selector','actual',lambda d:d['versions'][1]['panels'][0].update(actor_ID=82)),
        ('wrong-actual-caption','actual',lambda d:d['versions'][1]['panels'][1].update(name='Square Shopkeeper')),
        ('changed-normal-value','actual',lambda d:d['versions'][1]['command_pairs'][-1].update(result=[0,1])),
        ('changed-native-UI','actual',lambda d:d['versions'][1]['command_pairs'][-2].update(UI_after=[0])),
        ('erased-timing-RNG-differences','actual',lambda d:d['comparisons'][0]['command_differences'].clear()),
        ('hidden-outside-caption-RGB','actual',lambda d:next(r for r in d['comparisons'][0]['RGB_differences'] if not r['all_differences_within_nameplate_strip']).update(all_differences_within_nameplate_strip=True)),
        ('claimed-world-equivalence','actual',lambda d:d['comparisons'][0].update(no_full_RAM_final_components_future_or_complete_causal_equivalence_claim=False)),
        ('closed-B189-wrap-lead','actual',lambda d:d.update(B189_early_line_breaks_separate_retrospective_editorial_lead=False)),
        ('claimed-natural-activation','actual',lambda d:d.update(initialized_scenes_not_natural_activation_original_location_earned_progress_full_effects_full_route_or_hardware=False)),
        ('unviewed-sheets','view',lambda d:d.update(visual_review_pending=True)),
        ('false-pane-pixel-proof','view',lambda d:d['all32_whole_frame_panes_pixel_equal'][0].update(whole_pane_pixel_equal=False)),
        ('misbound-actual-view-reference','view',lambda d:d['all32_whole_frame_panes_pixel_equal'][0].update(capture='wrong.png')),
    ]
    assert len({t[0] for t in tests})==len(tests);cases=[];original=owned.load
    for label,kind,edit in tests:
        values={k:deepcopy(v) for k,v in bases.items()};edit(values[kind]);assert values[kind]!=bases[kind],'No-op negative:'+label
        overrides={config.resolve():values['conf'],**{path.resolve():values[k] for k,path in require_paths.items()}}
        image=NdsImage.open(parent);writes=[];replace=image.replace_file
        def tracked(*args,**kwargs):writes.append(args[0]);return replace(*args,**kwargs)
        image.replace_file=tracked;owned.load=lambda p:deepcopy(overrides[Path(p).resolve()]) if Path(p).resolve() in overrides else original(p)
        try:owned.apply_release(image,baseline,config)
        except (ValueError,AssertionError,KeyError,StopIteration) as exc:cases.append(dict(case=label,rejected=True,error=str(exc),archive_writes=len(writes)))
        else:raise AssertionError('Corruption accepted:'+label)
        finally:owned.load=original
        assert not writes and all(image.read_file(p)==v for _,p,v in source.iter_files()) and all(image.read_file(p)==v for p,v in source.iter_components())
        print('Rejected',label,flush=True)
    for p,h in before.items():assert sha(Path(p).read_bytes())==h
    ROOT.mkdir(parents=True);save(ROOT/'negative_cases.json',cases)
    receipt=deepcopy(positive);receipt.update(negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(cases),all_negatives_reject_before_mutation=True,
        virtual_JSON_semantics_tested_behind_valid_physical_hashes=True,all_actual_source_files_config_registry_builder_ledger_pins_and_ROMs_unchanged=True,full_goal_complete=False)
    save(ROOT/'atomic_validation_receipt.json',receipt);print(f'{len(cases)} real-changing corruptions rejected before writes;all source artifacts preserved.',flush=True)
