"""Paired whole-script fixtures with the original nine-command Lil opening prelude; no forced conditions."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_scene_fixtures_v8224')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
MAP=Path('work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
CENSUS=Path('work/analysis/Gerhard_surname_consumers_v8196/all20_current_Latin_occurrences_five_whole_clean_exchanges.json')
LOADERS=Path('work/analysis/Gerhard_loaders_v8222/336_whole_native_loads_cache_hits672_initial_parent_modes.json')
CALLERS=Path('work/analysis/Gerhard_reference_census_v8223/all225_commands44_relative_sites_five_revisions_EV2_entries_shipped_callers.json')
if __name__=='__main__':
    assert not ROOT.exists();reference,mapping,current,census,loaders,callers=map(read,[REFERENCE,MAP,CURRENT,CENSUS,LOADERS,CALLERS])
    assert loaders['fresh_native_whole_loads_andcache_hits']==336 and callers['all225_source_current_target_commands44_relative_sites_bound_to_research_ROM']
    parents={v:Path(reference[k]) for v,k in [('parent_English','parent'),('revised_English','research_ROM')]}
    images={v:NdsImage.open(p) for v,p in parents.items()}
    for v,p in parents.items():assert sha(p.read_bytes())==reference['parent_sha256' if v=='parent_English' else 'research_ROM_sha256']
    clean=NdsImage.open('work/clean.nds');file='/data/SC2.DK4';inventory,_,_=scoped_inventory()
    baseline=images['parent_English'];bank=IlnkContainer.parse(baseline.read_file(file)).blocks;opening=bank[22]
    commands,speeches=inventory(baseline.read_file('/__arm9__.bin'),opening);first=speeches[0]['offset'];prelude=opening[8:first];delta=len(prelude)
    initializers=[c for c in commands if c['offset']<first]
    assert first==56 and delta==48 and len(initializers)==9
    assert prelude==IlnkContainer.parse(clean.read_file(file)).blocks[22][8:first]
    assert all(c['word'] not in [0x4000,0x100,0x200,0x300,0x400,0x8000,0x8100,0] for c in initializers)
    fixtures=[];planned=[]
    for number in [27,74]:
        group=next(g for g in mapping['groups'] if g['block']==number);spec=next(g for g in current['groups'] if g['block']==number)
        canonical=next(g for g in census['groups'] if g['file_path']==file and g['block']==number)
        source_records={r['source_reference']['header_offset']:r for r in canonical['complete_clean_source_records']}
        assert len(source_records)==(51 if number==27 else 79)
        for version,parent in images.items():
            originalbank=IlnkContainer.parse(parent.read_file(file)).blocks;selected=originalbank[number]
            expected=spec['current_block_sha256'] if version=='parent_English' else group['target_block_sha256']
            assert sha(selected)==expected
            selected_commands=spec['all_current_commands'] if version=='parent_English' else group['all_target_commands']
            end=8+struct.unpack_from('<H',selected,4)[0];assert selected[end:]==bytes(len(selected)-end)
            assert selected[:4]==opening[:4] and selected[6:8]==opening[6:8]
            logical=bytearray(opening[:8]+prelude+selected[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
            target=bytes(logical)+bytes(-len(logical)%4)
            parsed,parsed_speeches=inventory(parent.read_file('/__arm9__.bin'),target)
            assert len(parsed)==len(selected_commands)+9 and len(parsed_speeches)==len(source_records) and len(target)<0x2400
            assert sum(c['word']==0 for c in parsed)==1 and parsed[-1]['offset']+4==len(logical)
            objects=[];texts=[];relative_count=0
            for ordinal,(source,command) in enumerate(zip(spec['all_source_commands'],selected_commands,strict=True)):
                at=command['offset']+delta;actual=next(c for c in parsed if c['offset']==at)
                assert actual['word']==command['word']==source['word'] and actual['native_extent']==command['native_extent'] and actual['whole_command_hex']==command['whole_command_hex']
                assert actual['ancestor_0100_offsets']==[a+delta for a in command['ancestor_0100_offsets']]
                if command['word'] in [0x100,0x200,0x300,0x400]:
                    span=struct.unpack_from('<H',selected,command['offset']+2)[0]
                    assert struct.unpack_from('<H',target,at+2)[0]==span and at+4+span==command['offset']+4+span+delta
                    relative_count+=1
                record=source_records.get(source['offset']) if source['word']==0x4000 else None
                objects.append(dict(original_block=number,source_command_ordinal=ordinal,canonical_clean_offset=source['offset'],original_command_offset=command['offset'],
                    fixture_command_offset=at,native_extent=command['native_extent'],word=command['word'],whole_command_hex=command['whole_command_hex'],
                    text_ID=None if record is None else record['id'],original_0100_ancestors=command['ancestor_0100_offsets'],fixture_0100_ancestors=actual['ancestor_0100_offsets']))
                if record is not None:
                    texts.append(dict(id=record['id'],source_record_index=record['source_record_index'],source_selector=record['source_selector'],fixture_command_offset=at,
                        fixture_body_offset=at+5,source_reference=record['source_reference'],corrected_surname_body=record['id'] in {r['id'] for r in current['records']}))
            assert len(texts)==len(source_records) and relative_count==(24 if number==27 else 20)
            image=NdsImage.open(parents[version]);blocks=list(originalbank);blocks[22]=target;image.replace_file(file,IlnkContainer(blocks).to_bytes())
            assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[file] and all(image.read_file(p)==v for p,v in parent.iter_components())
            after=IlnkContainer.parse(image.read_file(file)).blocks;assert [i for i,(a,b) in enumerate(zip(originalbank,after,strict=True)) if a!=b]==[22]
            payload=bytes(image.rom.save());out=Path(f'out/Gerhard_B{number}_{version}_v8224_RESEARCH_ONLY.nds');assert not out.exists();planned.append((out,payload))
            fixtures.append(dict(route=2,route_identity='Lil',version=version,source_block=number,research_ROM=str(out),research_ROM_sha256=sha(payload),
                parent=str(parents[version]),parent_sha256=sha(parents[version].read_bytes()),source_file=file,source_block_sha256=expected,
                fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),fixture_stored_bytes=len(target),fixture_logical_end=len(logical),
                fixture_storage_tail_bytes=len(target)-len(logical),original_opening_prelude_hex=prelude.hex(),original_opening_prelude_commands=initializers,
                all_original_exchange_commands=objects,original_text_records=texts,all_fixture_commands=parsed,source_relative_sites=relative_count,
                no_original_speech_branch_resource_effect_choice_orend_omitted=True,all_relative_operands_unchanged_under_constant48byte_shift=True,
                source_event_not_naturally_selected=True,initialized_Amsterdam_opening_entry_not_original_Stockholm_Hamburg_location=True,
                no_conditions_RNG_party_roster_funds_orresults_forced=True,conditional_text_membership_must_be_measured_not_assumed=True))
    ROOT.mkdir(parents=True)
    for path,payload in planned:path.write_bytes(payload);assert sha(path.read_bytes())==sha(payload)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert all(Path(v['path']).resolve() not in {p.resolve() for p,_ in planned} for v in values)
    added=[dict(path=str(p.resolve()),reason='Gerhard surname paired whole B27/B74 script with original9-command Lil prelude;disclosed Amsterdam entry fixture,not natural optional activation/promotion/handoff. Preserve every ROM. SHA256 '+sha(b)) for p,b in planned]
    updated=values+added;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    (ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-4]==values
    save(ROOT/'four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json',dict(fixtures=fixtures,
        paired_versions_are_previous_andrevised_English_not_clean_Japanese_ROM=True,
        complete_clean_source_context_is_separate295_speech_editorial_evidence=True,
        original9_opening_commands48bytes_preserved_without_invented_initializer=True,
        original_all225_commands130_speeches44_relative_sites_preserved_perpair=True,
        no_savestate_RAM_eventflag_role_roster_money_seed_condition_orresult_forcing=True,
        original_opening_replaced_only_for_disclosed_focused_scene_testing=True,
        actual_branch_membership_full_body_name_bounds_pagination_transitions_andnormal_return_pending=True,
        registered_current_V8172_andmainV4701_unchanged=True,new_credit=0,new_ROMs=4,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,MAP,CURRENT,CENSUS,LOADERS,CALLERS,Path(__file__)]}))
    print('Pinned4 whole-script fixtures:parent/revised English B27/B74,9original Lil initializers;all225commands/130speech memberships/44relatives preserved perpair.No forced conditions.')
