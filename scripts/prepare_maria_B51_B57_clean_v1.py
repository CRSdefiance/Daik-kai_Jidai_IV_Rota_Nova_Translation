"""Select 310 disjoint clean source objects in seven complete exchanges, before current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B51_B57_clean_20261109')
def main():
    assert not ROOT.exists()
    path=Path('work/story_source_coverage_20261109_SC3_v3/residual_clean_source_packet.json');packet=load(path)
    assert packet['source_only_not_current_English']
    image=NdsImage.open(packet['source_ROM']);assert digest(packet['source_ROM'])==packet['source_ROM_sha256']
    archive=image.read_file('/data/SC3.DK4');assert sha(archive)==packet['source_archive_sha256']
    blocks=IlnkContainer.parse(archive).blocks
    selected=deepcopy([g for g in packet['groups'] if 51<=g['block']<=57])
    assert [g['block'] for g in selected]==list(range(51,58)) and sum(len(g['records']) for g in selected)==310
    keys=[]
    for group in selected:
        assert bytes.fromhex(group['clean_block_hex'])==blocks[group['block']]
        for row in group['records']:
            assert not row['covered'] and not row['exact_credited_source_bindings']
            at=row['source_reference']['offset'];raw=bytes.fromhex(row['source_hex'])
            assert blocks[group['block']][at:at+len(raw)]==raw
            keys.append((row['block'],at,row['source_hex']))
    assert len(keys)==len(set(keys))==310
    ROOT.mkdir()
    save(ROOT/'clean_source_packet.json',{**packet,'groups':selected,'records':310,
        'selected_blocks':list(range(51,58)),'complete_exchanges':7,'source_only_not_current_English':True,
        'original_census':str(path),'original_census_sha256':digest(path),
        'B50_separate_registered_integration_in_progress_not_restarted':True,'new_credit':0})
    save(ROOT/'source_selection_v1.json',dict(source_objects=310,complete_exchanges=7,
        blocks=[dict(block=g['block'],records=len(g['records'])) for g in selected],
        all_exact_clean_source_positions_rechecked=True,complete_existing_native_inventory_reused_not_replayed=True,
        source_current_comparisons_andall_five_gates_pending=True,no_current_English_read_orapproval=True,
        no_meanings_drafts_orlocalization_approval_yet=True,new_credit=0,
        evidence={str(p):digest(p) for p in [path,ROOT/'clean_source_packet.json',Path(__file__)]}))
    print('Prepared310 clean-only objects/seven complete exchanges;allsource positions exact,no current English ornew review credit.')
if __name__=='__main__':main()
