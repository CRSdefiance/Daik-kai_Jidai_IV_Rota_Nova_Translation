"""Rebuild only ten B210 speech bodies with exact preambles, opaque leaves and full inverse."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B210_relocation_research_v6513');DOC=Path('translations/lil_B210_editorial_manuscript_v1.json');SOURCE=Path('work/analysis/lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json');FONT=Path('work/analysis/lil_B210_research_fonts_v6508/all10_bodies10_complete_native_pages_and80_alignments_RESEARCH.json');VIEW=Path('work/analysis/lil_B210_source_native_view_v6512/ten_source_objects39_body_name_holds_ten_English_native_pages_and_name_literals_viewed.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,source,font,view=map(read,[DOC,SOURCE,FONT,VIEW]);assert font['manuscript_sha256']==sha(DOC.read_bytes()) and not view['visual_review_pending'];image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');file=image.read_file('/data/SC2.DK4');bank=IlnkContainer.parse(file).blocks;block=bank[210];assert len(block)==688 and block[686:]==bytes(2);inventory,walker,invsource=scoped_inventory();commands,speeches=inventory(arm,block);assert len(commands)==12 and len(speeches)==10 and commands==source['blocks'][0]['all_current_native_commands']
    fonts={r['id']:r for r in font['records']};patches=[];refs=[]
    for row in doc['records']:
        at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);assert block[at:at+len(old)+1]==old+b'\0' and block[at-5:at+1].hex()==row['source_complete_preamble_hex'];compiled=bytes.fromhex(fonts[row['id']]['compiled_hex']);value=compiled;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        assert value[0]==old[0]==row['source_selector'] and len(value)%2==len(old)%2 and b'\0' not in value;patches.append(dict(start=at,end=at+len(old),old=old,value=value));refs.append(dict(id=row['id'],old_offset=at,old_length=len(old),new_length=len(value),compiled_hex=compiled.hex(),target_hex=value.hex(),parity_space_added=pad,source_reference=row['source_reference'],current_reference=row['current_reference'],source_preamble_hex=row['source_complete_preamble_hex']))
    patches.sort(key=lambda p:p['start']);assert len(patches)==10 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            assert not p['start']<offset<p['end'],'undeclared interior text reference'
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:686]);logical=bytearray(b''.join(pieces));assert len(logical)==mapped(686)<0x2400;struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4);newcommands,newspoken=inventory(arm,target);assert len(newcommands)==12 and len(newspoken)==10;maps=[]
    for old,new in zip(commands,newcommands,strict=True):
        assert old['word']==new['word'] and mapped(old['offset'])==new['offset'] and mapped(old['offset']+old['native_extent'])==new['offset']+new['native_extent'] and not old['ancestor_0100_offsets'] and not new['ancestor_0100_offsets']
        n=6 if old['word']==0x4000 else old['native_extent'];assert block[old['offset']:old['offset']+n]==target[new['offset']:new['offset']+n];maps.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],old_native_extent=old['native_extent'],new_native_extent=new['native_extent']))
    for ref in refs:
        at=mapped(ref['old_offset']);ref.update(new_offset=at,new_record_index=target[:at].count(b'\0'));assert target[at:at+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0'
    inverse=bytearray(logical);struct.pack_into('<H',inverse,4,678)
    for p in reversed(patches):at=mapped(p['start']);inverse[at:at+len(p['value'])]=p['old']
    assert bytes(inverse)+block[686:]==block;end=mapped(682);assert target[end:end+4]==bytes(4) and end+4==len(logical);ROOT.mkdir(parents=True);bp=ROOT/'SC2_block210_RESEARCH_ONLY.bin';bp.write_bytes(target);newbank=list(bank);newbank[210]=target;data=IlnkContainer(newbank).to_bytes();sp=ROOT/'SC2_RESEARCH_ONLY.DK4';sp.write_bytes(data);assert [i for i,(a,b) in enumerate(zip(bank,IlnkContainer.parse(data).blocks,strict=True)) if a!=b]==[210]
    save(ROOT/'ten_speech_relocation_complete_preambles_A000_end_and_full_inverse_RESEARCH.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),target_SC2=str(sp),target_SC2_sha256=sha(data),source_SC2_sha256=sha(file),blocks=[dict(block=210,source_block_sha256=sha(block),research_block_sha256=sha(target),source_bytes=688,source_logical_end=686,source_tail_bytes=2,research_bytes=len(target),research_logical_end=len(logical),research_tail_bytes=len(target)-len(logical),research_block=str(bp),text_records=refs,mapped_native_commands=maps,actor_style_commands=[],choice_commands=[],relative_skip_fixups=[],original_A000_map=next(c for c in maps if c['word']==0xA000),complete_end_map=dict(source_offset=682,target_offset=end,extent=4),all12_commands10_preambles_one_A000_and_complete_end_preserved=True,inverse_recovers_every_original688_byte=True)],all335_other_blocks_exact=True,external_references_complete=False,not_release_approved_relocation_map=True,final_stored_planes_external_entries_loaders_actual_English_and_atomic_release_pending=True,name_asset_unchanged_and_full_catalogue_typography_correction_separate=True,all10_manuscript_formatting_gates_still_false=True,source_prose_or_completion_credit_added=0,new_ROMs=0,new_emulator_runs=0,explicit_unmatched_native_walk=walker,unchanged_inventory_function=invsource,evidence={str(p):sha(p.read_bytes()) for p in [DOC,SOURCE,FONT,VIEW,Path(__file__)]},full_goal_complete=False));print(dict(source=688,target_stored=len(target),target_logical=len(logical),tail=len(target)-len(logical),complete_end=end,commands=12,preambles=10,parity_tail_spaces=sum(r['parity_space_added'] for r in refs),full_inverse=True,credit=0))
