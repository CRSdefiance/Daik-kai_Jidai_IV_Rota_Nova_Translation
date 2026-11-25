"""Keep the approved318 pages; qualify one source-bound FE storage alignment amendment."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_FE_storage_padding_v1 import remove_FE_text_parity_space
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    out=ROOT/'reconstruction_v2';assert not out.exists()
    prior_path=ROOT/'reconstruction_v1/reconstruction.json';prior=load(prior_path)
    for field in ['manuscript','plan','native','packet','menu','styles','research_ROM','target_archive']:
        assert sha(Path(prior[field]).read_bytes())==prior[field+'_sha256']
    doc=load(prior['manuscript']);assert doc['current_ROM_sha256']==prior['parent_sha256']
    registered=load('work/maria_B50_release_v1/registered_release_verification.json')
    assert prior['parent_sha256']==registered['candidate_sha256'] and sha(Path('translations/release_stack.json').read_bytes())==registered['registry_sha256']
    image=NdsImage.open(prior['research_ROM']);parent=NdsImage.open(prior['parent']);arm=image.read_file('/__arm9__.bin')
    assert arm==parent.read_file('/__arm9__.bin')
    bank=IlnkContainer.parse(image.read_file('/data/SC3.DK4'));blocks=list(bank.blocks)
    group=next(g for g in prior['groups'] if g['block']==54)
    text=next(r for r in group['text_records'] if r['id']=='DK4_MES_B54_R0507')
    row=next(r for r in doc['records'] if r['id']==text['id'])
    assert row['source_complete_preamble_hex']=='0040ffff00fe' and row['source_reference']['offset']==4509
    assert text['source_hex']==row['source_hex'] and text['current_hex']==row['current_hex']
    assert text['parity_space_added'] and text['stored_hex']==text['compiled_hex']+'20'
    command=next(c for c in group['all_target_commands'] if c['offset']==text['new_offset']-5)
    owner=dict(id=text['id'],command_offset=command['offset'],compiled_hex=text['compiled_hex'],
        stored_command_hex=command['whole_command_hex'],source_complete_preamble_hex=row['source_complete_preamble_hex'],
        source_reference=row['source_reference'],current_reference=row['current_reference'],source_hex=row['source_hex'],current_hex=row['current_hex'])
    inventory,_,_=scoped_inventory();target,receipt=remove_FE_text_parity_space(arm,blocks[54],owner,inventory)
    assert target!=blocks[54] and receipt['full_block_inverse_exact']
    negatives=[]
    for key in ['control','compiled','offset','stored']:
        attempt=deepcopy(owner)
        if key=='control':attempt['source_complete_preamble_hex']='0040ffff0000'
        elif key=='compiled':attempt['compiled_hex']='fe41'
        elif key=='offset':attempt['command_offset']+=2
        else:attempt['stored_command_hex']=attempt['stored_command_hex'][:-2]+'01'
        try:remove_FE_text_parity_space(arm,blocks[54],attempt,inventory)
        except (AssertionError,ValueError):negatives.append(key)
        else:raise AssertionError('Accepted malformed owned alignment '+key)
    assert len(negatives)==4
    new=deepcopy(prior);new_group=next(g for g in new['groups'] if g['block']==54)
    mapping={c['old_offset']:c['new_offset'] for c in receipt['command_map']}
    for r in new_group['text_records']:
        r['new_offset']=mapping[r['new_offset']-5]+5
        if r['id']==owner['id']:r.update(stored_hex=r['compiled_hex'],parity_space_added=False,owned_FE_storage_alignment=True)
        raw=bytes.fromhex(r['stored_hex']);at=r['new_offset']
        assert target[at:at+len(raw)+1]==raw+b'\0'
        r['new_record_index']=target[:at].count(b'\0')
    for c in new_group['command_map']:
        c['new_offset']=mapping[c['new_offset']]
        actual=next(q for q in receipt['all_target_commands'] if q['offset']==c['new_offset'])
        c['new_extent']=actual['native_extent']
    amendments={f['old_offset']:f for f in receipt['relative_fixups']}
    for f in new_group['relative_fixups']:
        amendment=amendments[f['new_offset']]
        assert f['new_span']==amendment['old_span'] and f['new_target']==amendment['old_target']
        f.update(new_offset=amendment['new_offset'],new_span=amendment['new_span'],new_target=amendment['new_target'])
    out.mkdir();block_path=out/'B54_RESEARCH_ONLY.bin';block_path.write_bytes(target)
    receipt_path=out/'FE_storage_alignment.json';save(receipt_path,dict(**receipt,semantic_negatives_rejected=negatives,
        previous_reconstruction=str(prior_path),previous_reconstruction_sha256=sha(prior_path.read_bytes()),
        no_new_pages_no_changes_to_compiled_text_controls_orpixels=True))
    new_group.update(target_block=str(block_path),target_sha256=sha(target),target_bytes=len(target),
        all_target_commands=receipt['all_target_commands'],new_logical_end=receipt['new_logical_end'],
        new_tail_hex=target[receipt['new_logical_end']:].hex(),owned_FE_storage_amendment=str(receipt_path),
        owned_FE_storage_amendment_sha256=sha(receipt_path.read_bytes()))
    blocks[54]=target;resource=IlnkContainer(blocks).to_bytes()
    inverse=list(blocks);inverse[54]=bank.blocks[54];assert IlnkContainer(inverse).to_bytes()==image.read_file('/data/SC3.DK4')
    image.replace_file('/data/SC3.DK4',resource)
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==['/data/SC3.DK4']
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    rom=out/'reviewed_RESEARCH_ONLY.nds';image.save(rom)
    reopened=NdsImage.open(rom);assert reopened.read_file('/data/SC3.DK4')==resource
    reopened.replace_file('/data/SC3.DK4',parent.read_file('/data/SC3.DK4'))
    assert bytes(reopened.rom.save())==Path(prior['parent']).read_bytes()
    archive_path=out/'reviewed_RESEARCH_ONLY.DK4';archive_path.write_bytes(resource)
    new.update(target_archive=str(archive_path),target_archive_sha256=sha(resource),research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        initial_reconstruction=str(prior_path),initial_reconstruction_sha256=sha(prior_path.read_bytes()),
        owned_FE_storage_amendment=str(receipt_path),owned_FE_storage_amendment_sha256=sha(receipt_path.read_bytes()),
        composed_block_archive_andserialized_parent_inverses_exact=True,all318_compiled_native_pages_unchanged=True,
        all_source_native_commands_preserved=True,stored_catalogue_loaders_gameplay_andregistered_release_pending=True)
    new['producers'].update({str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/script/reviewed_FE_storage_padding_v1.py')]})
    save(out/'reconstruction.json',new)
    pins=Path('translations/rom_retention_pins.json');values=load(pins);absolute=str(rom.resolve())
    if not any(p['path']==absolute for p in values):values.append(dict(path=absolute,reason='Preserve Maria310 native FE storage alignment research and all original318 compiled pages.'))
    save(pins,values)
    print('Qualified source-bound FE storage alignment;604 commands/132 relative sites and318 compiled pages preserved;',new['research_ROM_sha256'])

if __name__=='__main__':main()
