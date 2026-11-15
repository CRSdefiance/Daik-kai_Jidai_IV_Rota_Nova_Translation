"""Prepare additive B50 builder support and namespace-only predecessor successors;no builder edit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v5 import STAGE_V5,STAGE_B49_V2

ROOT=Path('work/analysis/Hodram_B50_builder_support_v8534')
SPECS=[
 ('dialogue','profile',5,6,{'hodram_outcomes_builder_guard_v5':'hodram_outcomes_builder_guard_v6'}),
 ('dialogue','layout',5,6,{'hodram_outcomes_profile_v5':'hodram_outcomes_profile_v6'}),
 ('dialogue','names',5,6,{'hodram_outcomes_profile_v5':'hodram_outcomes_profile_v6'}),
 ('patch','native_guards',5,6,{'hodram_outcomes_profile_v5':'hodram_outcomes_profile_v6'}),
 ('patch','native_evidence',6,7,{'hodram_outcomes_native_guards_v5':'hodram_outcomes_native_guards_v6'}),
 ('patch','controls',5,6,{'hodram_outcomes_profile_v5':'hodram_outcomes_profile_v6','hodram_outcomes_native_guards_v5':'hodram_outcomes_native_guards_v6'}),
 ('patch','editorial',5,6,{'hodram_outcomes_profile_v5':'hodram_outcomes_profile_v6','hodram_outcomes_layout_v5':'hodram_outcomes_layout_v6','hodram_outcomes_names_v5':'hodram_outcomes_names_v6','hodram_outcomes_native_evidence_v6':'hodram_outcomes_native_evidence_v7','hodram_outcomes_controls_v5':'hodram_outcomes_controls_v6','hodram_outcomes_builder_guard_v5':'hodram_outcomes_builder_guard_v6','hodram_outcomes_editorial_release_v5':'hodram_outcomes_editorial_release_v6'}),
]
VALIDATOR='''def validate_builder_bytes(raw,digest):
    if not isinstance(raw,bytes):raise ValueError('Hodram builder guard: complete builder bytes required')
    predecessor,prior,addition=STAGE_V6.encode(),STAGE_B49_V3.encode(),STAGE_B50.encode()
    present=any(s in raw for s in [predecessor,prior,addition]);normalized=raw
    if present:
        if raw.count(predecessor)!=1 or raw.count(prior)!=1 or raw.count(addition)>1:
            raise ValueError('Hodram builder guard: complete compatible v6 andB49v3 stages once required')
        if STAGE_V5.encode() in raw or STAGE_B49_V2.encode() in raw:
            raise ValueError('Hodram builder guard: mixed owned versions forbidden')
        if raw.index(predecessor)>=raw.index(prior):raise ValueError('Hodram builder guard: original predecessor stage order required')
        if addition in raw:
            boundary=b'    # Lexically valid "% o"'
            if raw.count(boundary)!=1 or not raw.index(prior)+len(prior)<=raw.index(addition)<raw.index(boundary):
                raise ValueError('Hodram builder guard: B50 must follow complete B49 before final percent safety')
            normalized=normalized.replace(addition,b'',1)
        normalized=normalized.replace(predecessor,STAGE_V5.encode(),1).replace(prior,STAGE_B49_V2.encode(),1)
    proof=previous_validate(normalized,digest);compile(raw,str(BUILDER),'exec')
    return {**proof,'compatible_v6_predecessor':present,'corrected_B49_stage_version':3 if present else proof.get('corrected_B49_stage_version'),'B50_additive_stage_present':addition in raw}
'''

if __name__=='__main__':
    assert not ROOT.exists();guard=Path('dk4tool/patch/hodram_outcomes_builder_guard_v6.py');assert not guard.exists()
    stage=checked_text('if True:\n'+STAGE_B49_V2,{
        'hodram_B49':'hodram_B50','Hodram B49':'Hodram B50','hodram_B49_editorial_v2':'hodram_B50_editorial_v1','V8377':'V8475',
    }).split('\n',1)[1]
    old=Path('dk4tool/patch/hodram_outcomes_builder_guard_v5.py');source=old.read_text(encoding='utf-8')
    a=source.index('STAGE_V5=');b=source.index('\ndef validate_builder_bytes',a);c=source.index('def validate_builder_bytes');d=source.index('\ndef checked_dependency',c)
    stages="STAGE_V6=checked_text('if True:\\n'+STAGE_V5,{'hodram_outcomes_editorial_v5':'hodram_outcomes_editorial_v6'}).split('\\n',1)[1]\nSTAGE_B49_V3=checked_text('if True:\\n'+STAGE_B49_V2,{'hodram_B49_editorial_v2':'hodram_B49_editorial_v3'}).split('\\n',1)[1]\nSTAGE_B50="+repr(stage)+'\n'
    tools=[derive(str(old),str(guard),{
        'from dk4tool.patch.hodram_outcomes_builder_guard_v4 import BUILDER,STAGE_V4,STAGE_B49,validate_builder_bytes as previous_validate':'from dk4tool.patch.hodram_outcomes_builder_guard_v5 import BUILDER,STAGE_V5,STAGE_B49_V2,validate_builder_bytes as previous_validate',
        source[a:b]:stages,source[c:d]:VALIDATOR,
        'Permit only exact preserved stages or one source-locked corrected B49 stage after compatible V8377.':'Permit exact preserved builders or one additive B50 stage after compatible outcomesv6/B49v3,with full original inverse.',
    })]
    paths=[guard]
    for area,name,before,after,changes in SPECS:
        src=Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{before}.py');dst=Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{after}.py')
        tools.append(derive(src,dst,changes));paths.append(dst)
    B49=Path('dk4tool/patch/hodram_B49_editorial_v3.py')
    tools.append(derive('dk4tool/patch/hodram_B49_editorial_v2.py',str(B49),{'hodram_outcomes_builder_guard_v5':'hodram_outcomes_builder_guard_v6'}));paths.append(B49)
    oldconfig=Path('translations/hodram_outcomes_editorial_release_v5.json');newconfig=Path('translations/hodram_outcomes_editorial_release_v6.json');assert not newconfig.exists()
    conf=read(oldconfig);before=dict(conf['dependencies'])
    for p in [oldconfig,Path(__file__),*paths]:
        key=str(p.resolve());digest=sha(p.read_bytes());assert key not in conf['dependencies'] or conf['dependencies'][key]==digest;conf['dependencies'][key]=digest
    assert all(conf['dependencies'][p]==h for p,h in before.items());save(newconfig,conf)
    oldB49=Path('translations/hodram_B49_editorial_release_v3.json');newB49=Path('translations/hodram_B49_editorial_release_v4.json');assert not newB49.exists()
    bc=read(oldB49);olddeps=dict(bc['dependencies'])
    for p,h in conf['dependencies'].items():assert p not in bc['dependencies'] or bc['dependencies'][p]==h;bc['dependencies'][p]=h
    for p in [oldB49,newconfig,guard,B49,Path(__file__)]:bc['dependencies'][str(p.resolve())]=sha(p.read_bytes())
    assert all(bc['dependencies'][p]==h for p,h in olddeps.items());save(newB49,bc)
    ROOT.mkdir(parents=True);save(ROOT/'source_equivalence.json',dict(derivations=tools,namespace_only_outcomes_derivations=tools[1:8],B49_guard_import_only_derivation=tools[-1],new_stage=stage,old_outcomes_configuration=str(oldconfig),old_outcomes_configuration_sha256=sha(oldconfig.read_bytes()),new_outcomes_configuration=str(newconfig),new_outcomes_configuration_sha256=sha(newconfig.read_bytes()),prior_outcomes_dependencies=len(before),new_outcomes_dependencies=len(conf['dependencies']),all524_prior_outcomes_dependencies_retained_exact=True,old_B49_configuration=str(oldB49),old_B49_configuration_sha256=sha(oldB49.read_bytes()),new_B49_configuration=str(newB49),new_B49_configuration_sha256=sha(newB49.read_bytes()),prior_B49_dependencies=len(olddeps),new_B49_dependencies=len(bc['dependencies']),all663_prior_B49_dependencies_retained_exact=True,all_prior_semantic_bodies_native_addresses_andmultiplicity_preserved=True,all_prior417_andB49445_frozen_contract_entries_preserved=True,guard_validation_full_prior_output_semantic_tests_andbuilder_edit_pending=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('Prepared additive B50 guard andnamespace-only outcomesv6/B49v3 successors;all524outcomes/663B49 prior dependencies retained.No builder/registry/ROM mutation.')
