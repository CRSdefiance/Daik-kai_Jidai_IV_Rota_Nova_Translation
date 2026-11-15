"""Bind the immutable B209 evidence and reconstruct its target with a single archive write."""
from pathlib import Path
from dk4tool.patch import lil_B209_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B209_references_v6481 import MAP,PARENT,ROM,ENTRY,LOADER,CENSUS,CONTROL
from scripts.prepare_lil_B209_workflow_v6484 import OUTPUT as DOC,SEAL
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_atomic_v6485b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();doc,mapping=read(DOC),read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');clean=NdsImage.open('work/clean.nds')
    deps={str(p) for p in [DOC,MAP,SEAL,ENTRY,LOADER,CENSUS,CONTROL,Path(owned.__file__).relative_to(Path.cwd()),Path(__file__).relative_to(Path.cwd()),'scripts/prepare_lil_B209_workflow_v6484.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md',doc['native_profile_module'],doc['native_formatter_module'],doc['native_policy_contract'],doc['native_approval'],doc['actual_English_proof'],doc['actual_English_view']]}
    deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file());deps.update(mapping['evidence'])
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',*[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        d=read(p)
        if not isinstance(d,dict):continue
        for k in ['evidence','dependencies']:
            for item in d.get(k,{}) if isinstance(d.get(k),dict) else []:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    deps={p for p in deps if Path(p).resolve() not in excluded}
    conf=dict(format='dk4-lil-B209-editorial-release-v2',manuscript=str(DOC),reference_map=str(MAP),reference_approval=str(SEAL),controls=str(CONTROL),entry=str(ENTRY),loader=str(LOADER),census=str(CENSUS),required_map_flags=owned.FLAGS,
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=sha(baseline.read_file(owned.PATH)),clean_SC2_sha256=sha(clean.read_file(owned.PATH)),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf);image=NdsImage.open(PARENT);calls=[];replace=image.replace_file
    def tracked(*args,**kwargs):calls.append(args[0]);return replace(*args,**kwargs)
    image.replace_file=tracked;proof=owned.apply_release(image,baseline,config)
    assert calls==[owned.PATH] and len(proof['changed_records'])==20 and image.read_file(owned.PATH)==NdsImage.open(ROM).read_file(owned.PATH)
    assert all(image.read_file(p)==data for _,p,data in parent.iter_files() if p!=owned.PATH) and all(image.read_file(p)==data for p,data in parent.iter_components())
    save(ROOT/'positive_reconstruction.json',proof);save(ROOT/'positive_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=20,one_archive_write_after_all_gates=True,all_other_files_components_exact=True,source1148_bytes_inverse_recovered=True,negative_controls_pending=True,full_goal_complete=False));print('B20920-object positive reconstruction:one archive write after all gates,all1148 predecessor bytes reversible,all other files/components exact. Semantic negatives next.')
