"""Source-only next-family packet,including all73 raw/native speech objects.

All three exchanges have been read; prose decisions/native review are pending.
No new editorial completion or source/prose counter credit is granted here.
"""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_source_v2017')
ROM=Path('out/all_routes_combined_v2013_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()
    image,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    assert sha(ROM.read_bytes())=='29d9de4bdd46231b865cbe39a0592dd65a0c55378dfdbb7d8c10aa6104ca7d55'
    current_file,source_file=image.read_file('/data/SC1.DK4'),clean.read_file('/data/SC1.DK4')
    before,original=map(lambda value:IlnkContainer.parse(value).blocks,(current_file,source_file))
    packets=[]
    for number,count in((42,37),(43,9),(44,27)):
        raw=Path(f'work/analysis/editorial_source_census_v1992/SC1_block{number:03d}_raw_source.json')
        packet=read(raw)
        assert packet['current_file_sha256']==sha(current_file)and packet['clean_file_sha256']==sha(source_file)
        assert packet['current_block_sha256']==sha(before[number])and packet['clean_block_sha256']==sha(original[number])
        native={label:Path(f'work/analysis/native_storyline_census_v1995/SC1_block{number:03d}_{label}_native.json')for label in('clean','current')}
        walks={label:read(path)for label,path in native.items()}
        assert all(not w['errors']and not w['typed_choice_errors']and not w['typed_choice_objects']for w in walks.values())
        assert len(packet['records'])==count
        assert all(w['all_independent_raw_speech_headers_equal_native4000_boundaries']for w in walks.values())
        assert [(r['word'],len(r['ancestor_0100_offsets']))for r in walks['clean']['commands']]==[(r['word'],len(r['ancestor_0100_offsets']))for r in walks['current']['commands']]
        packets.append(dict(block=number,raw_packet=str(raw),raw_packet_sha256=sha(raw.read_bytes()),
            native_proofs={k:dict(path=str(p),sha256=sha(p.read_bytes()))for k,p in native.items()},
            source_and_current_byte_exact_to_new_registered_ROM=True,records=packet['records'],native_commands=walks))
    existing=Path('work/analysis/Gerhard_story_control_proof_v1857/original4000_prefix10_Gerhard_live_mapping.json')
    control=read(existing)
    assert control['ARM9_sha256']==sha(image.read_file('/__arm9__.bin'))
    old=NdsImage.open(control['candidate'])
    assert old.read_file('/data/SC1.DK4')==current_file
    assert control['actual_Gerhard_portrait_full_nameplate_body_and_normal_next_Hodram_portrait_viewed']
    ROOT.mkdir(parents=True)
    save(ROOT/'all73_clean_current_opening_and_Lil_encounter_source.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        file_path='/data/SC1.DK4',current_SC1_sha256=sha(current_file),clean_SC1_sha256=sha(source_file),packets=packets,
        source_speeches=73,source_choice_labels=0,all_three_full_clean_Japanese_current_exchanges_read=True,
        old_fixed_batch='translations/hodram_intro_natural_v2_sc1_b42_b44.json',
        old_batch_67_translation_count_does_not_cover_all73_native_objects=True,
        old_nonprose_B42_R0032_fragment_not_counted_as_speech=True,
        source_only_leads=[
            'B42 territorial warning changed from direct sovereign-water accusation to a generic border rule.',
            'B42 R0079 pirate-like patrol fleet became pirate hunters,a substantive factual reversal.',
            'B42 R0076 omits the named sole ship Vasteros;retain approved ship spelling after reference check.',
            'B42 R0082 national-policy support for Protestants needs its stated budget context.',
            'B42 R0113 loses the personal first experience of trembling with anticipation for battle.',
            'B42 R0135 invents escape where source says the quarry was not what was expected.',
            'B43 R0039 loses the world-largest trading sphere;R0068 invents an after-battle condition.',
            'B44 R0049 omits adventurers;R0084 changes the apology into an assertion of offense already taken.',
            'B44 R0111 omits the explicit objection to tolerating the rude woman\'s abuse.',
        ],
        inherited_exact_runtime_SC1_Gerhard_Hodram_live_control=dict(path=str(existing),sha256=sha(existing.read_bytes())),
        remaining_control_gate='Confirm Charles12/Manuel17 andthe seven separate FE panels inthis complete source context;reuse proven identical controls where exact.',
        all_sources_preserved_no_manuscript_ROM_registry_or_counter_change=True,source_prose_reviews_added=0,
        full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    handoff=Path('docs/editorial_handoff_current.md');text=handoff.read_text(encoding='utf-8')
    (ROOT/'handoff_before.md').write_bytes(handoff.read_bytes())
    section=('## Next complete family prepared - V2017\n\n'
        'Hodram SC1B42/B43/B44:all73 clean/current speeches reread ascomplete exchanges(37/9/27),nochoices. '
        'Sourcepacket:work/analysis/hodram_opening_source_v2017/all73_clean_current_opening_and_Lil_encounter_source.json. '
        'Allsource/current/native bodylocks matchV2013 unchangedSC1f262660b6321c33a941f7f959f726d42f40ce035973298c9f807a663f449ec35. '
        'Older67-record batch omits six native speech objects;its separate B42R0032 four-byte nonprose fragment remainsoutside speech counts. '
        'Source leads include pirate-like patrol fleet versuspiratehunters,omittedVasteros,the first battle-thrill recollection,unsupportedescape/after-battle claims,andLil/Camille exchange omissions. '
        'Source-only preparation grantsno newsource/prose/completioncredit:545fresh integrated,1948historicalcomplete,2064source/prose,0activeroutedrafts remaincurrent. '
        'Next:source-grounded individual prose decisions forall73,with live/private presentation gates forCharles12,Manuel17 andsevenFE objects asneeded. '
        'Gerhard10/Hodram01 liveV1857 exactSC1/runtime evidence isreusable. No needtorepeat V2013completedrelease/patch/startupchecks. '
        'Alljobs terminal;fullgoalactive,allROMs preserved.\n\n')
    marker='## Rafael Lisbon opening117 integrated - V2016';assert marker in text
    text=text.replace('# Current editorial handoff - V2016b','# Current editorial handoff - V2017',1).replace(marker,section+marker,1)
    handoff.write_text(text,encoding='utf-8')
    save(ROOT/'source_checkpoint_receipt.json',dict(source_speeches=73,source_prose_credit=0,editorial_completion_credit=0,
        current_registered_ROM_unchanged=True,handoff_sha256=sha(handoff.read_bytes()),full_goal_complete=False))
    print(dict(next_source_speeches=73,blocks=[42,43,44],choices=0,new_editorial_credit=0,exact_old_control_inheritance=True))
