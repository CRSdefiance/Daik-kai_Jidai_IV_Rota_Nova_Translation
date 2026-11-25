"""Bind B52 original loaders and exactly reuse the unchanged complete caller census."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_loaders_production_v8681')
    assert not root.exists()
    receipt = derive('dk4tool/patch/hodram_B51_loaders_v1.py', 'dk4tool/patch/hodram_B52_loaders_v1.py', {
        'B51': 'B52', "caller['block']==51": "caller['block']==52",
        "caller['all5_text_records']": "caller['all3_speech_records']",
        "caller['typed_choice_records']==[]": "caller['typed_choice_records']==data['stored']['typed_choice_records'] and [r['id'] for r in caller['typed_choice_records']]==declared['choice_commands'][0]['record_IDs']",
        'all20 caller-selected source/current/final command maps and5record references': 'all14 caller-selected source/current/final command maps and3speech/2choice references',
        "a.get('native_selected_block')==51": "a.get('native_selected_block')==52",
        "[(e['event_ID'],e['script_block'],e['must_be_completed']) for e in caller['source_event_records']]==[(51,51,[])]": "[(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in caller['source_event_records']]==[(52,52,[30],[74])]",
        'event51 hasno listed prerequisite,not full eligibility orchronology': 'event52 requires30/excludes74,not full eligibility orchronology',
        "require(census(reference)==caller['native_call_census'] and caller['external_references_complete'],'independent shipped code caller/literal census')": """from ndspy.code import MainCodeFile,loadOverlayTable
    from dk4tool.patch.main_pool_cache_visibility import BASE
    from dk4tool.dialogue.hodram_B52_profile_v1 import contract
    frozen=contract();priorpath=Path('work/analysis/Hodram_B51_references_v8572/references.json')
    require(Path(caller['exact_prior_census'])==priorpath and sha(priorpath.read_bytes())==frozen['dependencies'][str(priorpath.resolve())],'exact immutable prior complete caller census')
    prior=load(priorpath)
    units=[('section'+str(n),s.ramAddress,bytes(s.data)) for n,s in enumerate(MainCodeFile(arm,BASE).sections)]
    units += [('overlay'+str(n),s.ramAddress,bytes(s.data)) for n,s in loadOverlayTable(reference.rom.arm9OverlayTable,lambda _,f:reference.rom.files[f]).items()]
    fingerprints=[dict(name=n,base=b,bytes=len(value),sha256=sha(value)) for n,b,value in units]
    require(fingerprints==prior['native_call_census']['units'] and prior['native_call_census']==caller['native_call_census'] and caller['external_references_complete'],'complete identical decoded native input units justify exact census reuse')""",
        "caller['fresh_caller_censuses']==1": "caller['fresh_caller_censuses']==0 and caller['exact_reused_caller_censuses']==1",
        'preserved exact prior shippedcode association plus fresh B51 census': 'preserved exact prior shippedcode association, no repeated census',
        'shipped_code_caller_census_recomputed=True': 'shipped_code_caller_census_recomputed=False,complete_original_shipped_code_census_reused_by_every_decoded_unit_identity=True',
    })
    from dk4tool.patch.hodram_B52_loaders_v1 import check_loaders_and_census
    paths = dict(loaders='work/analysis/Hodram_B52_loaders_v8646/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
        callers='work/analysis/Hodram_B52_references_v8647/references.json',
        relocation='work/analysis/Hodram_B52_references_v8647/source_current_final_map.json',
        current='work/analysis/Hodram_B52_current_v8631/current_effective.json',
        stored='work/analysis/Hodram_B52_stored_v8643/stored_native_controls_andrefs.json')
    data = {k: read(p) for k,p in paths.items()}
    docpath = Path('translations/hodram_B52_editorial_manuscript_v6.json')
    doc = read(docpath)
    parent, reference = [NdsImage.open(doc[k]) for k in ['current_ROM','reference_ROM']]

    def require(value, message):
        if not value:
            raise ValueError('B52 loader production:' + message)

    result = check_loaders_and_census(data,parent,reference,data['relocation'],read,require)
    negatives = []

    def reject(label, mutate):
        changed = deepcopy(data)
        mutate(changed)
        assert changed != data
        try:
            check_loaders_and_census(changed,parent,reference,changed['relocation'],read,require)
        except ValueError as error:
            assert 'Native dependency changed' not in str(error)
            negatives.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=str(error)))
        else:
            raise AssertionError('Changed loader evidence accepted:' + label)

    reject('missing-loader-count',lambda d:d['loaders'].__setitem__('fresh_native_whole_loads_andcache_hits',324))
    reject('parent-mode-count',lambda d:d['loaders'].__setitem__('fresh_initial_parent_modes',649))
    reject('caller-command-offset',lambda d:d['callers']['all_command_maps'][0].__setitem__('new_offset',10))
    reject('wrong-event-prerequisite',lambda d:d['callers']['source_event_records'][0].__setitem__('must_be_completed',[51]))
    reject('natural-activation-overclaim',lambda d:d['loaders'].__setitem__('controlled_native_route_global_inputs_not_ordinary_event_activation',False))
    reject('changed-complete-code-unit',lambda d:d['callers']['native_call_census']['units'][0].__setitem__('sha256','0'*64))
    reject('typed-choice-reference',lambda d:d['callers']['typed_choice_records'][1]['final_reference'].__setitem__('offset',92))
    assert len(negatives)==7
    root.mkdir(parents=True)
    save(root/'loader_production_validation.json',dict(derivation=receipt,summary=result,negative_count=7,negative_cases=negatives,
         every_negative_actual_input_changed_andguard_rejected_with_frozen_dependencies_enabled=True,
         original325_loads_cachehits650_parentmodes326_actions_independently_bound=True,
         existing_census_reused_by_exact_name_base_length_andhash_ofevery_shipped_decoded_unit=True,
         no_repeated_census_native_loader_producer_oractual_capture=True,
         no_ROM_registry_atomic_commit_orcompletion_credit=True,full_goal_complete=False,
         evidence={str(p):sha(Path(p).read_bytes()) for p in [*paths.values(),docpath,__file__,'dk4tool/patch/hodram_B52_loaders_v1.py']}))
    print('B52 production loaders:325cache-loads/650modes/326actions,all5speech-choice refs andexact complete native-unit census reuse;7 changed evidence defects reject. No new capture/ROM/credit.')
