"""Pinned research-only full reference:6 reviewed speeches intwo SC1 blocks; every other file/component exact."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_reference_v8329')
ROM=Path('out/Hodram_B47_B48_reference_v8329_RESEARCH_ONLY.nds')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v2.json')
MAP=Path('work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json')
STORED=Path('work/analysis/Hodram_outcome_stored_v8327/six_stored_bodies8_fresh16_reused_alignments_six_exact_native_pages.json')
CONTROLS=Path('work/analysis/Hodram_outcome_final_dispatch_v8328/six_final_dispatches9_exact_nontext_commands_FE_FI_andcomplete_ends.json')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();doc,mapping,stored,controls=map(read,[DOC,MAP,STORED,CONTROLS])
    assert stored['relocation_sha256']==controls['relocation_sha256']==sha(MAP.read_bytes()) and len(controls['final_dispatches'])==6
    parentpath=Path(doc['current_ROM']);assert sha(parentpath.read_bytes())==doc['current_ROM_sha256']==mapping['candidate_sha256']
    parent=NdsImage.open(parentpath);image=deepcopy(parent);file=doc['file_path'];old=parent.read_file(file);target=Path(mapping['target_archive']).read_bytes()
    assert sha(old)==mapping['source_archive_sha256'] and sha(target)==mapping['target_archive_sha256']
    a,b=[IlnkContainer.parse(v).blocks for v in [old,target]];assert len(a)==len(b)==325 and [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[47,48]
    image.replace_file(file,target);assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[file] and all(image.read_file(p)==v for p,v in parent.iter_components())
    restored=deepcopy(image);restored.replace_file(file,old);assert bytes(restored.rom.save())==parentpath.read_bytes()
    raw=bytes(image.rom.save());ROOT.mkdir(parents=True);ROM.write_bytes(raw);assert sha(ROM.read_bytes())==sha(raw)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);assert not any(Path(p['path']).resolve()==ROM.resolve() for p in values)
    updated=values+[dict(path=str(ROM.resolve()),reason='Hodram6two-block source/context reviewed reference;onlySC1B47/B48,allotherfiles/components exact/fullparentinverse. Unregistered/research-only;actualFE/scene-controls/nameheaders/loader/census/policy/atomic/release gates pending. Preserve every ROM. SHA256 '+sha(raw))]
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())[:-1]==values
    save(ROOT/'research_image_receipt.json',dict(parent=str(parentpath),parent_sha256=doc['current_ROM_sha256'],research_ROM=str(ROM),research_ROM_sha256=sha(raw),
        current_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),research_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),only_changed_files=[file],only_changed_components=[],only_changed_blocks=[47,48],
        source_relocation_plan=str(MAP),source_relocation_plan_sha256=sha(MAP.read_bytes()),source_SC1_sha256=sha(old),target_SC1_sha256=sha(target),
        all323_other_SC1_blocks_all_other_files_andall_components_exact=True,full_ROM_inverse_recovers_every_parent_byte=True,
        all6_complete_speaker_preambles15commands_zero_relative_queries_one_FE_one_FI_andfullends_preserved=True,
        current_Adernkatz_Blades_andall_registered_V8300_name_assets_unchanged=True,all_prior_ROM_pins_preserved=True,
        pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),registered_candidate=False,not_for_handoff_ornew_parent=True,currentregistered_V8300_andmainV4701_unchanged=True,
        loaders_caller_census_actual_FE_scene_effects_nameheaders_policy_atomic_registered_release_pending=True,
        new_credit=0,new_emulator_runs=0,new_ROMs=1,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,MAP,STORED,CONTROLS,Path(__file__)]}))
    print('PinnedresearchHodram6 reference;onlySC1twoblocks change/323others/components exact/fullparentROM inverse.CurrentV8300 unchanged;not a release.')
