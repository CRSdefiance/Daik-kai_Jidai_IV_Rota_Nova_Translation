"""Rebuild only B152; preserve the other23 reviewed blocks and the qualified FE repair."""
from copy import deepcopy
from pathlib import Path
import os
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'reconstruction_v3';assert not out.exists()
    priorpath=ROOT/'reconstruction_v2/reconstruction.json';prior=load(priorpath)
    docpath=ROOT/'formatting_v2/formatting_input.json';doc=load(docpath)
    planpath=ROOT/'plan_wine_v4/automatic_plans.json';plan=load(planpath)
    nativepath=ROOT/'final_native_v2.json';native=load(nativepath)
    approvalpath=ROOT/'offline_display_approval_v2.json';approval=load(approvalpath)
    assert approval['all373_final_pages_directly_viewed'] and approval['all_names_and17_captions_directly_viewed']
    assert native['manuscript_sha256']==plan['manuscript_sha256']==digest(docpath)
    assert native['plan_sha256']==digest(planpath) and doc['runtime']==native['runtime']
    image=NdsImage.open(prior['research_ROM']);parent=NdsImage.open(prior['parent']);clean=NdsImage.open('work/clean.nds')
    assert digest(prior['research_ROM'])==prior['research_ROM_sha256'] and digest(prior['parent'])==prior['parent_sha256']==doc['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');assert arm==parent.read_file('/__arm9__.bin')
    oldarchive=image.read_file('/data/SC3.DK4');blocks=list(IlnkContainer.parse(oldarchive).blocks)
    cleanblock=IlnkContainer.parse(clean.read_file('/data/SC3.DK4')).blocks[152]
    currentblock=IlnkContainer.parse(parent.read_file('/data/SC3.DK4')).blocks[152]
    inventory,_,_=scoped_inventory();rows=deepcopy([r for r in doc['records'] if r['block']==152])
    assert len(rows)==14 and all(r['kind']!='typed-choice-label' for r in rows)
    for r in rows:r['current_record_index']=r['current_reference']['record_index']
    plans={r['id']:r for r in plan['records']}
    target,proof=rebuild_block(arm,cleanblock,currentblock,rows,plans,inventory,[])
    assert len(target)<=9216 and target!=blocks[152]
    oldgroup=next(g for g in prior['groups'] if g['block']==152)
    assert sha(blocks[152])==oldgroup['target_sha256']
    oldtexts={r['id']:r for r in oldgroup['text_records']}
    assert [r['id'] for r in proof['text_records'] if r['compiled_hex']!=oldtexts[r['id']]['compiled_hex']]==['DK4_MES_B152_R0008']
    out.mkdir();blockpath=out/'B152_RESEARCH_ONLY.bin';blockpath.write_bytes(target)
    new=deepcopy(prior)
    group=dict(block=152,file_path='/data/SC3.DK4',current_sha256=sha(currentblock),clean_sha256=sha(cleanblock),
        target_sha256=sha(target),target_block=str(blockpath),current_bytes=len(currentblock),target_bytes=len(target),**proof)
    new['groups']=[group if g['block']==152 else g for g in new['groups']]
    assert all(a==b for a,b in zip(prior['groups'],new['groups'],strict=True) if a['block']!=152)
    blocks[152]=target;resource=IlnkContainer(blocks).to_bytes()
    inverse=list(blocks);inverse[152]=IlnkContainer.parse(oldarchive).blocks[152]
    assert IlnkContainer(inverse).to_bytes()==oldarchive
    image.replace_file('/data/SC3.DK4',resource)
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==['/data/SC3.DK4']
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    rom=out/'reviewed_RESEARCH_ONLY.nds';image.save(rom)
    reopened=NdsImage.open(rom);assert reopened.read_file('/data/SC3.DK4')==resource
    reopened.replace_file('/data/SC3.DK4',parent.read_file('/data/SC3.DK4'))
    assert bytes(reopened.rom.save())==Path(prior['parent']).read_bytes()
    archivepath=out/'reviewed_RESEARCH_ONLY.DK4';archivepath.write_bytes(resource)
    new.update(target_archive=str(archivepath),target_archive_sha256=sha(resource),research_ROM=str(rom),research_ROM_sha256=digest(rom),
        previous_wine_reconstruction=str(priorpath),previous_wine_reconstruction_sha256=digest(priorpath),
        manuscript=str(docpath),manuscript_sha256=digest(docpath),source_manuscript=str(docpath),source_manuscript_sha256=digest(docpath),
        plan=str(planpath),plan_sha256=digest(planpath),native=str(nativepath),native_sha256=digest(nativepath),
        menu=str(ROOT/'menu_native_approved_v3.json'),menu_sha256=digest(ROOT/'menu_native_approved_v3.json'),
        styles=str(ROOT/'compiled_styles_v2/compiled_style_objects.json'),styles_sha256=digest(ROOT/'compiled_styles_v2/compiled_style_objects.json'),
        exact_other23_reconstruction_groups_reused=True,only_reopened_wine_reply_compiled_bytes_change=True,
        complete_B152_source_current_native_rebuild_andinverse_fresh=True,
        full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,
        composed_block_archive_andserialized_parent_inverses_exact=True,
        all373_compiled_native_pages_unchanged=False,changed_compiled_page_IDs=['DK4_MES_B152_R0008'],
        stored_catalogue_loaders_gameplay_andregistered_release_pending=True,new_credit=0)
    new['evidence'].update({str(p):digest(p) for p in [priorpath,docpath,planpath,nativepath,approvalpath,Path(__file__)]})
    save(out/'reconstruction.json',new)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    absolute=str(rom.resolve());assert not any(v['path']==absolute for v in values)
    values.append(dict(path=absolute,reason='Preserve Maria390 source-faithful wine reply amendment;SHA256 '+digest(rom)))
    (out/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.Maria390wine.pending.json')
    assert not pending.exists();save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    print('Rebuilt B152 only;23 exact groups andFE padding repair reused;complete inverses pass.',digest(rom))


if __name__=='__main__':main()
