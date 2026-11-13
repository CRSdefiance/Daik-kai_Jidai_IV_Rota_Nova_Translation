"""Freeze static evidence closure andprove one final Maria single-file commit matches the reference."""
from pathlib import Path
from dk4tool.patch import maria_B207_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.Maria_B207_final_paths_v7712 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_atomic_v7714')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    mapping=read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');clean=NdsImage.open('work/clean.nds')
    deps={str(p) for p in [*SEALED.values(),*APPROVED.values(),MAP,SEAL,APPROVAL,*map(Path,proofs().values()),Path(owned.__file__),Path('dk4tool/patch/maria_B207_atomic_support_v1.py'),Path('dk4tool/dialogue/maria_B207_profile_v1.py'),Path('dk4tool/dialogue/maria_B207_layout_v1.py'),Path('scripts/Maria_B207_final_paths_v7712.py'),Path('scripts/seal_Maria_B207_references_v7713.py'),Path(__file__)]}
    for path in SEALED.values():
        doc=read(path);deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file())
    deps.update(mapping['evidence'])
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',*[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
    while pending:
        path=pending.pop()
        if path in seen:continue
        seen.add(path)
        if Path(path).suffix!='.json':continue
        value=read(path)
        if not isinstance(value,dict):continue
        for key in ['evidence','dependencies']:
            if not isinstance(value.get(key),dict):continue
            for item in value[key]:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    deps={p for p in deps if Path(p).resolve() not in excluded}
    conf=dict(format='dk4-Maria-B207-editorial-release-v1',manuscripts=[str(p) for p in SEALED.values()],reference_map=str(MAP),reference_approval=str(SEAL),required_map_flags=owned.FLAGS,proofs=proofs(),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),canonical_ROM_sha256=sha(baseline.source.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),archives=[dict(file_path=g['file_path'],block=g['block'],source_sha256=g['source_archive_sha256'],target_sha256=g['target_archive_sha256'],canonical_sha256=sha(baseline.read_file(g['file_path'])),clean_sha256=sha(clean.read_file(g['file_path']))) for g in mapping['groups']],dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf)
    image=NdsImage.open(PARENT);original_list=image.rom.files;calls=[];commit=owned.commit_files
    def tracked(im,files):
        assert im is image and im.rom.files is original_list and files is not original_list
        calls.append(dict(changed_indices=[i for i,(a,b) in enumerate(zip(original_list,files,strict=True)) if a!=b]));return commit(im,files)
    owned.commit_files=tracked
    try:proof=owned.apply_release(image,baseline,config)
    finally:owned.commit_files=commit
    assert len(calls)==1 and len(calls[0]['changed_indices'])==1 and len(proof['changed_records'])==18
    assert [p for _,p,data in parent.iter_files() if image.read_file(p)!=data]==list(owned.PATHS) and all(image.read_file(p)==data for p,data in parent.iter_components())
    assert bytes(image.rom.save())==ROM.read_bytes() and sha(PARENT.read_bytes())==read('work/analysis/maria_B207_reference_v7698/research_image_receipt.json')['parent_sha256']
    save(ROOT/'positive_reconstruction.json',proof)
    save(ROOT/'positive_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=18,one_final_files_list_commit_after_complete_reconstruction=True,single_changed_file_indices=calls[0]['changed_indices'],all_other_files_components_exact=True,whole_ROM_equals_pinned_research_reference=True,static_dependency_count=len(conf['dependencies']),source1468_logical1468_tail0_target1472_logical1470_tail2_full_clean_andpredecessor_inverse=True,all18_actual_pages_complete_headers_andlate_limits_bound=True,production_negative_controls_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('18-record Maria positive reconstruction passes one single-file commit;whole ROM equals pinned research reference. All other files/components andparent preserved;production challenges pending.')
