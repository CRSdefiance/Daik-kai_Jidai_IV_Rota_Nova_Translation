"""Prepare complete clean-only transcripts and original relative-span proof."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_remaining_B135_B140_source_v3345b/next35_B135_B136_clean_current_context.json')
ROOT=Path('work/analysis/lil_B135_B136_clean_transcripts_v3348')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);old=Path('scripts/prove_lil_B122_B127_branches_v3261b.py');new=Path('scripts/prove_lil_B135_B136_branches_v3348b.py');assert not new.exists()
    sites=sum(c['word'] in [0x100,0x200,0x300,0x400] for b in packet['blocks'] for c in b['all_clean_native_commands']);assert sites>0
    text=old.read_text(encoding='utf-8');changes={'lil_B122_B127_branches_v3261b':'lil_B135_B136_branches_v3348b','work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json':str(SOURCE).replace('\\','/')}
    for a,b in changes.items():assert a in text,a;text=text.replace(a,b)
    # Bind expected totals to this new exact packet; never inherit the prior64 sites.
    text=text.replace('==64',f'=={sites}').replace('==640',f'=={sites*10}')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf-8');ROOT.mkdir(parents=True);files=[]
    for b in packet['blocks']:
        byoffset={r['source_reference']['offset']-5:r for r in b['records']};choice={c['command_offset']:c for c in b['choices']};reading=[];full=[]
        for c in b['all_clean_native_commands']:
            at=c['offset'];full.append(f"COMMAND {at:04X} word={c['word']:04X} bytes={c['native_extent']} ancestors={c['ancestor_0100_offsets']} hex={c['whole_command_hex']}")
            if at in byoffset:
                r=byoffset[at];s=f"{r['id']} @0x{r['source_reference']['offset']:04X} prefix={r['source_presentation_prefix_hex']} complete_preamble={r['source_complete_preamble_hex']}\n{r['source_Japanese']}\n";reading.append(s);full.append(s)
            if at in choice:
                for r in choice[at]['records']:
                    s=f"{r['id']} choice{r['option_index']} @0x{r['source_reference']['offset']:04X}\n{r['source_Japanese']}\n";reading.append(s);full.append(s)
        for suffix,lines in [('clean_reading',reading),('complete_clean_exchange',full)]:
            p=ROOT/f'B{b["block"]}_{suffix}.txt';p.write_text('\n'.join(lines),encoding='utf-8');files.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'complete_clean_transcript_and_branch_tool_provenance.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),transcripts=files,full_commands=61,source_speeches=35,typed_labels=0,all35_complete_source_preambles_preserved=True,whole_clean_exchange_reading_not_yet_claimed=True,older_English_not_in_transcripts=True,branch_sites=sites,expected_original_clean_current_native_cases=sites*10,branch_producer=str(new),branch_producer_sha256=sha(new.read_bytes()),previous_branch_producer=str(old),previous_branch_producer_sha256=sha(old.read_bytes()),source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(complete_clean_transcript_blocks=[135,136],source_speeches=35,labels=0,commands=61,relative_sites=sites,expected_native_cases=sites*10,whole_context_reading_still_pending=True,credit=0))
