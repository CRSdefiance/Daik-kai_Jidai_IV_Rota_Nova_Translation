"""Independent bounded native walks for every source/current route block.

Opaque effects are bridged only to determine structure. No branch reachability,
portrait, display, gameplay or editorial completion is inferred from this walk.
"""
from collections import Counter
from pathlib import Path
import struct
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.census_editorial_sources_v1990 import decoded
from scripts.research_wedding_command_v676 import walk
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/native_storyline_census_v1991')
RAW = Path('work/analysis/editorial_source_census_v1990/four_routes_raw_and_COMMON_source_census.json')
BASE, OBJECT, STREAM = 0x02000000, 0x02650000, 0x02660000


def complete_walk(arm,block):
    commands, errors, bridges = [], [], []
    if len(block) < 8 or block[:4] != b'CS\0\1':
        return dict(commands=[],errors=[dict(type='non-CS-block',first16_hex=block[:16].hex())],opaque_effect_bridges=[])
    end = 8+struct.unpack_from('<H',block,4)[0]
    if end > len(block) or any(block[end:]):
        return dict(commands=[],errors=[dict(type='extent-or-nonzero-tail',logical_end=end,block_bytes=len(block))],opaque_effect_bridges=[])
    def visit(start,stop,ancestors):
        if len(ancestors) > 256:
            errors.append(dict(type='nested-span-depth',start=start,stop=stop)); return
        body = block[start:stop]
        synthetic = b'CS\0\1'+struct.pack('<H',len(body))+b'\0\0'+body
        try: result = walk(arm,synthetic)
        except Exception as exc:
            errors.append(dict(type=type(exc).__name__,error=str(exc),scope_start=start,scope_stop=stop)); return
        for effect in result['opaque_effect_bridges']:
            bridges.append({**effect,'source_offset':start+effect['source_offset']-8,'scope_start':start})
        for command in result['rows']:
            at = start+command['offset']-8
            extent = command['native_extent']
            commands.append(dict(offset=at,word=command['word'],native_extent=extent,ancestor_0100_offsets=ancestors,
                whole_command_hex=block[at:at+extent].hex(),native_result_hex=command['result']))
            if command['word'] == 0x100:
                span = struct.unpack_from('<H',block,at+2)[0]
                if extent != span+4:
                    errors.append(dict(type='0100-native-span-mismatch',offset=at,extent=extent,span=span))
                else: visit(at+4,at+extent,[*ancestors,at])
        if result['error'] is not None or result['stopped_offset'] != result['logical_end']:
            errors.append(dict(type='native-walk-error',scope_start=start,scope_stop=stop,
                stopped_original_offset=start+result['stopped_offset']-8,error=result['error']))
    visit(8,end,[])
    ordered = sorted(commands,key=lambda r:r['offset'])
    if len({r['offset'] for r in ordered}) != len(ordered): errors.append(dict(type='duplicate-native-command-boundaries'))
    return dict(commands=ordered,errors=errors,logical_end=end,opaque_effect_bridges=bridges,
        linear_extents_and_nested0100_structure_only_not_runtime_reachability=True)


def choices(cpu,block,commands):
    rows,errors = [],[]
    untouched = bytes(cpu.mem_read(BASE,0x400000))
    for command in commands:
        if command['word'] != 0x2100: continue
        value = bytes.fromhex(command['whole_command_hex'])
        try:
            cpu.mem_write(STREAM-16,b'\xa5'*(len(value)+32))
            cpu.mem_write(STREAM,value)
            cpu.mem_write(OBJECT-16,b'\xa5'*64)
            cpu.mem_write(OBJECT,struct.pack('<3I',0,0,STREAM))
            owner = bytes(cpu.mem_read(OBJECT-16,64))
            call(cpu,0x2A3B8,(OBJECT,))
            count = cpu.reg_read(UC_ARM_REG_R0)
            assert 0 < count <= 64,('native-label-count',count)
            labels = []
            for index in range(count):
                call(cpu,0x2A30C,(OBJECT,index))
                pointer = cpu.reg_read(UC_ARM_REG_R0)
                offset = pointer-STREAM
                assert 2 <= offset < len(value),('native-label-pointer-outside-object',offset,len(value))
                end = value.find(b'\0',offset)
                assert offset <= end < len(value)
                raw = value[offset:end]
                labels.append(dict(option_index=index,relative_offset=offset,offset=command['offset']+offset,
                    bytes=len(raw),hex=raw.hex(),CP932=decoded(raw)))
            assert bytes(cpu.mem_read(BASE,0x400000)) == untouched
            assert bytes(cpu.mem_read(OBJECT-16,64)) == owner
            assert bytes(cpu.mem_read(STREAM,len(value))) == value
            assert bytes(cpu.mem_read(STREAM-16,16)) == bytes(cpu.mem_read(STREAM+len(value),16)) == b'\xa5'*16
            rows.append(dict(command_offset=command['offset'],native_label_count=count,labels=labels,
                native_getters_ABI_4MiB_owner_input_and_guard_checks_pass=True))
        except Exception as exc:
            errors.append(dict(command_offset=command['offset'],type=type(exc).__name__,error=str(exc)))
    return rows,errors


if __name__ == '__main__':
    assert not ROOT.exists()
    raw = read(RAW)
    assert sha(Path(raw['candidate']).read_bytes()) == raw['candidate_sha256']
    current,clean = map(NdsImage.open,(raw['candidate'],'work/clean.nds'))
    assert sha(Path('work/clean.nds').read_bytes()) == raw['clean_ROM_sha256']
    images = dict(clean=clean,current=current)
    arms = {name:im.read_file('/__arm9__.bin') for name,im in images.items()}
    spans = ((0x293B8,0x2A600),(0x28A28,0x28A64))
    same_parser = all(arms['clean'][a:b] == arms['current'][a:b] for a,b in spans)
    ROOT.mkdir(parents=True)
    journal = ROOT/'progress.jsonl'
    results,errors,pairs = [],[],[]
    counts = Counter()
    cpu = {name:machine(arm) for name,arm in arms.items()}
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        containers = {name:IlnkContainer.parse(im.read_file(path)).blocks for name,im in images.items()}
        for number in range(len(containers['clean'])):
            spec = next(r for r in raw['blocks'] if r['file_path'] == path and r['block'] == number)
            raw_path = Path(spec['raw_source_packet'])
            assert sha(raw_path.read_bytes()) == spec['raw_source_packet_sha256']
            packet = read(raw_path)
            versions = {}
            for name in ('clean','current'):
                block = containers[name][number]
                assert sha(block) == packet[('clean' if name == 'clean' else 'current')+'_block_sha256']
                walked = complete_walk(arms[name],block)
                menus,menu_errors = choices(cpu[name],block,walked['commands'])
                signatures = [i for i in range(max(0,len(block)-4)) if block[i:i+5] == bytes.fromhex('0040ffff00')]
                speeches = [r for r in walked['commands'] if r['word'] == 0x4000]
                native_offsets = [r['offset'] for r in speeches]
                matching = signatures == native_offsets
                if not matching:
                    walked['errors'].append(dict(type='raw-native-speech-boundary-difference',
                        raw_only=sorted(set(signatures)-set(native_offsets)),native_only=sorted(set(native_offsets)-set(signatures))))
                out = ROOT/f'SC{route}_block{number:03d}_{name}_native.json'
                value = dict(version=name,file_path=path,block=number,block_sha256=sha(block),ARM9_sha256=sha(arms[name]),
                    **walked,typed_choice_objects=menus,typed_choice_errors=menu_errors,
                    all_independent_raw_speech_headers_equal_native4000_boundaries=matching,
                    raw_source_packet=str(raw_path),raw_source_packet_sha256=spec['raw_source_packet_sha256'],
                    no_display_gameplay_or_editorial_credit=True,full_goal_complete=False)
                save(out,value)
                result = dict(version=name,file_path=path,block=number,proof=str(out),proof_sha256=sha(out.read_bytes()),
                    commands=len(walked['commands']),speeches=len(speeches),choice_objects=len(menus),
                    choice_labels=sum(len(r['labels']) for r in menus),errors=walked['errors']+menu_errors,
                    raw_speech_boundaries_equal=matching)
                results.append(result)
                counts[name+'_blocks'] += 1
                counts[name+'_commands'] += len(walked['commands'])
                counts[name+'_speeches'] += len(speeches)
                counts[name+'_choice_objects'] += len(menus)
                counts[name+'_choice_labels'] += sum(len(r['labels']) for r in menus)
                if result['errors']: errors.append(result)
                versions[name] = value
            a,b = versions['clean'],versions['current']
            structure = ([r['word'] for r in a['commands']] == [r['word'] for r in b['commands']]
                and [len(r['ancestor_0100_offsets']) for r in a['commands']] == [len(r['ancestor_0100_offsets']) for r in b['commands']])
            pair = dict(file_path=path,block=number,clean_current_native_word_order_and_nested_depth_equal=structure,
                raw_and_native_all_boundaries_agree=all(v['all_independent_raw_speech_headers_equal_native4000_boundaries'] for v in versions.values()),
                both_complete_without_errors=all(not v['errors'] and not v['typed_choice_errors'] for v in versions.values()),
                choice_counts_equal=[r['native_label_count'] for r in a['typed_choice_objects']] == [r['native_label_count'] for r in b['typed_choice_objects']])
            pairs.append(pair)
            with journal.open('a',encoding='utf-8') as stream: stream.write(__import__('json').dumps(pair)+'\n')
            if number%32 == 0:
                print(dict(route=route,block=number,blocks_done=len(pairs),blocks_with_errors=len(errors)),flush=True)
    save(ROOT/'all_route_source_current_native_census.json',dict(candidate=raw['candidate'],candidate_sha256=raw['candidate_sha256'],
        raw_source_census=str(RAW),raw_source_census_sha256=sha(RAW.read_bytes()),
        native_parser_code_spans_identical_clean_current=same_parser,
        parser_spans=[dict(start=BASE+a,end_exclusive=BASE+b,clean_sha256=sha(arms['clean'][a:b]),current_sha256=sha(arms['current'][a:b])) for a,b in spans],
        totals=dict(counts),versions=results,paired_block_structures=pairs,blocks_requiring_further_parser_work=errors,
        source_current_structure_differences=[r for r in pairs if not r['clean_current_native_word_order_and_nested_depth_equal']],
        raw_current_pairing_not_approved_where_native_structure_or_boundaries_differ=True,
        opaque_effect_bridges_only_structural_not_runtime_branch_reachability=True,
        no_native_display_portrait_gameplay_or_editorial_review_credit_added=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(totals=dict(counts),error_blocks=len(errors),structure_differences=sum(not r['clean_current_native_word_order_and_nested_depth_equal'] for r in pairs),editorial_credit_added=0),flush=True)
