"""Lossless four-route raw-source and3668 native COMMON-entry coverage snapshot.

Raw speech signatures are candidates until the independent native-command walk
agrees. This snapshot grants no editorial, display or gameplay completion credit.
"""
from collections import Counter
from pathlib import Path
import re
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_source_census_v1992')
ROM = Path('out/all_routes_combined_v1986_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
HEADER = bytes.fromhex('0040ffff00')
STALE = re.compile(r'\b(?:Raphael|Kamil|Hodrum|Joaquim)\b')


def decoded(raw):
    try: return raw.decode('cp932')
    except UnicodeDecodeError: return None


def segments(block):
    rows, offset = [], 0
    for index, raw in enumerate(block.split(b'\0')):
        if raw:
            text = decoded(raw)
            row = dict(index=index,offset=offset,bytes=len(raw),sha256=sha(raw),CP932_decodable=text is not None)
            if text is not None and contains_japanese(text): row.update(Japanese_candidate_text=text)
            rows.append(row)
        offset += len(raw)+1
    return rows


def raw_speeches(block):
    rows, pos = [], 0
    while True:
        pos = block.find(HEADER,pos)
        if pos < 0: break
        at = pos+5
        end = block.find(b'\0',at+1)
        terminated = end >= 0
        if end < 0: end = len(block)
        raw = block[at:end]
        body = raw[1:] if raw else b''
        text, whole = decoded(body), decoded(raw)
        rows.append(dict(header_offset=pos,offset=at,bytes=len(raw),hex=raw.hex(),terminated=terminated,
            segment_index=block[:at].count(b'\0')+int(block[at:at+1]==b'\0'),
            legacy_header_following_segment_index=block[:at].count(b'\0'),
            text_offset=at+1,zero_speaker_is_control_not_terminator=block[at:at+1]==b'\0',complete_preamble_hex=block[pos:pos+6].hex(),
            leading_byte_hex=raw[:1].hex(),body_after_first_byte_CP932=text,whole_record_CP932=whole,
            body_contains_Japanese=text is not None and contains_japanese(text),
            whole_record_CP932_decodable=whole is not None,body_CP932_decodable=text is not None))
        pos += len(HEADER)
    return rows


if __name__ == '__main__':
    assert not ROOT.exists()
    ledger = read(LEDGER)
    candidate = ledger['current_integrated_candidate']
    digest = sha(ROM.read_bytes())
    assert digest == candidate['sha256'] == 'f2dcb4cc4d688e1cd40a22367180841d27d06e540edbd16927f784b2cfcb50ca'
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and len(manifest['batches']) == 485
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    image, clean = map(NdsImage.open,(ROM,'work/clean.nds'))
    arm, clean_arm = image.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    fresh = set(ledger['contextual_story_natural_dialogue_pass_v1871']['record_IDs'])
    completed = {}
    common_ids = set()
    for family in ledger['completed_editorial_families']:
        common_ids.update(n for n in family.get('native_message_IDs',[]) if isinstance(n,int))
        for row in family.get('records',[]):
            path = row.get('file_path',family.get('file_path'))
            ident = row.get('id','')
            match = re.fullmatch(r'COMMON_MESSAGE_(\d+)',ident)
            if match: common_ids.add(int(match.group(1)))
            if path in tuple(f'/data/SC{n}.DK4' for n in range(4)):
                source = row.get('source_hex',row.get('raw_source',{}).get('hex'))
                if source: completed.setdefault((path,ident),[]).append(dict(family=family['id'],source_hex=source,
                    source_reference=row.get('source_reference'),final_review=family.get('final_review')))
    ROOT.mkdir(parents=True)
    save(ROOT/'input_locks.json',dict(candidate=str(ROM),candidate_sha256=digest,
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),ARM9_sha256=sha(arm),
        ledger=str(LEDGER),ledger_sha256=sha(LEDGER.read_bytes()),release_stack_sha256=manifest['release_stack_sha256'],
        manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),full_goal_complete=False))
    blocks_summary, examples, gaps = [], [], []
    prefixes = Counter()
    total = Counter()
    matched_fresh = set()
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        source_file, target_file = clean.read_file(path), image.read_file(path)
        sources, currents = (IlnkContainer.parse(raw).blocks for raw in (source_file,target_file))
        assert len(sources) == len(currents)
        for number,(source,current) in enumerate(zip(sources,currents,strict=True)):
            a,b = raw_speeches(source),raw_speeches(current)
            pairable = len(a) == len(b)
            rows = []
            for ordinal, speech in enumerate(a):
                ident = f'DK4_MES_B{number:02d}_R{speech["segment_index"]:04d}'
                bindings = [r for r in completed.get((path,ident),[]) if r['source_hex'] == speech['hex']
                    and (not r['source_reference'] or r['source_reference']['offset'] == speech['offset'])]
                reconciled = path == '/data/SC2.DK4' and ident in fresh and bool(bindings)
                if reconciled: matched_fresh.add(ident)
                row = dict(id=ident,file_path=path,block=number,source_ordinal=ordinal,source_reference=speech,
                    historical_completed_source_bindings=bindings,fresh_contextual_source_binding_found=reconciled,
                    raw_header_not_yet_independently_native_verified=True)
                prefixes[(route,speech['leading_byte_hex'])] += 1
                total['raw_speech_signatures'] += 1
                if not speech['whole_record_CP932_decodable'] and speech['body_contains_Japanese']:
                    total['whole_record_decode_would_omit_Japanese_body'] += 1
                    examples.append(dict(file_path=path,block=number,id=ident,source_offset=speech['offset'],
                        leading_byte_hex=speech['leading_byte_hex'],source_Japanese=speech['body_after_first_byte_CP932']))
                if pairable:
                    now = b[ordinal]
                    row['provisional_current_reference'] = now
                    row['provisional_same_leading_byte'] = now['leading_byte_hex'] == speech['leading_byte_hex']
                    if now['body_contains_Japanese']: total['current_raw_speech_bodies_containing_Japanese'] += 1
                    if now['body_after_first_byte_CP932']:
                        aliases = STALE.findall(now['body_after_first_byte_CP932'])
                        if aliases: row['current_name_aliases_requiring_contextual_review'] = aliases
                rows.append(row)
            source_segments,current_segments = segments(source),segments(current)
            text_ranges = [(r['offset'],r['offset']+r['bytes']) for r in a]
            outside = [r for r in source_segments if 'Japanese_candidate_text' in r
                and not any(low <= r['offset'] < high for low,high in text_ranges)]
            native_pending = dict(clean=True,current=True)
            name = ROOT/f'SC{route}_block{number:03d}_raw_source.json'
            save(name,dict(file_path=path,block=number,clean_file_sha256=sha(source_file),current_file_sha256=sha(target_file),
                clean_block_sha256=sha(source),current_block_sha256=sha(current),clean_bytes=len(source),current_bytes=len(current),
                clean_first16_hex=source[:16].hex(),current_first16_hex=current[:16].hex(),
                raw_header_count_clean=len(a),raw_header_count_current=len(b),raw_ordinal_pairing_provisional=pairable,
                records=rows,all_nonempty_clean_null_segments=source_segments,all_nonempty_current_null_segments=current_segments,
                clean_Japanese_null_segments_outside_speech_signatures=outside,
                native_inventory_pending=native_pending,editorial_review_or_display_approval=False,full_goal_complete=False))
            block_row = dict(file_path=path,block=number,clean_block_sha256=sha(source),current_block_sha256=sha(current),
                raw_speeches=len(a),current_raw_speeches=len(b),raw_source_packet=str(name),raw_source_packet_sha256=sha(name.read_bytes()),
                clean_nonempty_null_segments=len(source_segments),Japanese_segments_outside_speech_headers=len(outside),
                native_walk_pending=True)
            blocks_summary.append(block_row)
            total['blocks'] += 1
            total['nonempty_clean_null_segments'] += len(source_segments)
            total['Japanese_segments_outside_speech_headers'] += len(outside)
            if not pairable: gaps.append(dict(file_path=path,block=number,type='raw-header-counts-differ',clean=len(a),current=len(b)))
        print(dict(route=route,blocks=len(sources),raw_speeches=sum(r['raw_speeches'] for r in blocks_summary if r['file_path'] == path)),flush=True)
    current_common, clean_common = image.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/COMMON/MESFILE.DK4')
    directory = read('translations/reinforcement_faction_prose_release_v1.json')['directory_sha256']
    source_entries = common_message_entries(clean_common,clean_arm)
    target_entries = entries(current_common,arm,directory)
    assert len(source_entries) == len(target_entries) == 3668
    common_rows = []
    for source,current in zip(source_entries,target_entries,strict=True):
        assert source.message_id == current.message_id
        common_rows.append(dict(id=f'COMMON_MESSAGE_{source.message_id}',message_id=source.message_id,
            source_reference=dict(block=source.block,offset=source.block_offset,copy_end=source.copy_end,bytes=len(source.text)),
            current_reference=dict(block=current.block,offset=current.block_offset,copy_end=current.copy_end,bytes=len(current.text)),
            source_hex=source.text.hex(),current_hex=current.text.hex(),source_Japanese=source.text.decode('cp932'),
            current_stored_English=current.text.decode('cp932'),historical_completed_ID=source.message_id in common_ids,
            fresh_contextual_review_not_inferred_from_historical_completion=True))
    common_path = ROOT/'all3668_clean_current_native_COMMON_entries.json'
    save(common_path,dict(clean_COMMON_sha256=sha(clean_common),current_COMMON_sha256=sha(current_common),
        current_ARM9_sha256=sha(arm),directory_sha256=directory,records=common_rows,
        historical_completed_IDs_found=sorted(common_ids),native_boundaries_not_a_new_copy_or_gameplay_test=True,
        editorial_reviews_added=0,full_goal_complete=False))
    summary = dict(candidate=str(ROM),candidate_sha256=digest,clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        totals=dict(total),blocks=blocks_summary,common_entries=str(common_path),common_entries_sha256=sha(common_path.read_bytes()),
        whole_record_decode_omission_examples=examples,raw_header_pairing_gaps=gaps,
        leading_byte_counts=[dict(route=r,byte_hex=b,count=n) for (r,b),n in sorted(prefixes.items())],
        fresh_speech_source_bindings_found=len(matched_fresh),fresh_speech_IDs=sorted(matched_fresh),
        historical_completed_COMMON_IDs_found=len(common_ids),ledger_declared_completed_COMMON=ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'],
        supersedes_raw_census='work/analysis/editorial_source_census_v1990/four_routes_raw_and_COMMON_source_census.json',
        predecessor_preserved=True,speaker00_consumed_before_string_terminator=True,
        native_command_choice_and_nonstandard_text_inventory_still_required=True,
        all_raw_speech_and_null_segments_preserved_without_decoding_filter=True,
        no_editorial_completion_ROM_patch_registry_or_gameplay_change=True,editorial_reviews_added=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'four_routes_raw_and_COMMON_source_census.json',summary)
    print(dict(totals=dict(total),COMMON_entries=3668,COMMON_historical_bindings=len(common_ids),fresh_speech_bindings=len(matched_fresh),
        raw_pairing_gaps=len(gaps),native_walk_pending=True,editorial_credit_added=0),flush=True)
