"""Clean/current38-speech packet, with unchanged raw and native source locks."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_source_v2034')
ROM=Path('out/all_routes_combined_v2030_candidate.nds')
RAW=Path('work/analysis/editorial_source_census_v1992/SC3_block033_raw_source.json')

if __name__=='__main__':
    assert not ROOT.exists()
    image,clean=map(NdsImage.open,(ROM,'work/clean.nds'));packet=read(RAW)
    assert sha(ROM.read_bytes())=='4ed991686628ef679ee1d0fc6a00ad98bccafc99c0b83cba9371fa335eb53532'
    current,original=[im.read_file('/data/SC3.DK4')for im in(image,clean)]
    assert sha(current)==packet['current_file_sha256']and sha(original)==packet['clean_file_sha256']
    cb,jb=[IlnkContainer.parse(value).blocks[33]for value in(current,original)]
    assert sha(cb)==packet['current_block_sha256']and sha(jb)==packet['clean_block_sha256']
    native={k:Path(f'work/analysis/native_storyline_census_v1995/SC3_block033_{k}_native.json')for k in('clean','current')}
    walks={k:read(p)for k,p in native.items()}
    assert all(not w['errors']and not w['typed_choice_errors']and not w['typed_choice_objects']for w in walks.values())
    assert all(w['all_independent_raw_speech_headers_equal_native4000_boundaries']for w in walks.values())
    assert len(packet['records'])==38 and cb[:4]==jb[:4]==b'CS\1\1'
    assert [(r['word'],r['offset'],r['native_extent'],r['ancestor_0100_offsets'])for r in walks['clean']['commands']]==[(r['word'],r['offset'],r['native_extent'],r['ancestor_0100_offsets'])for r in walks['current']['commands']]
    for row in packet['records']:
        for block,key in((jb,'source_reference'),(cb,'provisional_current_reference')):
            r=row[key];at=r['offset'];v=bytes.fromhex(r['hex'])
            assert block[at:at+len(v)]==v and block[at+len(v)]==0 and block[r['header_offset']:r['header_offset']+6].hex()==r['complete_preamble_hex']
    ROOT.mkdir(parents=True)
    save(ROOT/'all38_clean_current_Hangzhou_opening_source.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        file_path='/data/SC3.DK4',current_SC3_sha256=sha(current),clean_SC3_sha256=sha(original),block=33,
        source_block_sha256=sha(jb),current_block_sha256=sha(cb),raw_packet=str(RAW),raw_packet_sha256=sha(RAW.read_bytes()),
        native_proofs={k:dict(path=str(p),sha256=sha(p.read_bytes()))for k,p in native.items()},native_commands=walks,
        records=packet['records'],source_speeches=38,source_choice_labels=0,presentation_counts=dict(Counter(r['source_reference']['leading_byte_hex']for r in packet['records'])),
        complete_Japanese_current_exchange_read=True,
        source_only_findings=[
            'R0017 loses the explicit mission against wako vessels;R0030 loses their boarding specialty.',
            'R0045 has unnatural Both did well rather than directly addressing both returning officers.',
            'R0067 omits the narrow bay;R0070 needs the exact predicted appearance and informal enthusiasm.',
            'R0090 should preserve Ming maritime closure and the English connections without inventing defiance of a law.',
            'R0093 explicitly names France;R0096 taking the blame must not assert unsupported details about how it happened.',
            'R0103 loses stowing away and traveling to Ming in search of the sword;R0107 loses compatriots and duty.',
            'R0121 asks for Ian by name,not a generic envoy.',
            'R0143 omits the large expected tax revenue;R0154 needs careful ship maintenance in anticipation of retaliation.',
        ],
        system_unlock_fixture_existing_not_earned_actual_capture_pending=True,
        source_prose_credit=0,completion_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(source_speeches=38,native_commands=len(walks['current']['commands']),relative_sites=sum(r['word']in(0x100,0x200,0x300,0x400)for r in walks['current']['commands']),presentation=dict(Counter(r['source_reference']['leading_byte_hex']for r in packet['records'])),new_editorial_credit=0))
