"""Freeze immutable evidence and validate one final ARM9 write, leaving every file intact."""
from pathlib import Path
from dk4tool.patch import square_shopkeeper_label_release_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_shopkeeper_atomic_v7026b')
DOC=Path('translations/square_shopkeeper_label_manuscript_v4.json')
APPROVAL=Path('work/analysis/square_shopkeeper_approval_v7025/ten_label_approval.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();doc=read(DOC);seal=read(APPROVAL)
    parent_path=Path(doc['current_ROM']);parent=NdsImage.open(parent_path);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');clean=NdsImage.open('work/clean.nds')
    assert sha(parent_path.read_bytes())==doc['current_ROM_sha256'];reference=Path(doc['target_research_ROM'])
    deps={str(p) for p in [DOC,APPROVAL,Path(owned.__file__),Path('dk4tool/patch/square_shopkeeper_label_data_v1.py'),Path(__file__),
        Path('scripts/square_shopkeeper_exact_native_context_v7020.py'),Path('scripts/square_shopkeeper_name_style_v7020.py'),Path('scripts/square_shopkeeper_font_oracles_v7020.py'),
        Path('work/analysis/square_shopkeeper_origin_v7024b/exact_native_origin_and_source_locked_successor.json')]}
    deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file())
    actual,names,view=[read(doc[k]) for k in ['actual_scenes','native_names','visual_review']]
    deps.update(p['path'] for p in view['viewed_images'])
    for row in actual['native_pages'].values():deps.update(p['native_plane'] for p in row['pages'])
    deps.update(p['plane'] for p in actual['native_name_planes'].values())
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py',
        'translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',
        *[str(Path('docs')/p) for p in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
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
    deps={p for p in deps if Path(p).resolve() not in excluded}
    conf=dict(format=owned.FORMAT,manuscript=str(DOC),approval=str(APPROVAL),names=doc['native_names'],actual=doc['actual_scenes'],view=doc['visual_review'],
        source_ARM9_sha256=sha(parent.read_file(owned.PATH)),target_ARM9_sha256=doc['target_ARM9_sha256'],
        source_files={p:sha(v) for _,p,v in parent.iter_files()},source_components={p:sha(v) for p,v in parent.iter_components()},
        canonical_ARM9_sha256=sha(baseline.read_file(owned.PATH)),clean_ARM9_sha256=sha(clean.read_file(owned.PATH)),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        reference_ROM=str(reference),reference_ROM_sha256=sha(reference.read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf)
    image=NdsImage.open(parent_path);writes=[];replace=image.replace_file
    def tracked(*args,**kwargs):writes.append(args[0]);return replace(*args,**kwargs)
    image.replace_file=tracked;proof=owned.apply_release(image,baseline,config);target=NdsImage.open(reference)
    assert writes==[owned.PATH] and len(proof['changed_records'])==10 and image.read_file(owned.PATH)==target.read_file(owned.PATH)
    assert all(image.read_file(p)==v for _,p,v in parent.iter_files())
    assert [p for p,v in parent.iter_components() if image.read_file(p)!=v]==[owned.PATH]
    save(ROOT/'positive_proof.json',proof)
    save(ROOT/'positive_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),parent_ROM=str(parent_path),parent_ROM_sha256=sha(parent_path.read_bytes()),
        positive_proof=str(ROOT/'positive_proof.json'),positive_proof_sha256=sha((ROOT/'positive_proof.json').read_bytes()),positive_records=10,archive_writes=writes,dependency_count=len(deps),
        exact18_owned_byte_changes_two_literal_prefixes_all621_pointers_and_unread_tails_preserved=True,all_files_and_other_components_exact=True,new_ROMs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(positive_records=10,archive_writes=writes,dependencies=len(deps),all_other_assets_exact=True),flush=True)
