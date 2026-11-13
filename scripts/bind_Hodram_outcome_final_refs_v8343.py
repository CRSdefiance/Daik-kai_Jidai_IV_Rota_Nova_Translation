"""Bind six approved whole-exchange rows to exact clean/current/stored/final native references."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_current_binding_v8343')
OLD=Path('translations/hodram_B47_B48_editorial_manuscript_v3.json')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v4.json')
CURRENT=Path('work/analysis/Hodram_B47_B48_current_v8317c/six_exact_source_current_effective_refs_after_whole_clean_gloss_andnative_source_view.json')
STORED=Path('work/analysis/Hodram_outcome_stored_v8327/six_stored_bodies8_fresh16_reused_alignments_six_exact_native_pages.json')
RELOC=Path('work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json')
REFERENCE=Path('work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json')
APPROVAL=Path('work/analysis/Hodram_outcome_display_review_v8340/display_review_receipt.json')
NAMES=Path('translations/hodram_B47_B48_speaker_name_review_v2.json')
PACKET=ROOT/'six_exact_source_current_final_refs_registered_parent_anddisplay_binding.json'
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,current,stored,reloc,reference,approval=map(read,[OLD,CURRENT,STORED,RELOC,REFERENCE,APPROVAL])
    assert approval['manuscript_sha256']==sha(OLD.read_bytes()) and approval['name_review_sha256']==sha(NAMES.read_bytes()) and approval['all_six_five_perrecord_review_gates_true']
    parent,target,clean=[NdsImage.open(p) for p in [old['current_ROM'],reference['research_ROM'],'work/clean.nds']]
    assert sha(Path(old['current_ROM']).read_bytes())==old['current_ROM_sha256']==reference['parent_sha256'] and sha(Path(reference['research_ROM']).read_bytes())==reference['research_ROM_sha256']
    file=old['file_path'];banks=[IlnkContainer.parse(i.read_file(file)).blocks for i in [clean,parent,target]];assert len(banks[0])==len(banks[1])==len(banks[2])==325
    assert target.read_file(file)==Path(reloc['target_archive']).read_bytes() and stored['relocation_sha256']==sha(RELOC.read_bytes())
    rows=[]
    for original in old['records']:
        row=deepcopy(original);proof=next(r for r in stored['records'] if r['id']==row['id']);ref=proof['target_reference'];source_ref,prior_ref=row['source_reference'],row['current_reference']
        for bank,at,raw,length,index in [(banks[0],source_ref['offset'],row['source_hex'],source_ref['bytes'],source_ref['record_index']),(banks[1],prior_ref['offset'],row['current_hex'],prior_ref['bytes'],prior_ref['record_index']),(banks[2],ref['offset'],proof['stored_hex'],ref['bytes'],ref['record_index'])]:
            block=bank[row['block']];value=bytes.fromhex(raw);assert len(value)==length and block[at:at+length+1]==value+b'\0' and block[:at].count(b'\0')==index and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert proof['compiled_hex']==row['compiled_hex'] and ref['file_path']==file and ref['block']==row['block'] and ref['target_block_sha256']==sha(banks[2][row['block']])
        row.update(integrated_reference_pending={k:ref[k] for k in ['offset','bytes','header_offset','record_index']},final_stored_hex=proof['stored_hex'],source_current_final_reference_binding=str(ROOT/'source_current_final_reference_binding.json'),source_prose_orcompletion_credit_added=False)
        assert all(row['review'].values()) and all(row[k]==original[k] for k in ['english','compiled_hex','planned_English_markup','source_reference','current_reference','review','context','localization_note','retention_reason','qa_waivers','qa_waiver_scope']);rows.append(row)
    ROOT.mkdir(parents=True);doc=deepcopy(old);doc.update(records=rows,predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),source_current_final_reference_binding=str(ROOT/'source_current_final_reference_binding.json'),current_source_packet=str(PACKET),no_prose_compiler_display_orname_change=True)
    save(DOC,doc);packet=deepcopy(current);packet['records']=deepcopy(rows)
    for group in packet['groups']:
        group.update(source_header_hex=bytes.fromhex(group['clean_block_hex'])[:8].hex(),current_header_hex=bytes.fromhex(group['current_block_hex'])[:8].hex(),records=[deepcopy(r) for r in rows if r['block']==group['block']])
    packet.update(predecessor_current_packet=str(CURRENT),predecessor_current_packet_sha256=sha(CURRENT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_current_final_refs_bound_no_new_editorial_oractual_credit=True)
    save(PACKET,packet);save(ROOT/'source_current_final_reference_binding.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),packet=str(PACKET),packet_sha256=sha(PACKET.read_bytes()),approved_predecessor_manuscript=str(OLD),approved_predecessor_manuscript_sha256=sha(OLD.read_bytes()),name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),records=6,all_complete_source_current_final_refs_hex_preambles_record_indices_bound=True,
        all_source_prose_context_decisions_reasons_compiler_waivers_andfive_gates_unchanged=True,reference_ROM=reference['research_ROM'],reference_ROM_sha256=reference['research_ROM_sha256'],new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,CURRENT,STORED,RELOC,REFERENCE,APPROVAL,NAMES,Path(__file__)]}))
    print('Six finalrefs bound toapprovedv4:exactclean/current/storedrefs,completepreambles,NULs/recordindices;allprose/native/actualapprovals unchanged.Independent rebuild andpolicy next;zero credit.')
