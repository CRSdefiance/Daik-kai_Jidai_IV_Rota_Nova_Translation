"""Capture one original Hamburg exchange; no revised-prose or all-path credit."""
import argparse
import json
from pathlib import Path
from types import FunctionType
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import navigate_lil_crew_v1759b as prior
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_village_wrap_v608 import read,save

RUN = Path('work/analysis/lil_Speyer_access_run_v1924')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_access_run_v1924_RESEARCH_ONLY')
JOURNAL = RUN/'navigation.jsonl'
snapshot = FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})
ROM = Path('out/all_routes_combined_v1909_candidate.nds')

def append(command):
    with JOURNAL.open('a',encoding='utf-8') as stream:stream.write(json.dumps(command)+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frame',type=int,required=True)
    parser.add_argument('--block',type=int,required=True,choices=[74,128])
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--close-run',action='store_true')
    args = parser.parse_args()
    root = args.out
    assert not root.exists()
    image,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    current = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[args.block]
    japanese = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[args.block]
    commands,speeches = inventory(image.read_file('/__arm9__.bin'),current)
    ja_commands,ja_speeches = inventory(clean.read_file('/__arm9__.bin'),japanese)
    shape = lambda rs:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets'])for r in rs]
    assert shape(commands)==shape(ja_commands)
    by_offset = {r['offset']:r for r in commands}
    source_rows = []
    for jp,now in zip(ja_speeches,speeches,strict=True):
        ja,at = jp['offset']+5,now['offset']+5
        source = japanese[ja:japanese.index(b'\0',ja)]
        value = current[at:current.index(b'\0',at)]
        assert source[0]==value[0]
        source_rows.append(dict(id=f'DK4_MES_B{args.block}_R{japanese[:ja].count(bytes([0])):04d}',
            source_reference=dict(offset=ja,bytes=len(source)),current_reference=dict(offset=at,bytes=len(value)),
            source_hex=source.hex(),current_hex=value.hex(),prefix_hex=source[:1].hex(),
            source_Japanese=source[1:].decode('cp932'),current_English=value[1:].decode('cp932')))
    rows_at = {r['current_reference']['offset']-5:r for r in source_rows}
    root.mkdir(parents=True)
    save(root/'full_source_context_uncredited.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        block=args.block,clean_block_sha256=sha(japanese),current_block_sha256=sha(current),
        all_clean_native_commands=ja_commands,all_current_native_commands=commands,records=source_rows,
        source_inventory_not_an_editorial_review=True,no_source_prose_orcompletion_credit=True))
    frame = args.frame
    holds,art,choices = [],[],[]
    for step in range(110):
        raw,im,progress,photo = snapshot(frame)
        pending = [progress['rows'][i] for i in progress['pending'].values()]
        active = [r for r in pending if r['source'].get('route')==2 and r['source'].get('block')==args.block]
        if not active:
            ends = [r for r in progress['rows']if r['kind']=='after_command'and r['source'].get('route')==2
                and r['source'].get('block')==args.block and r['source']['first_word']==0]
            assert holds and ends,('No active scene or original end;leftpaused',frame,pending)
            save(root/'closed_original_scene_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
                block=args.block,terminal_frame_requested=frame,old_text_observations=holds,original_art_pauses=art,
                choices=choices,original_end=ends[-1],observed_prefixes=sorted({r['prefix_hex']for r in holds}),
                unique_observed_record_IDs=sorted({r['id']for r in holds}),terminal_capture=str(photo),
                terminal_capture_sha256=sha(photo.read_bytes()),original_process_closed=args.close_run,
                no_editorial_revised_font_or_all_conditional_path_approval=True,
                producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
            if args.close_run:append({'stop':True})
            print(dict(block=args.block,original_scene_closed=True,observations=len(holds),
                unique_speeches=len({r['id']for r in holds}),frame=frame,run_left_paused=not args.close_run),flush=True)
            break
        assert len(active)==1
        src = active[0]['source']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==sha(current)
        at = src['payload_address']-0x02000000
        assert raw[at:at+src['payload_bytes']]==current
        assert src['first_word'] in (0x4000,0x2000,0x2100),('unclassified original pending command;leftpaused',src)
        group = []
        for hold in range(2):
            raw,im,progress,photo = snapshot(frame)
            assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
            group.append(dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw)))
            if hold==0:append(dict(until=frame+30,duration=1));frame+=30
        if src['first_word']==0x4000:
            row = rows_at[src['instruction_offset']]
            holds.append(dict(id=row['id'],prefix_hex=row['prefix_hex'],source=src,holds=group,
                original_text_observation_only=True,repeated_instruction_possible_original_pagination=sum(r['id']==row['id']for r in holds)))
            print(dict(block=args.block,observations=len(holds),id=row['id'],prefix=row['prefix_hex'],frame=frame),flush=True)
        elif src['first_word']==0x2000:
            assert by_offset[src['instruction_offset']]['whole_command_hex']=='0020'
            art.append(dict(source=src,holds=group,original_art_pause_not_padding_generated_blank=True))
        else:
            assert src['first_word']==0x2100 and not choices
            choices.append(dict(source=src,holds=group,ordinary_A_selects_current_default=True,
                actual_return_and_visible_option_association_to_be_audited=True))
        append(dict(until=frame+300,buttons=['A'],duration=8))
        frame += 300
        save(root/'original_presentation_observations_LIVE.json',dict(rows=holds,art_pauses=art,choices=choices,
            next_pause_frame=frame,not_terminal_or_revised_prose_approval=True))
    else:raise AssertionError('Bounded navigation exhausted;original process left paused')
