"""Bind trusted B51 native adapters and independently recompute every body/name."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_native_production_v8587')
    assert not root.exists()
    sourcepath = Path('work/analysis/Hodram_B51_source_display_v8556/source_display.json')
    controlpath = Path('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json')
    guardpath = Path('dk4tool/patch/hodram_B50_native_guards_v1.py')
    source = guardpath.read_text('utf-8')
    oldadapters = next(line for line in source.splitlines() if line.startswith('ADAPTERS='))
    oldtrusted = next(line for line in source.splitlines() if line.startswith('TRUSTED='))
    adapters = {key: (sourcepath.as_posix(), field) for key, field in [
        ('pages', 'source_owned_target_page_adapter'), ('dispatch', 'source_owned_dispatch_adapters'),
        ('macro_body', 'source_owned_macro_body_adapter'), ('progressive_macro', 'source_owned_progressive_adapter')]}
    adapters.update({key: (controlpath.as_posix(), field) for key, field in [
        ('seeded_end', 'source_owned_seeded_end_adapter'), ('entry', 'source_owned_entry_adapter'),
        ('skip', 'source_owned_skip_probe'), ('query', 'source_owned_query_probe')]})
    derivations = [derive(str(guardpath), 'dk4tool/patch/hodram_B51_native_guards_v1.py', {
        'hodram_B50_profile_v2': 'hodram_B51_profile_v1', 'B50 native adapter:': 'B51 native adapter:',
        oldadapters: 'ADAPTERS=' + repr(adapters), oldtrusted: 'TRUSTED=' + repr({p.as_posix(): sha(p.read_bytes()) for p in [sourcepath, controlpath]}),
        'Exact trusted B50 source adapter': 'Exact trusted B51 source adapter',
    })]
    derivations.append(derive('dk4tool/patch/hodram_B50_native_evidence_v1.py', 'dk4tool/patch/hodram_B51_native_evidence_v1.py', {
        'scoped Lil nameplane': 'four scoped nameplanes',
        'hodram_B50_native_guards_v1': 'hodram_B51_native_guards_v1',
        "len(rows)==3 and {r['source_selector'] for r in rows}=={2,254}": "len(rows)==5 and {r['source_selector'] for r in rows}=={1,16,18,113} and all(r['kind']=='progressive' for r in rows)",
        'three source-qualified mixed-consumer records': 'five source-qualified progressive records',
        'pixels,factory,oracle=bind(parent);paint,calibration=factory(parent)': 'pixels,unused_factory,oracle=bind(parent)',
        "len(declared)==3 and len({r['id'] for r in declared})==3": "len(declared)==5 and len({r['id'] for r in declared})==5",
        'Recompute the scoped Lil default-name plane': 'Recompute four scoped default-name planes',
        "len(declared)==1 and declared==[source['reused_original_Lil_style11_plane']]": "len(declared)==4 and declared==[b['reused_current_original_style11_plane'] for b in source['scoped_clean_current_four_names_andreused_native_consumers']]",
        'one exact scoped source-bound Lil nameplane': 'four exact scoped source-bound nameplanes',
        "[(2,'Lil Argot',b'Lil Argot')]": "[(1,'Hodram Bergstrom',b'Hodram Bergstrom'),(16,'Gerhard Adernkatz',b'Gerhard Adernkatz'),(18,'Charles Rochefort',b'Charles Rochefort'),(113,'Port Worker',b'Port Worker')]",
        "set(names)=={2}": "set(names)=={1,16,18,113}",
        'one unique scoped source identity': 'four unique scoped source identities',
        'native_body_pages_recomputed=6,progressive_pages=4,original_FE_pages=2,scoped_style11_nameplanes_recomputed=1':
            'native_body_pages_recomputed=10,progressive_pages=10,original_FE_pages=0,scoped_style11_nameplanes_recomputed=4',
        'FE_original_index15_ink14_CP932_shadow_not_old_normalized1=True': 'no_FE_body_orpalette_scope_in_this_five_progressive_batch=True',
    }))
    from dk4tool.patch.hodram_B51_native_evidence_v1 import check_native_models
    from dk4tool.dialogue.hodram_B51_profile_v1 import validate_approved_batch, validate_runtime
    paths = dict(source_display=sourcepath.as_posix(), stored='work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
        models='work/analysis/Hodram_B51_models_v8575/native_models.json', pages='work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json')
    data = {key: read(path) for key, path in paths.items()}
    docpath = Path('translations/hodram_B51_editorial_manuscript_v5.json')
    doc = read(docpath)
    parent = NdsImage.open(doc['current_ROM'])
    validate_approved_batch(doc)
    validate_runtime(parent)
    def require(value, message):
        if not value:
            raise ValueError('B51 native production: ' + message)
    result = check_native_models(data, doc['records'], parent, read, require)
    assert result['summary']['native_body_pages_recomputed'] == 10 and len(result['names']) == 4
    negatives = []
    def reject(label, mutate):
        changed = deepcopy(data)
        mutate(changed)
        assert changed != data
        try:
            check_native_models(changed, doc['records'], parent, read, require)
        except ValueError as error:
            assert 'Native dependency changed' not in str(error)
            negatives.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed native evidence accepted: ' + label)
    reject('untrusted-page-adapter', lambda d: d['pages'].__setitem__('source_owned_target_page_adapter', d['pages']['source_owned_target_page_adapter'] + '\n'))
    reject('missing-source-body', lambda d: d['models']['native_models']['clean_Japanese'].pop())
    reject('missing-English-body', lambda d: d['models']['native_models']['revised_English'].pop())
    reject('source-expanded-bytes', lambda d: d['models']['native_models']['clean_Japanese'][0].__setitem__('expanded_native_hex', '00'))
    reject('English-stored-selector', lambda d: d['models']['native_models']['revised_English'][0].__setitem__('source_selector', 112))
    reject('source-complete-consumption', lambda d: d['models']['native_models']['clean_Japanese'][0].__setitem__('complete_consumed_bytes', 1))
    reject('English-last-glyph-metadata', lambda d: d['models']['native_models']['revised_English'][0]['pages'][0].__setitem__('end', 1))
    reject('name-membership', lambda d: d['models']['name_planes'].pop())
    reject('Gerhard-surname', lambda d: d['models']['name_planes'][1].__setitem__('text', 'Gerhard Ardelknatts'))
    reject('Charles-final-character', lambda d: d['models']['name_planes'][2].__setitem__('input_hex', d['models']['name_planes'][2]['input_hex'][:-2]))
    assert len(negatives) == 10
    root.mkdir(parents=True)
    save(root / 'native_production_validation.json', dict(module_derivations=derivations, summary=result['summary'], positive_native_pages=10,
        positive_scoped_nameplanes=4, negative_count=10, negative_cases=negatives,
        every_negative_actual_input_changed_andguard_rejected_with_frozen_dependencies_enabled=True,
        complete_first_internal_final_glyphs_bounds_consumption_planes_names_andfont_independently_recomputed=True,
        source_owned_adapters_exact_andnot_declared_by_challenged_release_evidence=True,
        no_producer_replay_emulator_capture_ROM_write_atomic_commit_orcompletion_credit=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [*paths.values(), docpath, Path(__file__),
            Path('dk4tool/patch/hodram_B51_native_guards_v1.py'), Path('dk4tool/patch/hodram_B51_native_evidence_v1.py')]}))
    print('B51 native production: ten source/stored pages and four complete nameplanes independently recomputed; ten actual-changing evidence defects reject with frozen guards enabled. No new gameplay or ROM commit.')
