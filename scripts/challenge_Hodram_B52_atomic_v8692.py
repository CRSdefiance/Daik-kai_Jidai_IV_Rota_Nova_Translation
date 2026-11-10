"""Reach genuine semantic defects past the outer digest layer; preserve every native guard."""
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_B52_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_release_paths_v8693 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_atomic_challenges_v8692')


def digest(value):return sha(json.dumps(value,sort_keys=True,ensure_ascii=False).encode('utf-8'))


def setpath(value,path,new):
    for part in path[:-1]:value=value[part]
    value[path[-1]]=new


if __name__=='__main__':
    assert not ROOT.exists()
    conf=read(CONFIG);template=NdsImage.open(PARENT);baseline=NdsImage.open(owned.CANONICAL);paths=proofs()
    protected={Path(p) for p in conf['dependencies']}|{CONFIG,PARENT,ROM,DOC,NAMES,SEAL,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')}
    hashes={str(p):sha(p.read_bytes()) for p in protected}
    specs=[
        ('config-format',CONFIG,['format'],'unapproved-release','exact source-qualified release configuration'),
        ('config-parent',CONFIG,['parent_ROM_sha256'],'0'*64,'whole in-memory predecessor/reference identities'),
        ('config-prior-profile',CONFIG,['required_registered_stack_dependency','profile'],'incomplete-route','sealed complete registered prefix'),
        ('doc-context',DOC,['records',0,'context'],read(DOC)['records'][0]['context']+' Invented kinship.','Exact Hodram-B52 approved prose/source/context'),
        ('doc-English',DOC,['records',0,'english'],read(DOC)['records'][0]['english']+' Unapproved words.','Exact Hodram-B52 approved prose/source/context'),
        ('typed-choice-order',DOC,['typed_choice_records'],list(reversed(read(DOC)['typed_choice_records'])),'Exact complete ordered Hodram-B52 approved records'),
        ('sealed-record-order',SEAL,['records'],list(reversed(read(SEAL)['records'])),'five sealed disjoint prose/choice references'),
        ('current-block-bytes',Path(paths['current']),['groups',0,'current_block_hex'],'00'+read(paths['current'])['groups'][0]['current_block_hex'][2:],'complete literal source/current blocks'),
        ('relocation-source-hash',Path(paths['relocation']),['groups',0,'source_block_sha256'],'0'*64,'complete source/current block'),
        ('normal-value-carry',Path(paths['stored']),['distinct_seeded_ends',1,'native_result',1],0,'all fifty original distinct seeded ends andguard fields'),
        ('flagged-sixth-word',Path(paths['stored']),['distinct_seeded_ends',26,'native_result',5],1,'all fifty original distinct seeded ends andguard fields'),
        ('actual-menu-final-glyph-mask',Path(paths['menu_actual']),['groups',0,'samples',0,'labels',1,'independent_font_mask_sha256'],'0'*64,'independent complete caption-mask identity'),
        ('lost-body-name-hold',Path(paths['actual']),['groups',0,'speeches',0,'complete_holds'],read(paths['actual'])['groups'][0]['speeches'][0]['complete_holds'][:-1],'every independently reconstructed actual trace/hold/header/return/following-command field'),
        ('false-opposition-unvisited',Path(paths['opposition_actual']),['groups',1,'unvisited_conditional_text_IDs'],[],'exact observed andexplicitly unvisited case membership'),
        ('false-long-withdrawal-state-equality',Path(paths['comparison']),['groups',0,'five_native_component_equality','state'],True,'computed final component/actor equality'),
        ('false-sealed-scope',SEAL,['observed_scope','initialized_whole_script_fixtures_not_original_optional_event_activation_location_earned_progress'],False,'every measured actual/offline/long divergence/focused limit'),
    ]
    ROOT.mkdir(parents=True);cases=[]
    original_load,dependencies,commit=owned.load,owned.check_dependencies,owned.commit_image
    try:
        for index,(label,path,key,new,expected) in enumerate(specs):
            prior=read(path);changed=deepcopy(prior);setpath(changed,key,new)
            assert changed!=prior and digest(changed)!=digest(prior),label
            image=NdsImage(owned.CANONICAL,deepcopy(template.rom));original=image.rom
            before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()};calls=[]

            def intercepted(requested):
                return deepcopy(changed) if Path(requested).resolve()==path.resolve() else original_load(requested)

            def forbidden(*args):
                calls.append('forbidden');raise AssertionError('Semantic defect reached commit:'+label)

            owned.load=intercepted;owned.check_dependencies=lambda unused:None;owned.commit_image=forbidden
            try:owned.apply_release(image,baseline,CONFIG)
            except ValueError as error:
                message=str(error)
                assert expected in message,(label,expected,message)
                assert 'Native dependency changed' not in message and 'Frozen Hodram-B52 contract changed' not in message
            else:raise AssertionError('Changed semantic evidence accepted:'+label)
            finally:owned.load=original_load;owned.check_dependencies=dependencies;owned.commit_image=commit
            assert not calls and image.rom is original and bytes(original.save())==before and original.files==files and {p:v for p,v in image.iter_components()}==components
            row=dict(case=label,changed_evidence_path=str(path),original_value_sha256=digest(prior),changed_value_sha256=digest(changed),
                 actual_changed_input=True,rejected=True,error=message,expected_guard=expected,commit_calls=0,
                 original_object_identity_files_components_andserialized_bytes_unchanged=True,
                 only_outer_production_digest_layer_bypassed_all_frozen_native_source_editorial_andsemantic_guards_active=True)
            save(ROOT/f'case{index:02d}.json',row);cases.append(row);print('PASS',index+1,label,flush=True)
        assert hashes=={str(p):sha(p.read_bytes()) for p in protected}
        save(ROOT/'semantic_rejections.json',dict(cases=cases,negative_count=len(cases),
             every_challenge_changes_actual_data_andreaches_expected_semantic_guard=True,
             zero_commits_andwhole_original_input_object_exact_forall_failures=True,
             all_protected_files_ROMs_registry_ledger_pins_andmodules_hash_exact=True,
             no_frozen_native_source_editorial_orsemantic_guard_bypassed=True,
             only_outer_production_digest_layer_bypassed_to_reach_semantics=True,
             no_new_emulator_capture_ROM_registration_promotion_orcredit=True,
             full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    finally:owned.load=original_load;owned.check_dependencies=dependencies;owned.commit_image=commit
    print('B52 atomic:16 genuinely changed semantic defects reject before commit;whole original objects/files/components exact. Frozen guards active;no ROM/credit.')
