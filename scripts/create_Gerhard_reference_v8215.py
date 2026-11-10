"""Pinned isolated research image for actual name/body tests; never a registered handoff or parent."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_reference_v8215')
ROM=Path('out/Gerhard_Adernkatz_reference_v8215_RESEARCH_ONLY.nds')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8213/verified_handoff.json')
MAP=Path('work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json')
OWNERSHIP=Path('work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json')
STORED=Path('work/analysis/Gerhard_stored_v8209/5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json')
CONTROLS=Path('work/analysis/Gerhard_final_controls_v8214/5_final_dispatches51_controls30_raw_evaluations150_seeded_ends.json')
NAME=Path('work/analysis/Gerhard_target_name_v8210c/owned12byte_input8_getters4_complete_name_planes_Blades_protected.json')
NAMEVIEW=Path('work/analysis/Gerhard_name_view_v8211/four_name_planes_directly_viewed_research_input_only.json')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();prior,plan,ownership,stored,controls,name,view=map(read,[PRIOR,MAP,OWNERSHIP,STORED,CONTROLS,NAME,NAMEVIEW])
    ledger=read('translations/editorial_review_current_v1.json');candidate=ledger['current_integrated_candidate']
    parentpath=Path(prior['candidate']);manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert ledger['records_editorially_completed']==7171 and sha(parentpath.read_bytes())==candidate['sha256']==prior['candidate_sha256']==plan['candidate_sha256']==ownership['candidate_sha256']
    assert candidate['profile']=='all-routes-unified-v8172' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==639 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert stored['relocation_sha256']==controls['relocation_sha256']==sha(MAP.read_bytes())
    assert len(controls['final_dispatches'])==5 and controls['raw_native_evaluations']==30 and controls['normal_seeded_end_cases']==150
    assert view['viewed'] and view['name_proof_sha256']==sha(NAME.read_bytes()) and name['protected_Blades_bytes_andall_other_RAM_exact']
    archive=Path(plan['target_archive']).read_bytes();assert sha(archive)==plan['target_archive_sha256']
    parent,image=NdsImage.open(parentpath),NdsImage.open(parentpath);oldarchive=parent.read_file(plan['file_path']);oldarm=parent.read_file('/__arm9__.bin')
    assert sha(oldarchive)==plan['source_archive_sha256'] and sha(oldarm)==ownership['ARM9_sha256']
    slot=ownership['current_owned_name_span'];at=slot['offset'];old,new=bytes.fromhex(slot['current_hex']),bytes.fromhex(slot['target_hex'])
    assert len(old)==len(new)==slot['bytes']==12 and oldarm[at:at+12]==old and oldarm[at+12:at+20]==b'Blades\0\0'
    arm=bytearray(oldarm);arm[at:at+12]=new
    assert sha(bytes(arm))==ownership['proposed_ARM9_sha256']==name['proposed_ARM9_sha256']
    assert arm[:at]==oldarm[:at] and arm[at+12:]==oldarm[at+12:]
    image.replace_file(plan['file_path'],archive);image.replace_file('/__arm9__.bin',bytes(arm));image.save(ROM);saved=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4']
    assert [p for p,v in parent.iter_components() if saved.read_file(p)!=v]==['/__arm9__.bin']
    source_blocks,target_blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,saved]]
    assert len(source_blocks)==len(target_blocks)==336 and [i for i,(a,b) in enumerate(zip(source_blocks,target_blocks,strict=True)) if a!=b]==[27,74]
    for group in plan['groups']:assert sha(target_blocks[group['block']])==group['target_block_sha256']
    restored=NdsImage.open(ROM);restored.replace_file('/__arm9__.bin',oldarm);restored.replace_file('/data/SC2.DK4',oldarchive)
    assert bytes(restored.rom.save())==parentpath.read_bytes()
    consumers=[]
    for path,data in [(p,v) for _,p,v in saved.iter_files()]+list(saved.iter_components()):
        assert b'Ardelknatts' not in data and b'Ardelnkatts' not in data
        start=0
        while True:
            pos=data.find(b'Adernkatz',start)
            if pos<0:break
            consumers.append(dict(file_path=path,offset=pos));start=pos+1
    assert len(consumers)==20
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    updated=values+[dict(path=str(ROM.resolve()),reason='Gerhard Adernkatz isolated research reference from registeredV8172;only owned12-byte surname/Blades protected and5 SC2 speeches. Allother assets exact/full ROM inverse. Not a separate unified test package,registered release,new parent,promotion orhandoff. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))]
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    (ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-1]==values
    save(ROOT/'research_image_receipt.json',dict(
        parent=str(parentpath),parent_sha256=sha(parentpath.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        current_ARM9_sha256=sha(oldarm),research_ARM9_sha256=sha(bytes(arm)),source_relocation_plan=str(MAP),source_relocation_plan_sha256=sha(MAP.read_bytes()),
        only_changed_files=['/data/SC2.DK4'],only_changed_components=['/__arm9__.bin'],only_changed_blocks=[27,74],only_changed_name_span=slot,
        all334_other_SC2_blocks125_other_speeches_andall_other_files_components_exact=True,
        every_ARM9_byte_outside_owned12_andBlades_pointer_andtext_exact=True,
        full_ROM_inverse_recovers_every_parent_byte=True,all20_Adernkatz_consumers=consumers,no_Ardelknatts_orArdelnkatts_remaining_in_image=True,
        all_prior_ROM_pins_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),
        registered_candidate=False,not_for_handoff_ornew_parent=True,currentregistered_V8172_andmainV4701_unchanged=True,
        fresh_own_research_startup_context_full_loaders_callers_actual_policy_atomic_registered_release_pending=True,
        native_name_data_overlay_proof_is_not_relabelled_as_actual_ROM_startup=True,
        new_credit=0,new_emulator_runs=0,new_ROMs=1,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,MAP,OWNERSHIP,STORED,CONTROLS,NAME,NAMEVIEW,Path(__file__)]}))
    print('Pinned research reference;20 consistent Adernkatz occurrences;only12-byte ARM9 name and5 SC2 bodies;full ROM inverse pass.Current/main unchanged.')
