"""Exact source-object census;decoding/coverage labels do not classify prose."""
import re
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_source_universe_v2701c')
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);auditpath=Path('work/analysis/editorial_handoff_verification_v2700/verified_handoff.json');audit=read(auditpath)
    assert sha(lp.read_bytes())==audit['ledger_sha256'];candidate=ledger['current_integrated_candidate'];rom=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds')
    completed_rows={historical_key(r):r for g in ledger['completed_editorial_families'] for r in g['records']};completed=set(completed_rows);assert len(completed)==2256
    ROOT.mkdir(parents=True);outputs=[]
    def diagnostic(raw):
        try:
            text=raw.decode('cp932');return dict(decoding='strict-cp932-Japanese-candidate' if contains_japanese(text) else 'strict-cp932-no-Japanese-detected',strict_decoded_text=text)
        except UnicodeDecodeError as e:
            value=dict(decoding='strict-cp932-rejected',decode_error_start=e.start,decode_error_end=e.end,decode_error_reason=e.reason)
            # This is only a diagnostic lead. In particular an ambiguous SJIS
            # lead byte is never globally stripped or accepted as a speaker.
            if len(raw)>1:
                try:
                    suffix=raw[1:].decode('cp932')
                    if contains_japanese(suffix):value.update(one_byte_suffix_decodes_Japanese_diagnostic_only=True,first_byte_hex=raw[:1].hex(),suffix_diagnostic_text=suffix,source_consumer_prefix_classification_required=True)
                except UnicodeDecodeError:pass
            return value
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'));rows=[]
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for n in range(3668):
        key=('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}');r=jp[n]
        rows.append(dict(id=key[1],message_ID=n,source_reference=ref(r),source_hex=r.text.hex(),source_sha256=sha(r.text),current_reference=ref(en[n]),current_hex=en[n].text.hex(),current_diagnostic=diagnostic(en[n].text),completed_file_qualified_key=key in completed,reviewed_but_incomplete=n in ledger['reviewed_but_incomplete_COMMON_IDs'],**diagnostic(r.text)))
    commonpath=ROOT/'COMMON_native_3668_source_current_catalog.json'
    counts=dict(Counter(r['decoding'] for r in rows));save(commonpath,dict(file_path='/COMMON/MESFILE.DK4',source_file_sha256=sha(clean.read_file('/COMMON/MESFILE.DK4')),current_file_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),records=rows,counts=counts,
        native_message_count=3668,completed_keys=sum(r['completed_file_qualified_key'] for r in rows),no_all_records_are_player_facing_or_decoding_equals_prose_claim=True,completion_credit_added=0,full_goal_complete=False))
    outputs.append(dict(file_path='/COMMON/MESFILE.DK4',path=str(commonpath),sha256=sha(commonpath.read_bytes()),native_objects=3668,completed_key_matches=sum(r['completed_file_qualified_key'] for r in rows),counts=counts))
    for route in range(4):
        path=f'/data/SC{route}.DK4';data=clean.read_file(path);container=IlnkContainer.parse(data);offset=8+(len(container.blocks)+1)*4;objects=[];empty=0
        for block,body in enumerate(container.blocks):
            cursor=0
            for segment,raw in enumerate(body.split(b'\0')):
                if not raw:empty+=1
                else:
                    key=(path,f'DK4_MES_B{block}_R{segment:04d}');at=offset+cursor;assert data[at:at+len(raw)]==raw
                    objects.append(dict(id=key[1],file_path=path,source_reference=dict(block=block,NUL_segment_index=segment,offset_in_block=cursor,absolute_file_offset=at,bytes=len(raw)),source_hex=raw.hex(),source_sha256=sha(raw),
                        raw_control_byte_hex=[f'{v:02x}' for v in sorted(set(raw)) if v<32 and v!=10],completed_file_qualified_key=key in completed,**diagnostic(raw)))
                cursor+=len(raw)+1
            offset+=len(body)
        assert offset==len(data)
        nul_keys={r['id'] for r in objects};choice_subobjects=[]
        for key,row in completed_rows.items():
            if key[0]!=path or key[1] in nul_keys:continue
            assert path=='/data/SC2.DK4' and 'CHOICE' in key[1]
            match=re.search(r'_B([0-9]+)_',key[1]);assert match
            block=int(match.group(1));ref=row['source_reference'];start=ref['offset'];raw=bytes.fromhex(row['source_hex'])
            assert len(raw)==ref['bytes'] and container.blocks[block][start:start+len(raw)]==raw
            containing=[o['id'] for o in objects if o['source_reference']['block']==block and o['source_reference']['offset_in_block']<=start and start+len(raw)<=o['source_reference']['offset_in_block']+o['source_reference']['bytes']]
            assert len(containing)==1
            choice_subobjects.append(dict(id=key[1],file_path=path,block=block,offset_in_block=start,source_hex=raw.hex(),source_sha256=sha(raw),bytes=len(raw),source_exact=True,containing_native_NUL_object=containing[0],completed_choice_key=True,not_a_new_NUL_object_or_new_review=True))
        counts=dict(Counter(r['decoding'] for r in objects));out=ROOT/f'SC{route}_all_nonempty_native_NUL_objects.json'
        save(out,dict(file_path=path,source_file_sha256=sha(data),current_file_sha256=sha(rom.read_file(path)),ILNK_blocks=len(container.blocks),nonempty_objects=len(objects),empty_segments=empty,counts=counts,objects=objects,completed_choice_subobjects=choice_subobjects,
            segmentation_is_native_NUL_inventory_not_dialogue_or_reachability_classification=True,completed_key_matches_do_not_certify_unexamined_binary_or_prefix_objects=True,current_file_hash_only_no_unverified_current_record_mapping=True,
            no_global_SJIS_prefix_stripping_or_rejected_record_approval=True,completion_credit_added=0,full_goal_complete=False))
        outputs.append(dict(file_path=path,path=str(out),sha256=sha(out.read_bytes()),native_objects=len(objects),ILNK_blocks=len(container.blocks),completed_key_matches=sum(r['completed_file_qualified_key'] for r in objects),completed_choice_subobjects=len(choice_subobjects),completed_key_matches_including_choice_subobjects=sum(r['completed_file_qualified_key'] for r in objects)+len(choice_subobjects),counts=counts,
            rejected_one_byte_suffix_Japanese_leads=sum(r.get('one_byte_suffix_decodes_Japanese_diagnostic_only',False) for r in objects)))
    assert sum(f['completed_key_matches']+f.get('completed_choice_subobjects',0) for f in outputs)==2256
    save(ROOT/'source_universe_inventory.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=sha(Path(candidate['path']).read_bytes()),
        ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),prior_audit=str(auditpath),prior_audit_sha256=sha(auditpath.read_bytes()),files=outputs,source_prose_reviewed=2259,completed_editorial_keys=2256,
        unresolved_existing_source_prose_COMMON=[750,751,752],five_named_target_leads_uncredited=[2187,2188,2189,2190,2191],
        interpretation='This extends the exact clean native-source inventory beyond decoded CSV rows. Route NUL identifiers use the existing ledger four-digit segment spelling. The preserved2701predecessor used unpadded spellings andits zero route-key overlaps must not be interpreted as missing previous reviews. COMMON uses its original proven3668message directory. Route files enumerate every nonempty NUL object,including strict CP932 failures;Japanese detection andone-byte suffix diagnostics do not establish dialogue,presentation-prefix meaning,reachability or approval. No ambiguous Shift-JIS byte is stripped. Source consumers andcomplete surrounding exchanges must classify each candidate before review or translation. File-qualified completion-key overlap is navigation metadata,not proof that every underlying source object or rejected segment was reviewed. Eight existing SC2choice keys use distinct opcode/option identifiers rather than NUL identifiers;their exact source bytes,block offsets andcontaining NULobjects are separately bound,andall2256completed keys reconcile. This does not inventory all unseen choice opcodes. Current route file hashes are bound without inventing record mappings. Other files/resources,help/UIprose,graphics andlater older-record technical re-audit remain in scope;this is not a full-ROM prose denominator.',
        next_action='Resolve market750-752callers while continuing untouched route/shared/town/shop/random/help/player prose. Prioritize source-consumer classification of rejected objects,including the known94presentation-prefix issue;do not equate decoder acceptance with route completeness.',
        no_prose_revision_ROM_registry_or_completion_credit=True,source_prose_credit_added=0,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for f in outputs:print(f['file_path'],f['native_objects'],f['counts'],'completed-key-overlap',f['completed_key_matches'])
    print('Source-object inventory only;no new editorial completion or whole-ROM denominator claim.')
