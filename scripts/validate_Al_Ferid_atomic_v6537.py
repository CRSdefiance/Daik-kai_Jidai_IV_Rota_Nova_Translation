"""Bind the exact reviewed additional-name asset after B210, before one component write."""
from pathlib import Path
from dk4tool.patch import Al_Ferid_name_release_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Al_Ferid_atomic_v6537')
PARENT=Path('out/lil_B210_reference_v6515_RESEARCH_ONLY.nds')
DOC=Path('translations/Al_Ferid_name_editorial_manuscript_v1.json')
SEAL=Path('work/analysis/Al_Ferid_target_view_v6523/approved_exact_name_typography_target_and_viewed_planes.json')
COMPAT=Path('work/analysis/B210_Ferid_compatibility_v6536/ten_final_B210_dispatches_exact_after_name_typography.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();doc=read(DOC);parent=NdsImage.open(PARENT);clean=NdsImage.open('work/clean.nds');baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    deps={str(p) for p in [DOC,SEAL,COMPAT,Path(doc['native_target_proof']),Path(owned.__file__).relative_to(Path.cwd()),Path(__file__).relative_to(Path.cwd()),'dk4tool/patch/main_pool_cache_visibility.py','scripts/Al_Ferid_exact_native_context_v6520.py']};excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',*[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
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
    conf=dict(format='dk4-Al-Ferid-name-release-v1',manuscript=str(DOC),approval=str(SEAL),native_proof=doc['native_target_proof'],B210_compatibility=str(COMPAT),source_files={p:sha(v) for _,p,v in parent.iter_files()},source_components={p:sha(v) for p,v in parent.iter_components()},canonical_ARM9_sha256=sha(baseline.read_file(owned.PATH)),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_ARM9_sha256=sha(clean.read_file(owned.PATH)),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps) if Path(p).resolve() not in excluded})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf);image=NdsImage.open(PARENT);calls=[];replace=image.replace_file
    def tracked(*args,**kwargs):calls.append(args[0]);return replace(*args,**kwargs)
    image.replace_file=tracked;proof=owned.apply_release(image,baseline,config)
    assert calls==[owned.PATH] and len(proof['changed_records'])==1 and image.read_file(owned.PATH)==NdsImage.open(doc['approved_target_research_ROM']).read_file(owned.PATH)
    assert all(image.read_file(p)==v for _,p,v in parent.iter_files()) and [p for p,v in parent.iter_components() if image.read_file(p)!=v]==[owned.PATH]
    save(ROOT/'positive_reconstruction.json',proof);save(ROOT/'positive_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=1,one_component_write_after_all_gates=True,all_other_files_components_exact=True,five_owned_bytes_changed_seven_byte_slot_and_full_inverse=True,negative_controls_pending=True,full_goal_complete=False));print('One exact Ferid field passes atomic reconstruction after B210; five owned bytes and no other asset change. Semantic negatives next.')
