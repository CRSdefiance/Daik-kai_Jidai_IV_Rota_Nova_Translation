"""Read the original consumer before interpreting an internal role field as the nameplate."""
import struct
from copy import deepcopy
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_LITTLE_ENDIAN
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retainer_source_consumer_v7828')
PRIOR=Path('work/analysis/retainer_name_triage_v7744/nine_roles18_getters147_source_blocks484_uses_nine_context_samples.json')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7827/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    verified,ledger,prior=map(read,[VERIFY,LEDGER,PRIOR])
    assert verified['ledger_sha256']==sha(LEDGER.read_bytes())
    current=ledger['current_integrated_candidate'];clean_path=Path('work/clean.nds');rom_path=Path(current['path'])
    assert current['profile']=='all-routes-unified-v7821' and sha(rom_path.read_bytes())==current['sha256']==verified['candidate_sha256']
    clean= NdsImage.open(clean_path);rom=NdsImage.open(rom_path)
    arms={'clean':clean.read_file('/__arm9__.bin'),'current':rom.read_file('/__arm9__.bin')}
    assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    dis=Cs(CS_ARCH_ARM,CS_MODE_ARM|CS_MODE_LITTLE_ENDIAN)
    ranges=[(0x7ED88,0x7EDD0,'progressive-name getter; literal pool separate'),
            (0x7EDD4,0x7EE20,'full-name getter and actor-ID wrapper'),
            (0x7F1F4,0x7F244,'original actor-ID resolver')]
    code=[]
    for lo,hi,purpose in ranges:
        a,b=arms['clean'][lo:hi],arms['current'][lo:hi]
        assert len(a)==hi-lo and a==b
        instructions=[dict(address=i.address,bytes_hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)
            for i in dis.disasm(a,BASE+lo)]
        assert len(instructions)*4==len(a)
        code.append(dict(offset=lo,end_exclusive=hi,purpose=purpose,source_current_bytes_exact=True,
            source_hex=a.hex(),sha256=sha(a),instructions=instructions))
    bypc={i['address']:(i['mnemonic'],i['operands']) for r in code for i in r['instructions']}
    expected={
        0x0207ED90:('bl','#0x207ee08'),
        0x0207ED94:('cmp','r0, #0x97'),
        0x0207ED98:('blt','#0x207eda8'),
        0x0207ED9C:('cmp','r0, #0x9f'),
        0x0207EDA0:('ldrle','r0, [pc, #0x28]'),
        0x0207EDA4:('pople','{r4, pc}'),
        0x0207EDC0:('ldr','r1, [r0]'),
        0x0207EDC4:('ldr','r1, [r1, #0x20]'),
        0x0207EDC8:('blx','r1'),
        0x0207EDE0:('cmp','r0, #0x52'),
        0x0207EDE4:('bge','#0x207edf4'),
        0x0207EDFC:('ldr','r1, [r1, #0x20]'),
        0x0207EE10:('bl','#0x20cb184'),
        0x0207EE18:('bl','#0x207f1f4'),
    }
    for pc,wanted in expected.items():assert bypc[pc]==wanted,(hex(pc),bypc[pc],wanted)
    literal_offset=0x7EDD0
    assert 0x0207EDA0+8+0x28==BASE+literal_offset
    literals={}
    for label,arm in arms.items():
        pointer=struct.unpack_from('<I',arm,literal_offset)[0];value=string(arm,pointer)
        assert value['status']=='printable-static-string'
        literals[label]=dict(literal_pool_offset=literal_offset,literal_pool_hex=arm[literal_offset:literal_offset+4].hex(),**value)
    assert literals['clean']['pointer']==literals['current']['pointer']==0x021484D4
    assert literals['clean']['text']=='水夫' and literals['clean']['hex']=='90859576'
    assert literals['current']['text']=='Sailor' and literals['current']['hex']=='5361696c6f72'
    previous_rom=read(prior['native_context_plan'])['candidate']
    previous=NdsImage.open(previous_rom)
    assert previous.read_file('/__arm9__.bin')==arms['current']
    assert previous.read_file('/COMMON/MESFILE.DK4')==rom.read_file('/COMMON/MESFILE.DK4')
    native=prior['current_original_eighteen_name_consumers'];rows=[]
    for ident in range(151,160):
        fields=next(r for r in prior['original_clean_nine_name_fields'] if r['actor_ID']==ident)
        field_offset=0x120B80+32*ident
        value=string(arms['clean'],struct.unpack_from('<I',arms['clean'],field_offset)[0])
        assert value['text']=='配下' and value['hex']=='947a89ba'
        assert fields['clean_fields'][0]['table_field']==field_offset and fields['clean_fields'][0]['text']=='配下'
        getters=[deepcopy(r) for r in native['rows'] if r['actor_ID']==ident]
        assert len(getters)==2
        progressive=next(r for r in getters if r['consumer']=='progressive-nameplate')
        catalogue=next(r for r in getters if r['consumer']=='full-catalogue')
        assert progressive['text']=='Sailor' and progressive['pointer']==literals['current']['pointer']
        assert catalogue['text']=='Retainer'
        rows.append(dict(actor_ID=ident,clean_internal_role_field=dict(offset=field_offset,**value),
            original_progressive_display_source=deepcopy(literals['clean']),
            current_progressive_display=deepcopy(literals['current']),
            exact_previous_native_getters=getters,native_getters_not_reexecuted=True,
            decision='retain-progressive-nameplate-wording',
            retention_reason='The original progressive getter deliberately returns the shared 水夫 literal for this actor ID. Sailor preserves that actual display source. The separate 配下 field is not the source for this nameplate.',
            full_name_andother_consumer_localization_remains_open=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'nine_roles_original_Sailor_nameplate_distinct_from_internal_subordinate_field.json',dict(
        format='dk4-source-name-consumer-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        clean_ROM=str(clean_path),clean_ROM_sha256=sha(clean_path.read_bytes()),current_ROM=str(rom_path),current_ROM_sha256=current['sha256'],
        clean_ARM9_sha256=sha(arms['clean']),current_ARM9_sha256=sha(arms['current']),original_source_current_code_ranges=code,
        exact_original_branch_inclusive_actor_IDs=[151,159],branch_literal=literals,rows=rows,
        prior_current_getter_proof=str(PRIOR),prior_current_getter_proof_sha256=sha(PRIOR.read_bytes()),
        prior_getter_ROM=previous_rom,prior_getter_ARM9_andCOMMON_exact_to_current=True,
        reviewed_clean_context_samples=9,reviewed_sample_speeches=129,
        broad_census_blocks=147,broad_census_direct_uses=484,broad_census_context_speeches=3150,
        not_all3150_speeches_editorially_reviewed=True,
        corrected_inference='The internal 配下 table and varied subordinate contexts do not invalidate Sailor: the original dialogue-name consumer explicitly selects 水夫. Earlier evidence remains; the broad nautical-mistranslation inference is superseded for these direct progressive nameplates.',
        full_name_Retainer_wording_indirect_typed_COMMON_andother_UI_consumers_unresolved=True,
        no_clean_native_execution_with_current_ROM_RAM=True,
        source_claim_scope='Read-only original source disassembly, exact literal/field bytes and previously executed current getters rebound by unchanged ARM9/COMMON; no new Japanese or English gameplay-nameplate capture.',
        no_global_asset_change_ornew_dialogue_credit=True,new_credit=0,new_emulator_runs=0,
        original_getter_calls_reused=18,new_native_getter_executions=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,VERIFY,Path(__file__)]},
        full207_name_review_andfull_editorial_goal_active=True,full_goal_complete=False))
    print('Nine progressive Sailor labels retained against original 水夫 consumer;separate 配下/full-name andother consumers remain open.No asset orcredit change.')
