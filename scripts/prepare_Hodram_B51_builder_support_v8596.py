"""Prepare source-locked B51 builder support; never edit the live builder here."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive, checked_text
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v6 import STAGE_V6, STAGE_B49_V3, STAGE_B50

ROOT = Path('work/analysis/Hodram_B51_builder_support_v8596')
SPECS = [
    ('dialogue', 'profile', 6, 7, {'hodram_outcomes_builder_guard_v6': 'hodram_outcomes_builder_guard_v7'}),
    ('dialogue', 'layout', 6, 7, {'hodram_outcomes_profile_v6': 'hodram_outcomes_profile_v7'}),
    ('dialogue', 'names', 6, 7, {'hodram_outcomes_profile_v6': 'hodram_outcomes_profile_v7'}),
    ('patch', 'native_guards', 6, 7, {'hodram_outcomes_profile_v6': 'hodram_outcomes_profile_v7'}),
    ('patch', 'native_evidence', 7, 8, {'hodram_outcomes_native_guards_v6': 'hodram_outcomes_native_guards_v7'}),
    ('patch', 'controls', 6, 7, {'hodram_outcomes_profile_v6': 'hodram_outcomes_profile_v7', 'hodram_outcomes_native_guards_v6': 'hodram_outcomes_native_guards_v7'}),
    ('patch', 'editorial', 6, 7, {
        'hodram_outcomes_profile_v6': 'hodram_outcomes_profile_v7', 'hodram_outcomes_layout_v6': 'hodram_outcomes_layout_v7',
        'hodram_outcomes_names_v6': 'hodram_outcomes_names_v7', 'hodram_outcomes_native_evidence_v7': 'hodram_outcomes_native_evidence_v8',
        'hodram_outcomes_controls_v6': 'hodram_outcomes_controls_v7', 'hodram_outcomes_builder_guard_v6': 'hodram_outcomes_builder_guard_v7',
        'hodram_outcomes_editorial_release_v6': 'hodram_outcomes_editorial_release_v7'}),
]
VALIDATOR = '''def validate_builder_bytes(raw,digest):
    if not isinstance(raw,bytes):raise ValueError('Hodram builder guard: complete builder bytes required')
    predecessor,prior,B50,addition=STAGE_V7.encode(),STAGE_B49_V4.encode(),STAGE_B50_V2.encode(),STAGE_B51.encode()
    present=any(stage in raw for stage in [predecessor,prior,B50,addition]);normalized=raw
    if present:
        if any(raw.count(stage)!=1 for stage in [predecessor,prior,B50]) or raw.count(addition)>1:
            raise ValueError('Hodram builder guard: complete compatible outcomesv7/B49v4/B50v2 stages once required')
        if any(stage.encode() in raw for stage in [STAGE_V6,STAGE_B49_V3,STAGE_B50]):
            raise ValueError('Hodram builder guard: mixed owned versions forbidden')
        boundary=b'    # Lexically valid "% o"'
        if raw.count(boundary)!=1 or not raw.index(predecessor)<raw.index(prior)<raw.index(B50)<raw.index(boundary):
            raise ValueError('Hodram builder guard: original predecessor order before final percent safety required')
        if addition in raw:
            if not raw.index(B50)+len(B50)<=raw.index(addition)<raw.index(boundary):
                raise ValueError('Hodram builder guard: B51 must follow complete B50 before final percent safety')
            normalized=normalized.replace(addition,b'',1)
        normalized=normalized.replace(predecessor,STAGE_V6.encode(),1).replace(prior,STAGE_B49_V3.encode(),1).replace(B50,STAGE_B50.encode(),1)
    proof=previous_validate(normalized,digest);compile(raw,str(BUILDER),'exec')
    return {**proof,'compatible_v7_predecessors':present,'B50_stage_module_version':2 if present else 1,'B51_additive_stage_present':addition in raw}
'''

if __name__ == '__main__':
    assert not ROOT.exists()
    guard = Path('dk4tool/patch/hodram_outcomes_builder_guard_v7.py')
    assert not guard.exists()
    stage = checked_text('if True:\n' + STAGE_B50, {'hodram_B50': 'hodram_B51', 'Hodram B50': 'Hodram B51', 'V8475': 'V8543'}).split('\n', 1)[1]
    old = Path('dk4tool/patch/hodram_outcomes_builder_guard_v6.py')
    source = old.read_text('utf-8')
    a, b = source.index('STAGE_V6='), source.index('\ndef validate_builder_bytes')
    c, d = source.index('def validate_builder_bytes'), source.index('\ndef checked_dependency')
    stages = "STAGE_V7=checked_text('if True:\\n'+STAGE_V6,{'hodram_outcomes_editorial_v6':'hodram_outcomes_editorial_v7'}).split('\\n',1)[1]\n"
    stages += "STAGE_B49_V4=checked_text('if True:\\n'+STAGE_B49_V3,{'hodram_B49_editorial_v3':'hodram_B49_editorial_v4'}).split('\\n',1)[1]\n"
    stages += "STAGE_B50_V2=checked_text('if True:\\n'+STAGE_B50,{'hodram_B50_editorial_v1':'hodram_B50_editorial_v2'}).split('\\n',1)[1]\n"
    stages += 'STAGE_B51=' + repr(stage) + '\n'
    tools = [derive(str(old), str(guard), {
        'from dk4tool.patch.hodram_outcomes_builder_guard_v5 import BUILDER,STAGE_V5,STAGE_B49_V2,validate_builder_bytes as previous_validate':
            'from dk4tool.patch.hodram_outcomes_builder_guard_v6 import BUILDER,STAGE_V6,STAGE_B49_V3,STAGE_B50,validate_builder_bytes as previous_validate',
        source[a:b]: stages, source[c:d]: VALIDATOR,
        'Permit exact preserved builders or one additive B50 stage after compatible outcomesv6/B49v3,with full original inverse.':
            'Permit preserved builders or one additive B51 stage after compatible outcomesv7/B49v4/B50v2,with full original inverse.',
    })]
    paths = [guard]
    for area, name, before, after, changes in SPECS:
        src, dst = Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{before}.py'), Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{after}.py')
        tools.append(derive(src, dst, changes))
        paths.append(dst)
    B49 = Path('dk4tool/patch/hodram_B49_editorial_v4.py')
    B50 = Path('dk4tool/patch/hodram_B50_editorial_v2.py')
    tools.append(derive('dk4tool/patch/hodram_B49_editorial_v3.py', str(B49), {'hodram_outcomes_builder_guard_v6': 'hodram_outcomes_builder_guard_v7'}))
    tools.append(derive('dk4tool/patch/hodram_B50_editorial_v1.py', str(B50), {'hodram_outcomes_builder_guard_v6': 'hodram_outcomes_builder_guard_v7'}))
    paths.extend([B49, B50])
    def extend(oldpath, newpath, added, inherited=None):
        oldpath, newpath = Path(oldpath), Path(newpath)
        assert not newpath.exists()
        conf = read(oldpath)
        original = dict(conf['dependencies'])
        if inherited:
            for key, digest in inherited.items():
                assert key not in conf['dependencies'] or conf['dependencies'][key] == digest
                conf['dependencies'][key] = digest
        for path in [oldpath, Path(__file__), *added]:
            key, digest = str(path.resolve()), sha(path.read_bytes())
            assert key not in conf['dependencies'] or conf['dependencies'][key] == digest
            conf['dependencies'][key] = digest
        assert all(conf['dependencies'][key] == digest for key, digest in original.items())
        save(newpath, conf)
        return conf, dict(old_configuration=str(oldpath), old_configuration_sha256=sha(oldpath.read_bytes()), new_configuration=str(newpath),
            new_configuration_sha256=sha(newpath.read_bytes()), prior_dependencies=len(original), new_dependencies=len(conf['dependencies']), all_prior_dependencies_retained_exact=True)
    oc = Path('translations/hodram_outcomes_editorial_release_v7.json')
    bc = Path('translations/hodram_B49_editorial_release_v5.json')
    fc = Path('translations/hodram_B50_editorial_release_v2.json')
    outcomes, outcome_binding = extend('translations/hodram_outcomes_editorial_release_v6.json', oc, paths)
    B49conf, B49_binding = extend('translations/hodram_B49_editorial_release_v4.json', bc, [oc, guard, B49], outcomes['dependencies'])
    B50conf, B50_binding = extend('translations/hodram_B50_editorial_release_v1.json', fc, [oc, bc, guard, B49, B50], B49conf['dependencies'])
    frozen = {str(p): sha(p.read_bytes()) for p in [Path('translations/hodram_outcomes_native_contract_v1.json'), Path('translations/hodram_B49_native_contract_v2.json'), Path('translations/hodram_B50_native_contract_v2.json')]}
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_equivalence.json', dict(derivations=tools, namespace_only_outcomes_derivations=tools[1:8], B49_guard_import_only_derivation=tools[-2],
        B50_guard_import_only_derivation=tools[-1], new_stage=stage, outcomes_configuration=outcome_binding, B49_configuration=B49_binding, B50_configuration=B50_binding,
        all535_prior_outcomes_dependencies_retained_exact=True, all675_prior_B49_dependencies_retained_exact=True, all756_prior_B50_dependencies_retained_exact=True,
        all_prior_semantic_bodies_native_addresses_andmultiplicity_preserved=True, unchanged_frozen_native_contracts=frozen,
        exact_builder_validation_wholeV8543_compatibility_andlive_builder_change_pending=True, no_builder_registry_ROM_orcredit_change=True,
        new_credit=0, full_goal_complete=False))
    print('Prepared additive B51 guardv7 andnamespace-only outcomesv7/B49v4/B50v2;all535/675/756 prior dependency entries preserved. Live builder/registry/ROM unchanged.')
