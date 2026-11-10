"""Select complete source-block display exchanges within the proven native QA capacity."""
import argparse
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['reconstruction','capacity','out']:p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--blocks',type=int,nargs='+',required=True);a=p.parse_args()
    assert not a.out.exists() and a.blocks==sorted(set(a.blocks))
    rebuilt,capacity=map(load,(a.reconstruction,a.capacity));image=NdsImage.open(rebuilt['research_ROM'])
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');assert sha(arm)==capacity['registered_ARM9_sha256']
    assert capacity['source_current_consumer_code_exact'] and capacity['safe_QA_block_limit']==9216
    bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
    inventory,_,_=scoped_inventory();opening,speeches=inventory(arm,bank[42]);first=speeches[0]['offset']
    assert first==42 and [c['word'] for c in opening[-2:]]==[0xC200,0]
    exit_bytes=sum(len(bytes.fromhex(c['whole_command_hex'])) for c in opening[-2:]);assert exit_bytes==6
    selected=[g for g in rebuilt['groups'] if g['block'] in a.blocks]
    assert [g['block'] for g in selected]==a.blocks
    chunks=[];pending=[];used=0
    padded=lambda n:(first+n+exit_bytes+3)//4*4
    for g in selected:
        ordinary={r['new_offset']-5:r for r in g['text_records']}
        compound={r['new_offset']:r for r in g['native_objects']};actions=[];size=0
        for c in g['all_target_commands']:
            at=c['offset']
            if at in ordinary:
                assert c['word']==0x4000;action=dict(speech=ordinary[at]['id'])
            elif at in compound:
                obj=compound[at];assert c['word']==obj['word']
                request=dict(block=g['block'],source_command_offset=obj['old_offset'])
                if c['word']==0x4100:request['expected_style']=4;action=dict(style=request)
                else:assert c['word'] in [0x2100,0x2200];action=dict(menu=request)
            else:continue
            actions.append(action);size+=len(bytes.fromhex(c['whole_command_hex']))
        assert len(actions)==len(ordinary)+len(compound) and padded(size)<=9216
        if pending and padded(used+size)>9216:chunks.append((pending,used));pending=[];used=0
        pending.append(dict(block=g['block'],actions=actions));used+=size
    if pending:chunks.append((pending,used))
    fixtures=[dict(name='hodram_residual_part'+str(i),
        purpose='Representative English display QA from complete exchanges in blocks '+','.join(str(g['block']) for g in groups)+'. Native initializers and complete text commands are retained; optional-event conditions, chronology, rewards and outcomes are not activated.',
        sequence=[x for g in groups for x in g['actions']],selected_complete_source_blocks=[g['block'] for g in groups],
        estimated_padded_QA_block_bytes=padded(size)) for i,(groups,size) in enumerate(chunks,1)]
    actions=[x for f in fixtures for x in f['sequence']]
    counts={key:sum(key in x for x in actions) for key in ['speech','style','menu']}
    save(a.out,dict(fixtures=fixtures,selection_counts=counts,selected_blocks=a.blocks,
        unvisited_blocks=[g['block'] for g in rebuilt['groups'] if g['block'] not in a.blocks],
        alternate_style_variants_offline_only=True,source_order_within_exchanges_preserved=True,
        complete_block_boundary_splits_only=True,safe_QA_block_limit=9216,actual_gameplay_pending=True,new_credit=0,
        evidence={str(q):digest(q) for q in [a.reconstruction,a.capacity,Path(__file__)]}))
    print(dict(fixtures=len(fixtures),selection_counts=counts,bounded_bytes=[f['estimated_padded_QA_block_bytes'] for f in fixtures]))

if __name__=='__main__':main()
