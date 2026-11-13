"""Inventory original native boundaries; classify header disagreements without credit."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/raw_B141_SC3_B109_diagnostic_v3493')
if __name__=='__main__':
    assert not ROOT.exists();clean,current=NdsImage.open('work/clean.nds'),NdsImage.open('out/all_routes_combined_v3487_candidate.nds');inventory,walker,source=scoped_inventory();needle="    assert raw_headers==[r['offset'] for r in rows]\n";assert source.count(needle)==1
    diagnostic_source=source.replace(needle,'    # Diagnostic only: retain both inventories below, never treat disagreement as approval.\n');ns=dict(inventory.__globals__);exec(compile(diagnostic_source,str(Path(__file__))+'::diagnostic-inventory','exec'),ns);diagnostic=ns['inventory'];ROOT.mkdir(parents=True);results=[]
    for route,n in [(2,141),(3,109)]:
        path=f'/data/SC{route}.DK4';versions=[]
        for label,image in [('clean',clean),('current',current)]:
            block=IlnkContainer.parse(image.read_file(path)).blocks[n];commands,speeches=diagnostic(image.read_file('/__arm9__.bin'),block)
            raw=[i for i in range(len(block)-4) if block[i:i+5]==b'\0\x40\xff\xff\0'];native=[c['offset'] for c in speeches];mismatches=[]
            for offset in sorted(set(raw)^set(native)):
                owners=sorted([c for c in commands if c['offset']<=offset<c['offset']+c['native_extent']],key=lambda c:c['native_extent'])
                mismatches.append(dict(offset=offset,canonical_raw_header=offset in raw,native_4000_command=offset in native,nearest_native_owner=owners[0] if owners else None,bytes32_hex=block[offset:offset+32].hex()))
            rows=[]
            for c in speeches:
                at=c['offset'];rows.append(dict(offset=at,whole_command_hex=c['whole_command_hex'],native_extent=c['native_extent'],first16_hex=block[at:at+16].hex(),ancestor_0100_offsets=c['ancestor_0100_offsets']))
            out=ROOT/f'{label}_SC{route}_block{n:03d}.bin';out.write_bytes(block)
            versions.append(dict(version=label,file_path=path,block=n,block_sha256=sha(block),bytes=len(block),logical_end=8+struct.unpack_from('<H',block,4)[0],complete_native_commands=commands,native_4000_commands=rows,canonical_raw_header_offsets=raw,header_disagreements=mismatches,block_copy=str(out),block_copy_sha256=sha(out.read_bytes())))
        results.append(dict(file_path=path,block=n,versions=versions,no_source_consumer_classification_or_editorial_credit_granted=True))
    (ROOT/'explicit_unmatched_native_walk.txt').write_text(walker,encoding='utf-8');(ROOT/'diagnostic_inventory_function.txt').write_text(diagnostic_source,encoding='utf-8')
    save(ROOT/'raw_header_and_original_native_boundaries.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM='out/all_routes_combined_v3487_candidate.nds',current_ROM_sha256=sha(Path('out/all_routes_combined_v3487_candidate.nds').read_bytes()),results=results,original_4000_extents_and_noncanonical_preambles_require_typed_classification=True,raw_header_equality_assertion_removed_only_for_explicit_diagnostic_not_approval=True,no_ROM_ledger_registry_review_orcompletion_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(r['file_path'],r['block'],[(v['version'],len(v['complete_native_commands']),len(v['native_4000_commands']),len(v['header_disagreements'])) for v in r['versions']]) for r in results])
