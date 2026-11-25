"""Preserve complete existing tea/recovery exchanges in disclosed target-label B22 fixtures."""
import json,os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_label_fixtures_v5882')
PARENT=Path('out/generic_speaker_labels_v5881_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read('work/analysis/generic_speaker_labels_research_v5881/research_image_receipt.json')
    assert sha(PARENT.read_bytes())==receipt['research_ROM_sha256'];parent=NdsImage.open(PARENT);arm=parent.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;inventory,_,_=scoped_inventory()
    init,_=inventory(arm,blocks[22]);first=next(c['offset'] for c in init if c['word']==0x4000);assert first==56 and len(init[:9])==9
    prelude=blocks[22][8:first];fixtures=[]
    assert not any(Path(f'out/generic_labels_{case}_v5882_RESEARCH_ONLY.nds').exists() for case in ['tea','recovery'])
    for case,number,expected_commands,expected_speeches in [('tea',184,12,9),('recovery',200,31,19)]:
        original=blocks[number];source_commands,source_speeches=inventory(arm,original);end=8+struct.unpack_from('<H',original,4)[0]
        assert len(source_commands)==expected_commands and len(source_speeches)==expected_speeches
        assert source_commands[-1]['word']==0 and source_commands[-1]['offset']+4==end
        logical=bytearray(blocks[22][:8]+prelude+original[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
        payload=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(arm,payload)
        assert len(commands)==expected_commands+9 and len(speeches)==expected_speeches
        mapped=[];texts=[]
        for ordinal,c in enumerate(source_commands):
            at=c['offset']+first-8;m=next(r for r in commands if r['offset']==at)
            assert m['whole_command_hex']==c['whole_command_hex'] and m['word']==c['word'] and m['native_extent']==c['native_extent']
            assert m['ancestor_0100_offsets']==[a+first-8 for a in c['ancestor_0100_offsets']]
            ident=None
            if c['word']==0x4000:
                ident=f'{case}_B{number}_speech{len(texts):02d}';p=c['offset']+5;raw=original[p:original.index(0,p+1)]
                texts.append(dict(id=ident,source_block=number,source_record_index=original[:p].count(b'\0'),source_selector=raw[0],
                    current_text_hex=raw.hex(),fixture_command_offset=at,native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex']))
            mapped.append(dict(source_block=number,source_offset=c['offset'],source_word=c['word'],fixture_offset=at,
                native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex'],text_ID=ident))
        expected={164,165,254} if case=='tea' else {19,172,254};assert {r['source_selector'] for r in texts}==expected
        after=list(blocks);after[22]=payload;rom=Path(f'out/generic_labels_{case}_v5882_RESEARCH_ONLY.nds')
        image=NdsImage.open(PARENT);image.replace_file('/data/SC2.DK4',IlnkContainer(after).to_bytes());image.save(rom);saved=NdsImage.open(rom)
        check=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
        assert [i for i,(a,b) in enumerate(zip(blocks,check,strict=True)) if a!=b]==[22]
        assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
        fixtures.append(dict(case=case,source_block=number,research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
            source_block_hex=original.hex(),source_block_sha256=sha(original),all_original_native_commands=source_commands,
            fixture_block=22,fixture_block_hex=payload.hex(),fixture_block_sha256=sha(payload),original_B22_prelude_hex=prelude.hex(),
            original_B22_prelude_commands=init[:9],selected_original_objects=mapped,original_text_records=texts,explicitly_excluded_original_commands=[],
            all_stored_fixture_commands=commands,original_source_speech_count=expected_speeches,original_source_command_count=expected_commands,
            all_existing_speech_bytes_complete_controls_and_effect_results_unforced=True,native_target_labels=[164,165] if case=='tea' else [172]))
    ROOT.mkdir(parents=True);save(ROOT/'two_complete_existing_exchanges_with_target_name_data.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),fixtures=fixtures,
        target_Man_Woman_Stranger_primary_data_only_all_other_names_and_prose_unchanged=True,
        all_source_commands_complete_exchanges_and_original_initializers_retained=True,
        initialized_Amsterdam_B22_fixture_not_natural_event184_or200_activation_or_original_location=True,
        no_save_state_RAM_roster_funds_RNG_predicate_result_or_effect_fixture=True,
        tea_C200_source_command_retained_not_a_new_effect_semantics_claim=True,not_registered_candidate_or_release_parent=True,
        producer_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,new_name_or_dialogue_credit=0,full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);(ROOT/'pins.before.json').write_bytes(raw)
    for f in fixtures:
        p=Path(f['research_ROM']);assert not any(Path(r['path']).resolve()==p.resolve() for r in values)
        values.append(dict(path=str(p.resolve()),reason='Complete '+f['case']+' target-name display fixture. Preserve every ROM. SHA256 '+f['research_ROM_sha256']))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');assert pins.read_bytes()==raw
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROMs=[f['research_ROM'] for f in fixtures],all_prior_pins_preserved=True,ROMs_deleted=0,
        before_sha256=sha(raw),after_sha256=sha(encoded),full_goal_complete=False))
    print('Pinned two complete target-name fixtures:tea12 commands/nine speeches,recovery31/19,plus nine unchanged initializers each. No dialogue/effect forcing or credit.')
