"""Read-only analysis of B44's stale final span; an in-memory copy only."""
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.census_native_storylines_v1995 import complete_walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_opening_span_v1999')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    rom=NdsImage.open('out/all_routes_combined_v1986_candidate.nds');clean=NdsImage.open('work/clean.nds')
    current=IlnkContainer.parse(rom.read_file('/data/SC0.DK4')).blocks[44]
    source=IlnkContainer.parse(clean.read_file('/data/SC0.DK4')).blocks[44]
    packet=read('work/analysis/editorial_source_census_v1992/SC0_block044_raw_source.json')
    last=packet['records'][-1];assert last['id']=='DK4_MES_B44_R0479'
    ref=last['provisional_current_reference'];at=ref['header_offset'];end=ref['offset']+ref['bytes']+1
    speech_extent=(end-at+1)&~1
    parent=at-12
    assert parent==6604 and struct.unpack_from('<HH',current,parent)==(0x100,64)
    assert current[parent+4:at].hex()=='00a0ffff00000100'
    after_speech=at+speech_extent
    assert current[after_speech:after_speech+4]==b'\0\1\0\0'
    successor=after_speech+4
    assert current[successor:successor+8].hex()=='00a0ffff9cff0073'
    span=successor-parent-4;assert span==76
    normalized=bytearray(current);struct.pack_into('<H',normalized,parent+2,span)
    native=complete_walk(rom.read_file('/__arm9__.bin'),bytes(normalized))
    original=read('work/analysis/native_storyline_census_v1995/SC0_block044_clean_native.json')
    assert not native['errors']
    current_speeches=[r['offset']for r in native['commands']if r['word']==0x4000]
    assert current_speeches==[r['provisional_current_reference']['header_offset']for r in packet['records']]
    assert [(r['word'],len(r['ancestor_0100_offsets']))for r in native['commands']]==[(r['word'],len(r['ancestor_0100_offsets']))for r in original['commands']]
    differences=[i for i,(a,b)in enumerate(zip(current,normalized,strict=True))if a!=b]
    assert differences==[6606]
    save(ROOT/'current_B44_final_span_diagnosis.json',dict(
        current_block_sha256=sha(current),clean_block_sha256=sha(source),one_byte_normalized_copy_sha256=sha(normalized),
        parent_offset=parent,parent_word=0x100,stored_span=64,current_matched_target=parent+4+64,
        final_speech_header_offset=at,final_speech_text_offset=ref['offset'],final_speech_terminator=end-1,
        intended_successor_A000_offset=successor,required_current_span=span,changed_copy_offsets=differences,
        corrected_in_memory_native=native,all115_current_speech_boundaries_equal_raw=True,
        clean_and_normalized_current_native_words_and_nesting_equal=True,commands=len(native['commands']),
        no_ROM_manuscript_map_registry_or_file_bytes_modified=True,
        current_candidate_still_contains_stale_span=True,release_repair_not_yet_approved=True,
        next_release_must_rebase_this_span_to_final_target_and_test_independent_preparation_branch=True,
        not_actual_gameplay_or_branch_reachability_proof=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(commands=len(native['commands']),speeches=115,old_span=64,required_current_span=span,in_memory_only=True))
