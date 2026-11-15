"""One disclosed QA sequence: two-page layout,three source speakers andthe long menu."""
from pathlib import Path
import os
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_static_labels_v1 import plan_static_labels
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Hodram_B151_B170_focused_20261102')
REBUILT=Path('work/analysis/Hodram_B151_B170_rebuilt_20261102/reconstruction.json')
STORED=Path('work/analysis/Hodram_B151_B170_stored_20261102/stored_native_verification.json')
PROPOSAL=Path('work/analysis/Hodram_B151_B170_clean_20261102/two_static_text_slots_proposal_v1.json')
STATIC=Path('work/analysis/Hodram_B151_B170_static_labels_20261102/native_static_labels_qualification.json')

if __name__=='__main__':
    assert not ROOT.exists() or not any(ROOT.iterdir());rebuilt,stored,proposal,static=map(load,[REBUILT,STORED,PROPOSAL,STATIC])
    assert stored['reconstruction_sha256']==sha(REBUILT.read_bytes()) and stored['complete_stored_pages']==650
    assert static['proposal_sha256']==sha(PROPOSAL.read_bytes()) and load(STATIC.with_name('visual_review.json'))['all5_native_source_current_proposed_literal_planes_visually_approved']
    story_path=Path(rebuilt['research_ROM']);assert sha(story_path.read_bytes())==rebuilt['research_ROM_sha256']
    story=NdsImage.open(story_path);arm=story.read_file('/__arm9__.bin');clean_arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    target_arm,data_plan=plan_static_labels(arm,proposal,clean_arm);assert data_plan==static['complete_owned_data_plan']
    ROOT.mkdir(parents=True,exist_ok=True)
    reference=NdsImage.open(story_path);reference.replace_file('/__arm9__.bin',target_arm)
    assert all(reference.read_file(p)==v for _,p,v in story.iter_files())
    assert [p for p,v in story.iter_components() if reference.read_file(p)!=v]==['/__arm9__.bin']
    ref_path=ROOT/'Hodram_B151_B170_static_labels_RESEARCH_ONLY.nds';reference.save(ref_path)
    inverse=NdsImage.open(ref_path);inverse.replace_file('/__arm9__.bin',arm);assert bytes(inverse.rom.save())==story_path.read_bytes()
    reference_proof=ROOT/'research_reference.json'
    save(reference_proof,dict(research_ROM=str(ref_path),research_ROM_sha256=sha(ref_path.read_bytes()),story_reconstruction=str(REBUILT),
        story_reconstruction_sha256=sha(REBUILT.read_bytes()),story_ROM=str(story_path),story_ROM_sha256=sha(story_path.read_bytes()),
        ARM9_sha256=sha(target_arm),owned_data_plan=data_plan,static_qualification=str(STATIC),static_qualification_sha256=sha(STATIC.read_bytes()),
        all_other_files_components_andcomplete_serialized_parent_inverse_exact=True,not_registered_candidate=True,new_credit=0))
    doc=load(rebuilt['manuscript']);byid={r['id']:r for r in doc['records']};groups={g['block']:g for g in rebuilt['groups']}
    file_path='/data/SC1.DK4';archive=reference.read_file(file_path);bank=IlnkContainer.parse(archive).blocks
    inventory,_,_=scoped_inventory();opening,speeches=inventory(target_arm,bank[42]);first=speeches[0]['offset'];assert first==42
    initializers=[c for c in opening if c['offset']<first];assert len(initializers)==8
    prefix_ids=['DK4_MES_B156_R0087','DK4_MES_B156_R0090']+[r['id'] for r in doc['records'] if r['block']==168 and 157<=r['source_reference'].get('record_index',-1)<=181]
    assert len(prefix_ids)==9
    logical=bytearray(bank[42][:8]+bank[42][8:first]);bindings=[]
    for ident in prefix_ids:
        r=byid[ident];group=groups[r['block']];text=next(t for t in group['text_records'] if t['id']==ident)
        at=text['new_offset']-5;command=next(c for c in group['all_target_commands'] if c['offset']==at);assert command['word']==0x4000
        raw=bytes.fromhex(command['whole_command_hex']);assert raw[:6]==bytes.fromhex(r['source_complete_preamble_hex'])
        assert bank[r['block']][at:at+len(raw)]==raw
        bindings.append(dict(id=ident,block=r['block'],stored_command_offset=at,fixture_offset=len(logical),whole_target_command_hex=raw.hex(),
            stored_hex=text['stored_hex'],selector=r['source_selector'],logical_English=r['english']))
        logical+=raw
    menu_group=groups[170];menu=next(o for o in menu_group['native_objects'] if o['old_offset']==1314)
    tail_start=menu['new_offset'];tail_end=menu_group['new_logical_end'];shift=len(logical)-tail_start
    tail=bank[170][tail_start:tail_end];tail_commands=[c for c in menu_group['all_target_commands'] if c['offset']>=tail_start]
    assert tail_commands[0]['word']==0x2100 and tail_commands[-1]['word']==0
    for fix in menu_group['relative_fixups']:
        if fix['new_offset']>=tail_start:assert tail_start<=fix['new_target']<=tail_end
    for text in menu_group['text_records']:
        if text['new_offset']-5>=tail_start:
            r=byid[text['id']];bindings.append(dict(id=r['id'],block=170,stored_command_offset=text['new_offset']-5,
                fixture_offset=text['new_offset']-5+shift,stored_hex=text['stored_hex'],selector=r['source_selector'],logical_English=r['english']))
    menu_fixture=tail_start+shift;logical+=tail;struct.pack_into('<H',logical,4,len(logical)-8)
    fixture_block=bytes(logical)+bytes(-len(logical)%4);actual,actual_texts=inventory(target_arm,fixture_block)
    assert actual[-1]['word']==0 and actual[-1]['offset']+4==len(logical) and len(actual_texts)==len(bindings)
    for c in tail_commands:
        q=next(q for q in actual if q['offset']==c['offset']+shift);assert q['word']==c['word'] and q['whole_command_hex']==c['whole_command_hex']
    for row in bindings:
        q=next(q for q in actual_texts if q['offset']==row['fixture_offset']);raw=bytes.fromhex(q['whole_command_hex'])
        encoded=bytes.fromhex(row['stored_hex']);assert raw[5:6+len(encoded)]==encoded+b'\0'
        row['expected_expanded_body_hex']=encoded[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet').hex()
    changed=list(bank);changed[42]=fixture_block;fixture=NdsImage.open(ref_path);fixture.replace_file(file_path,IlnkContainer(changed).to_bytes())
    assert all(fixture.read_file(p)==v for p,v in reference.iter_components())
    assert [p for _,p,v in reference.iter_files() if fixture.read_file(p)!=v]==[file_path]
    fixture_path=ROOT/'Hodram_page_speakers_long_menu_RESEARCH_ONLY.nds';fixture.save(fixture_path)
    restored=list(changed);restored[42]=bank[42];assert IlnkContainer(restored).to_bytes()==archive
    ordinary=Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json');inputs=ROOT/'inputs.json'
    save(inputs,load(ordinary)+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,17500,240)]+[dict(start=6720,duration=3,buttons=['DOWN'])])
    save(ROOT/'fixture.json',dict(research_ROM=str(fixture_path),research_ROM_sha256=sha(fixture_path.read_bytes()),text_language='reviewed-English',
        parent=str(ref_path),parent_sha256=sha(ref_path.read_bytes()),research_reference=str(reference_proof),research_reference_sha256=sha(reference_proof.read_bytes()),
        frames=18001,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),expected_FE_bodies_hex=[],selected_records=bindings,
        prefix_record_ids=prefix_ids,long_menu_source_block=170,long_menu_source_command_offset=1314,long_menu_fixture_offset=menu_fixture,
        long_menu_labels=[r['english'] for r in menu['records']],source_tail_offset=tail_start,source_tail_end=tail_end,
        all_selected_speech_commands_andcomplete_menu_tail_byte_exact=True,original_initializers=initializers,
        retained_menu_tail_original_effects_not_claimed_purely_visual=True,selected_prefix_has_no_added_control_operations=True,
        outer_conditions_andintervening_story_explicitly_excluded=True,synthetic_cross_scene_QA_sequence_not_a_story_exchange=True,
        predicted_DOWN_frame6720_not_a_selection_result_claim=True,no_savestate_RAM_roster_money_RNG_orcondition_result_override=True,
        not_registered_candidate_or_natural_activation_or_earned_progress=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REBUILT,STORED,PROPOSAL,STATIC,ordinary,Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    for p,reason in [(ref_path,'B151-B170 story plus separately qualified15-byte static label data plan'),(fixture_path,'B151-B170 focused page/name/menu QA content fixture')]:
        assert not any(Path(v['path']).resolve()==p.resolve() for v in values);values.append(dict(path=str(p.resolve()),reason=reason+';preserve all ROMs. SHA256 '+sha(p.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before);tmp=pins.with_name('rom_retention_pins.B151_focused.pending.json');assert not tmp.exists();save(tmp,values)
    assert pins.read_bytes()==before;os.replace(tmp,pins)
    print('Pinned separate static-label research reference andone page/speaker/long-menu QA fixture. Original commands/menu tail retained;actual input/pagination/header results pending.')
