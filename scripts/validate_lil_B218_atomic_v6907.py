"""Close immutable dependencies and require exactly one final archive write for the sealed batch."""
from pathlib import Path
from dk4tool.patch import lil_B218_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B218_references_v6905 import OUTPUT as DOC,MAP,PARENT,ROM,ENTRY,LOADER,CENSUS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B218_atomic_v6907')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();doc,mapping=read(DOC),read(MAP);seal=Path(doc['reference_approval']);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');clean=NdsImage.open('work/clean.nds');deps={str(p) for p in [DOC,MAP,seal,ENTRY,LOADER,CENSUS,Path(owned.__file__),Path(__file__),Path('scripts/seal_lil_B218_references_v6905.py'),Path(doc['native_policy_contract']),Path(doc['native_profile_module']),Path(doc['native_formatter_module']),Path(doc['later_scope_proof'])]};deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file());deps.update(mapping['evidence']);excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',*[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]};pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        d=read(p)
        if not isinstance(d,dict):continue
        for key in ['evidence','dependencies']:
            for item in d.get(key,{}) if isinstance(d.get(key),dict) else []:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    deps={p for p in deps if Path(p).resolve() not in excluded};conf=dict(format='dk4-lil-B218-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),reference_approval=str(seal),controls=doc['relocated_control_proof'],entry=str(ENTRY),loader=str(LOADER),census=str(CENSUS),required_map_flags=owned.FLAGS,required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=sha(baseline.read_file(owned.PATH)),clean_SC2_sha256=sha(clean.read_file(owned.PATH)),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf);image=NdsImage.open(PARENT);calls=[];replace=image.replace_file
    def tracked(*args,**kwargs):calls.append(args[0]);return replace(*args,**kwargs)
    image.replace_file=tracked;proof=owned.apply_release(image,baseline,config);reference=NdsImage.open(ROM);assert calls==[owned.PATH] and len(proof['changed_records'])==13 and image.read_file(owned.PATH)==reference.read_file(owned.PATH) and [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[owned.PATH] and all(image.read_file(p)==v for p,v in parent.iter_components());save(ROOT/'positive_proof.json',proof);save(ROOT/'positive_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_proof=str(ROOT/'positive_proof.json'),positive_proof_sha256=sha((ROOT/'positive_proof.json').read_bytes()),positive_records=13,archive_writes=calls,source1088_bytes_inverse_recovered=True,all335_other_blocks_files_components_preserved=True,dependency_count=len(deps),new_ROMs=0,new_credit=0,full_goal_complete=False));print('Atomic positive:13 records,one final archive write,complete1088-byte inverse; every other block/file/component preserved.')
