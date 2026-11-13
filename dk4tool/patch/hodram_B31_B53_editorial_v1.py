"""Plan the complete source-qualified B31_B53 exchange; commit one whole NDS after all gates."""
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import checked_dependency
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import validate_runtime,validate_approved_batch,profile_for
from dk4tool.dialogue.hodram_B31_B53_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.hodram_B31_B53_names_v1 import validate_scoped_names
from dk4tool.patch.hodram_B31_B53_references_v1 import reconstruct_and_bind
from dk4tool.patch.hodram_B31_B53_native_evidence_v1 import check_native_models
from dk4tool.patch.hodram_B31_B53_controls_v1 import check_controls
from dk4tool.patch.hodram_B31_B53_loaders_v1 import check_loaders_and_census
from dk4tool.patch.hodram_B31_B53_actual_evidence_v1 import check_actual
from dk4tool.patch.hodram_B31_B53_comparison_v1 import check_comparisons
from scripts.Hodram_B31_B53_release_paths_v8767 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs,observed_scope

PATH='/data/SC1.DK4'
CANONICAL=Path('out/raphael_natural_v2_accepted_base.nds')


def load(path):
    return json.loads(Path(path).read_bytes())


def require(value,message):
    if not value:raise ValueError('Hodram B31_B53 atomic contract: '+message)


def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():
        require(checked_dependency(Path(path),digest),'dependency:'+path)


def commit_image(image,rom):
    image.rom=rom


def plan_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Hodram-B31_B53-editorial-release-v1' and conf['manuscripts']==[str(DOC)] and conf['proofs']==proofs(),'exact source-qualified release configuration')
    require((conf['parent_ROM'],conf['reference_ROM'],conf['canonical_ROM'],conf['reference_approval'])==(str(PARENT),str(ROM),str(CANONICAL),str(SEAL)),'exact parent/reference/canonical/seal paths')
    require(sha(baseline.source.read_bytes())==sha(CANONICAL.read_bytes())==conf['canonical_ROM_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe','canonical baseline identity')
    require(conf['clean_ROM']=='work/clean.nds' and sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','clean Japanese identity')
    require(sha(PARENT.read_bytes())==conf['parent_ROM_sha256']==sha(bytes(image.rom.save())) and sha(ROM.read_bytes())==conf['reference_ROM_sha256'],'whole in-memory predecessor/reference identities')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'every predecessor file/component')
    frozen=validate_runtime(image);doc=load(DOC);validate_approved_batch(doc)
    data={k:load(p) for k,p in conf['proofs'].items()};seal=load(SEAL)
    require(data['native_contract']==frozen and data['names']==frozen['name_review_binding'],'frozen native andscoped-name approvals')
    validate_scoped_names(data['names'])
    require(seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['name_review_sha256']==sha(NAMES.read_bytes()) and seal['parent_sha256']==conf['parent_ROM_sha256'] and seal['reference_sha256']==conf['reference_ROM_sha256'],'sealed complete source/current/final lineage')
    require(doc['current_ROM_sha256']==conf['parent_ROM_sha256'] and doc['reference_ROM_sha256']==conf['reference_ROM_sha256'] and doc['source_current_final_references_complete'],'reviewed whole current/final identities')
    prior=data['predecessor_release']
    require(prior['profile']=='all-routes-unified-v8704' and prior['candidate_sha256']==conf['parent_ROM_sha256'] and prior['manifest_batches']==646 and prior['accepted_layers']==114 and prior['all18_registered_release_checks_pass'] and prior['all110_release_dialogue_regressions_pass'],'entire verified registered V8609 stack')
    require(sha(Path(prior['manifest']).read_bytes())==prior['manifest_sha256'] and prior['whole_clean_input_ROM_reconstruction_byte_exact'],'verified predecessor manifest/clean patch')
    dependency=conf['required_registered_stack_dependency']
    require(dependency==seal['required_registered_stack_dependency'] and dependency['profile']=='all-routes-unified-v8704' and dependency['ROM_sha256']==conf['parent_ROM_sha256'],'sealed complete registered prefix')
    for path,digest in dependency['configurations'].items():require(sha(Path(path).read_bytes())==digest,'preserved complete registered predecessor configuration:'+path)
    slot=data['Gerhard_reference']['only_changed_name_span'];arm=image.read_file('/__arm9__.bin');at=slot['offset']
    require(slot['bytes']==12 and arm[at:at+12].hex()==slot['target_hex'] and arm[at+12:at+20]==b'Blades\0\0' and sha(arm)==prior['ARM9_sha256'],'complete approved surname/following eight bytes/runtime')
    policy=data['policy_validation']
    require(policy['positive_editorial_units']==3 and len(policy['positive_speech_compilers'])==3 and policy['negative_count']==len(policy['negative_cases'])==236 and policy['all_frozen_dependency_guards_remained_enabled'],'three complete compiler positives and236 semantic rejections')
    counts={'independent_reconstruction':51,'independent_references':20,'independent_native':12,'independent_controls':12,'independent_loaders':8,'independent_actual':13,'independent_comparison':12}
    for key,count in counts.items():
        proof=data[key];require(len(proof['negative_cases'])==count and proof.get('negative_count',count)==count,'complete independent production challenge coverage:'+key)
        for path,digest in proof['evidence'].items():require(sha(Path(path).read_bytes())==digest,'independent immutable evidence:'+key+':'+path)
    archive=image.read_file(PATH);bank=IlnkContainer.parse(archive).blocks
    for row,positive in zip(doc['records'],policy['positive_speech_compilers'],strict=True):
        ident=row['id'];raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,bank[row['block']],ident,PATH,'progressive')
        encoded=encode_relocatable_dialogue(raw,row['planned_English_markup'],profile);qa=audit_relocatable_dialogue_record(raw,row['planned_English_markup'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==positive['compiled_hex'] and positive['id']==ident,'exact complete per-record compiler:'+ident)
        require(qa['base_QA_issues']==frozen['record_bindings'][ident]['base_QA_issues'] and qa['native_page_count']==1 and not qa['qa_waivers'] and not any(i['severity'] in ['warning','error'] for i in qa['issues']),'original full-width QA/bounds/pagination:'+ident)
    require(seal['records']==[{k:r[k] for k in ['id','source_reference','current_reference','final_reference','source_hex','current_hex','final_hex']} for r in doc['records']],'three sealed disjoint source/current/final prose references')
    clean,reference=NdsImage.open(conf['clean_ROM']),NdsImage.open(ROM)
    result=reconstruct_and_bind(image,clean,reference,doc,data,require)
    require(conf['archives']==[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=sha(result['target_archive']))] and conf['components']==[],'only owned SC1 archive/no code ornameasset changes')
    native=check_native_models(data,doc['records'],image,load,require)
    controls=check_controls(data,doc['records'],image,reference,result,native,load,require)
    loaders=check_loaders_and_census(data,image,reference,result,load,require)
    actual=check_actual(data,doc['records'],image,clean,result,native,load,require)
    comparison=check_comparisons(data,image,load,require)
    scope=observed_scope(data)
    require(scope==seal['observed_scope'] and scope['complete_page_occurrences']==4 and scope['complete_body_name_holds']==76 and scope['total_actual_frames']==24004 and scope['later_RGB_pairs']==[34,34] and scope['actual_unique_speech_IDs']==['DK4_MES_B31_R0018','DK4_MES_B53_R0007'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B31_R0013'],'every measured actual/offline/unforced alternate-path limit')
    approval=data['format_approval']
    require(approval['all3_five_gates_true'] and data['metadata']['predecessor_sha256']==approval['manuscript_sha256'] and data['metadata']['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes()),'complete individual formatting approval')
    for sheet in approval['measured_limits']['directly_viewed_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'directly reviewed complete scene/menu/header evidence')
    planned=deepcopy(image);planned.replace_file(PATH,result['target_archive']);validate_runtime(planned)
    require(bytes(planned.rom.save())==ROM.read_bytes(),'whole planned ROM equals reviewed pinned reference')
    require([p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[PATH] and all(planned.read_file(p)==v for p,v in image.iter_components()),'every unowned file/component exact')
    inverse=deepcopy(planned);inverse.replace_file(PATH,archive)
    require(bytes(inverse.rom.save())==bytes(image.rom.save()),'whole in-memory parent inverse inboth source lifecycles')
    changes=[dict(id=r['id'],file_path=PATH,block=r['block'],kind='progressive',old_offset=r['current_reference']['offset'],new_offset=r['final_reference']['offset']) for r in doc['records']]
    return planned.rom,dict(manuscripts=conf['manuscripts'],reference_approval=conf['reference_approval'],changed_records=changes,
        files=[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=sha(result['target_archive']),changed_records=changes)],
        one_complete_NDS_object_commit_after_all_gates=True,all18_commands3_preambles4_relatives1_query8_opaque2_normalends_andtails_preserved=True,
        all_clean_current_archive_andwhole_ROM_inverses_exact=True,explicit_complete_registered_V8704_dependency_preserved=True,
        native_summary=native['summary'],native_controls=controls,native_loaders=loaders,
        actual_summary=actual['summary'],comparison=comparison,actual_scope=scope,
        editorial_completion_credit_pending_registered_release=True,full_goal_complete=False)


def apply_release(image,baseline,config=CONFIG):
    try:planned,report=plan_release(image,baseline,config)
    except (KeyError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        raise ValueError('Hodram B31_B53 atomic contract: invalid orcontradictory evidence schema: '+str(exc)) from exc
    commit_image(image,planned)
    return report
