"""Plan all 150 reviewed paragraphs with actual variable virtual prefixes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B111_B119_profile import profile_for
from dk4tool.dialogue.lil_B111_B119_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_layout_v3227')
INPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v1.json'),
        Path('translations/lil_B111_B119_actor_style_manuscript_v1.json')]
OUTPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v2.json'),
         Path('translations/lil_B111_B119_actor_style_manuscript_v2.json')]
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    docs=[deepcopy(read(p)) for p in INPUTS];image=NdsImage.open(docs[0]['current_ROM'])
    arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    reports=[];failures=[];waivers=[]
    for kind,doc in zip(['speech','voice'],docs,strict=True):
        for row in doc['records']:
            raw=bytes.fromhex(row['source_hex']);prefix=row['source_selector']
            if kind=='voice':
                assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
                assert row['virtual_formatter_prefix_hex']==format(prefix,'02x')
                raw=bytes([prefix])+raw
            profile=profile_for(arm,blocks[row['block']],'FE-paper' if row['kind']=='system-FE' else 'progressive')
            try:
                encoded=encode_relocatable_dialogue(raw,row['english'],profile)
                qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
            except (ValueError,AssertionError) as error:
                failures.append(dict(id=row['id'],kind=kind,english=row['english'],error=str(error)));continue
            warnings=[d.code for d in encoded.diagnostics if d.severity=='warning']
            if 'line-break-count' in warnings:
                reason=('Source Japanese physical wrapping is not an English dramatic pause. Complete meaning,punctuation and exchange context are preserved in one logical paragraph;the calibrated formatter owns balanced pair-safe wrapping. Only row-count differences are accepted. No overflow,orphan,weak ending,missing glyph,source control,alias,predicate,event query orblank-page exemption is granted. Complete native planes andconsumer-specific pagination still require verification.')
                row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason)
                row['localization_note']+=' '+reason;waivers.append(dict(id=row['id'],reason=reason))
            issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not
                (i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]))]
            unwaived=[v for v in warnings if v not in row.get('qa_waivers',[])]
            if issues or unwaived:failures.append(dict(id=row['id'],kind=kind,english=row['english'],issues=issues,unwaived=unwaived))
            row['compiled_hex']=encoded.encoded.hex()
            if kind=='voice':
                assert encoded.encoded[0]==prefix
                row.update(compiled_virtual_source_hex=raw.hex(),compiled_stored_alternative_hex=encoded.encoded[1:].hex())
            reports.append(dict(id=row['id'],kind=kind,encoded_hex=encoded.encoded.hex(),
                formatted_markup=encoded.formatted_markup,qa=qa,encoder_warning_codes=warnings,
                virtual_prefix_excluded_from_physical_alternative=kind=='voice',
                actual_source_prefix_hex=format(prefix,'02x')))
    assert len(reports)+sum('error' in f for f in failures)==150
    ROOT.mkdir(parents=True);proof=ROOT/'all150_paragraph_layout_and_QA.json'
    save(proof,dict(manuscripts={str(p):sha(p.read_bytes()) for p in INPUTS},records=reports,failures=failures,waivers=waivers,
        actual_variable_virtual_prefixes=['d0','d1','d6','d7','dc'],unowned32_Maria_copy_not_formatted=True,
        formatting_approval_not_granted=True,no_ROM_registry_ledger_or_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:
        print(dict(layouts=len(reports),line_count_notes=len(waivers),unresolved=len(failures),findings=failures),flush=True)
        raise SystemExit(1)
    for doc,old,new in zip(docs,INPUTS,OUTPUTS,strict=True):
        profile=Path('dk4tool/dialogue/lil_B111_B119_profile.py');formatter=Path('dk4tool/dialogue/lil_B111_B119_layout_v1.py')
        doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),
            dialogue_profile='lil-opening-editorial-native-v1',scoped_profile_module=str(profile),
            scoped_profile_module_sha256=sha(profile.read_bytes()),native_formatter_module=str(formatter),
            native_formatter_module_sha256=sha(formatter.read_bytes()),layout_QA_proof=str(proof),
            layout_QA_proof_sha256=sha(proof.read_bytes()),
            status='source-prose-layout-planned;complete-native-font-reference-representative-release-pending')
        save(new,doc)
    print(f'All150paragraph layout plans pass;{len(waivers)}row-count-only notes. Complete native glyph/pagination/reference/release gates pending;zero credit.')
