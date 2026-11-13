"""Freeze immutable evidence closure and prove exactly one archive commit equals reference."""
from pathlib import Path
from dk4tool.patch import maria_story_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.Maria_story_final_paths_v7771 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_atomic_v7775')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');clean=NdsImage.open('work/clean.nds');mapping=read(MAP)
    deps={str(p) for p in [DRAFT,APPROVED,SEALED,MAP,APPROVAL,SEAL,*map(Path,proofs().values()),
        Path(owned.__file__),Path('dk4tool/patch/maria_story_reconstruction_v1.py'),
        Path('dk4tool/dialogue/maria_story_profile_v1.py'),Path('dk4tool/dialogue/maria_story_layout_v1.py'),
        Path('dk4tool/dialogue/maria_story_plan_v1.py'),Path('scripts/Maria_story_final_paths_v7771.py'),
        Path('scripts/seal_Maria_story_references_v7772.py'),Path(__file__)]}
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py',
        'translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',
        *[str(Path('docs')/name) for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
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
    conf=dict(format='dk4-Maria67-editorial-release-v1',manuscripts=[str(SEALED)],reference_map=str(MAP),reference_approval=str(SEAL),
        required_map_flags=owned.FLAGS,proofs=proofs(),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        predecessor_file_hashes={path:sha(value) for _,path,value in parent.iter_files()},
        predecessor_component_hashes={path:sha(value) for path,value in parent.iter_components()},
        canonical_ROM_sha256=sha(baseline.source.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),
        archives=[dict(file_path='/data/SC3.DK4',source_sha256=mapping['source_archive_sha256'],target_sha256=mapping['target_archive_sha256'],
            canonical_sha256=sha(baseline.read_file('/data/SC3.DK4')),clean_sha256=sha(clean.read_file('/data/SC3.DK4')))],
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf)
    image=NdsImage.open(PARENT);files=image.rom.files;calls=[];commit=owned.commit_files
    def tracked(im,values):
        assert im is image and im.rom.files is files and values is not files
        calls.append(dict(changed_indices=[i for i,(a,b) in enumerate(zip(files,values,strict=True)) if a!=b]))
        return commit(im,values)
    owned.commit_files=tracked
    try:proof=owned.apply_release(image,baseline,config)
    finally:owned.commit_files=commit
    assert len(calls)==1 and len(calls[0]['changed_indices'])==1 and len(proof['changed_records'])==67
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==list(owned.PATHS) and all(image.read_file(p)==v for p,v in parent.iter_components())
    assert bytes(image.rom.save())==ROM.read_bytes()
    save(ROOT/'positive_reconstruction.json',proof)
    save(ROOT/'positive_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),
        positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        positive_records=67,one_final_files_list_commit_after_complete_reconstruction=True,
        single_changed_file_indices=calls[0]['changed_indices'],all_other_files_components_exact=True,
        whole_ROM_equals_pinned_research_reference=True,static_dependency_count=len(conf['dependencies']),
        three_clean_predecessor_blocks_andwhole_archive_inverse_exact=True,production_negative_controls_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('67-record atomic positive:one final SC3 commit;whole ROM equals pinned reference.All other files/components exact;production challenges pending.')
