"""Flatten327 actual native speech commands without turning FE continuation pages into source credits."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

REBUILT=Path('work/analysis/Rafael_B81_B84_rebuilt_20261105/reconstruction.json')
FORMAT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
CHILD=Path('work/analysis/Rafael_B84_FE_pagination_20261105')
OUT=Path('work/analysis/Rafael330_stored_consumer_inputs_20261105')

if __name__=='__main__':
    assert not OUT.exists();rebuilt=load(REBUILT);doc=load(Path(rebuilt['manuscript']))
    native,plans=[load(FORMAT/p) for p in ['combined_native_v5.json','automatic_subset_v5/automatic_plans.json']]
    childdoc,childnative,childplans=[load(CHILD/p) for p in ['child_page_manuscript_v1.json','native_v1/compiled_native_pages.json','automatic_v1/automatic_plans.json']]
    assert native['runtime']==childnative['runtime'] and native['font_sha256']==childnative['font_sha256']
    parentnative=load(FORMAT/'native_subset_v2/compiled_native_pages.json')
    assert parentnative['source_owned_target_page_adapter']==childnative['source_owned_target_page_adapter']
    assert parentnative['source_owned_FE_expected_value_adapter']==childnative['source_owned_FE_expected_value_adapter']
    rows=[deepcopy(r) for r in doc['records'] if r['kind']!='typed-choice-label' and r['id'] not in {o['source_ID'] for o in childdoc['pagination_owners']}]
    rows+=deepcopy(childdoc['records']);assert len(rows)==327
    byid={r['id']:r for r in rows};parents={r['source_ID']:r for r in childdoc['pagination_owners']}
    byparentchild={o['source_ID']:o['child_IDs'] for o in childdoc['pagination_owners']}
    allnative=[*deepcopy(native['records']),*deepcopy(childnative['records'])]
    allplans=[*deepcopy(plans['records']),*deepcopy(childplans['records'])]
    assert {r['id'] for r in allnative}=={r['id'] for r in allplans}==set(byid)
    image=NdsImage.open(rebuilt['research_ROM']);assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    bank=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    groups=[];texts=[];relativecount=0
    for group in rebuilt['groups']:
        block=bank[group['block']];first=group['first_page_reconstruction'];pp=group['FE_pagination']
        mapped={r['old_offset']:r['new_offset'] for r in pp['original_command_map']} if pp else {}
        entries=[]
        for text in first['text_records']:
            item=deepcopy(text);parent=text['id'];oldat=text['new_offset']-5
            at=mapped[oldat]+5 if pp else text['new_offset']
            item.update(id=byparentchild[parent][0] if parent in parents else parent,
                new_offset=at,new_record_index=block[:at].count(b'\0'),source_editorial_ID=parent,
                complete_source_preamble_hex=byid[byparentchild[parent][0] if parent in parents else parent]['source_complete_preamble_hex'])
            assert block[at:at+len(bytes.fromhex(item['stored_hex']))+1]==bytes.fromhex(item['stored_hex'])+b'\0'
            entries.append(item)
        if pp:
            for child in pp['continuations']:
                parent=child['source_ID'];ident=byparentchild[parent][1];at=child['new_command_offset']+5
                entries.append(dict(id=ident,source_editorial_ID=parent,new_offset=at,new_record_index=block[:at].count(b'\0'),
                    compiled_hex=child['encoded_hex'],stored_hex=child['stored_hex'],
                    parity_space_added=child['stored_hex']!=child['encoded_hex'],
                    complete_source_preamble_hex=child['complete_source_preamble_hex'],native_child_page=2))
        entries.sort(key=lambda r:r['new_offset']);assert len(entries)==group['final_speech_commands']
        for text in entries:
            raw=bytes.fromhex(text['stored_hex']);at=text['new_offset']
            assert block[at-5:at+1].hex()==text['complete_source_preamble_hex']
            assert block[at:at+len(raw)+1]==raw+b'\0';texts.append(text)
        relatives=[]
        for fix in first['relative_fixups']:
            at=mapped[fix['new_offset']] if pp else fix['new_offset']
            span=struct.unpack_from('<H',block,at+2)[0]
            relatives.append({**fix,'new_offset':at,'new_span':span,'new_target':at+4+span})
        relativecount+=len(relatives)
        typed=[]
        for menu in first['native_objects']:
            at=mapped[menu['new_offset']] if pp else menu['new_offset']
            assert block[at:at+len(bytes.fromhex(menu['compiled_hex']))].hex()==menu['compiled_hex']
            typed.append({**menu,'new_offset':at})
        groups.append(dict(block=group['block'],target_sha256=group['target_sha256'],text_records=entries,
            relative_fixups=relatives,typed_objects=typed,all_target_commands=group['all_target_commands'],
            new_logical_end=group['new_logical_end'],current_bytes=group['current_bytes'],target_bytes=group['target_bytes']))
    assert len(texts)==327 and len({r['id'] for r in texts})==327
    OUT.mkdir();flatdoc=deepcopy(doc);flatdoc.update(records=rows,physical_speech_objects=327,ordinary_speech_objects=311,FE_speech_objects=16,
        source_editorial_speeches=325,virtual_FE_children=4,typed_choice_objects=0,
        source_manuscript=rebuilt['source_manuscript'],source_manuscript_sha256=rebuilt['source_manuscript_sha256'],
        native_consumer_view_only_not_new_source_coverage=True)
    docpath=OUT/'native_consumer_manuscript.json';save(docpath,flatdoc)
    planpath=OUT/'native_consumer_plans.json';save(planpath,dict(manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),records=allplans,failures=[],new_credit=0))
    nativepath=OUT/'native_consumer_planes.json';save(nativepath,dict(manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),
        plan=str(planpath),plan_sha256=sha(planpath.read_bytes()),runtime=native['runtime'],font_sha256=native['font_sha256'],records=allnative,pages=336,
        source_owned_target_page_adapter=parentnative['source_owned_target_page_adapter'],
        source_owned_FE_expected_value_adapter=parentnative['source_owned_FE_expected_value_adapter'],
        all_body_native_pages_directly_viewed=True,original323_record_native_proof=str(FORMAT/'combined_native_v5.json'),
        four_FE_child_page_native_proof=str(CHILD/'native_v1/compiled_native_pages.json'),new_credit=0))
    save(OUT/'native_consumer_reconstruction.json',{**rebuilt,'manuscript':str(docpath),'manuscript_sha256':sha(docpath.read_bytes()),
        'native':str(nativepath),'native_sha256':sha(nativepath.read_bytes()),'plan':str(planpath),'plan_sha256':sha(planpath.read_bytes()),
        'groups':groups,'speech_count':327,'relative_sites':relativecount,'complete_reconstruction':str(REBUILT),'complete_reconstruction_sha256':sha(REBUILT.read_bytes()),
        'native_consumer_view_not_additional_source_coverage':True})
    print('Bound327 stored native commands/336 viewed pages,two menus and',relativecount,'final relocated branch sites;source credit remains330 objects.')
