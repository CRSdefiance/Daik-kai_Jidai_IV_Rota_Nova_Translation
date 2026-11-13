"""Reviewed faction grammar after V1086;only text and native metadata may change."""
import struct
from pathlib import Path
from types import FunctionType
from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.sighting_editorial import current_entries as previous_entries
from dk4tool.patch.common_single_cache_v861 import SINGLE,entries,repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.sighting_layout_v1069 import IDS,PROFILE,compiled
from scripts.sighting_labels_v1083b import FIELDS
from scripts.verify_village_wrap_v608 import read

SOURCE_COMMON='82fc504746a28a5e95dafeabdc836c5986c90f252988cd320311e83998feb4ea'
SOURCE_ARM='4b1d8e1fd7f7113415e43d3694bda0729e0ff67afbbae9531480c497b976db17'
CONFIG='translations/sighting_grammar_editorial_release_v1.json'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['encoder']=='dialogue-relocatable-v1' and doc['consumer_layout_profile']==PROFILE
    assert tuple(r['message_id'] for r in doc['records'])==IDS
    assert doc['current_COMMON_sha256']==SOURCE_COMMON and doc['current_ARM9_sha256']==SOURCE_ARM
    clean,canonical=map(NdsImage.open,('work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    jp=parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    accepted=parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    before=previous_entries(common,arm);authored={}
    for row in doc['records']:
        n=row['message_id']
        assert row['source_hex']==jp[n].text.hex() and row['canonical_source_hex']==accepted[n].text.hex()
        assert row['current_text_hex']==before[n].text.hex()
        assert row['native_argument_count']==jp[n].text.count(b'%s')==2 and row['source_native_macros']==[]
        assert all(row['review'].get(g) for g in ('source','context','localization','naturalness','formatting'))
        payload=compiled(row);assert payload.hex()==row['compiled_hex'] and b'\n' not in payload
        authored[n]=payload
    assert all(authored[n]!=before[n].text for n in IDS)
    pack=FunctionType(repack.__code__,{**repack.__globals__,'previous_entries':previous_entries})
    before,blocks,first,last,selected,opaque,groups,attempts=pack(common,arm,authored)
    assert [first,last]==[7,7]
    target,rebuilt,fields=bytearray(arm),list(blocks),[]
    for block,(group,body) in zip(range(first,last+1),groups,strict=True):
        rebuilt[block]=body;at=parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target,at,group[0][0],len(body));fields.append((at,4))
        for n,offset,payload in group:
            at=parser.TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,offset);fields.append((at,2))
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target)
    directory=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET]);after=entries(c,a,directory)
    assert len(before)==len(after)==3668
    assert all(b.text==authored.get(e.message_id,e.text) for e,b in zip(before,after,strict=True))
    assert all(blocks[b]==rebuilt[b] for b in range(41) if b!=7)
    for n,payload in opaque.items():
        row=after[n];assert rebuilt[row.block][row.block_offset:row.copy_end]==payload
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==arm and cache_plan(a)==cache_plan(arm)
    old_code,new_code=MainCodeFile(arm,0x02000000),MainCodeFile(a,0x02000000)
    shape=lambda code:[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert shape(old_code)==shape(new_code)
    assert all(old_code.sections[n].data==new_code.sections[n].data for n in (1,2,3))
    assert len(new_code.sections[3].data)-48==123040
    for at,old,new in FIELDS:assert arm[at:at+len(new)]==a[at:at+len(new)]==new
    return c,a,{'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS],'reviewed_native_IDs':list(IDS),
        'metadata_fields':fields,'directory_sha256':directory,'repacked_block_range':[first,last],
        'packing_attempts':attempts,'repacked_native_IDs':[e.message_id for e in selected],
        'repacked_block_lengths':[len(rebuilt[b]) for b in range(first,last+1)],
        'all3653_unselected_strings_and_opaque_payloads_exact':True,'opaque_payload_IDs':sorted(opaque),
        'all_unselected_blocks_exact':True,'all_ARM9_bytes_except_native_message_metadata_exact':True,
        'entire_renderer_selector_and_previous_runtime_bytes_exact':True,
        'vicinity_and_Armed_Latina_labels_and_all_other_name_data_exact':True,
        'all15_one_paragraphs_no_LF_before_macro_expansion':True,'existing_single_cache_code_hex_preserved':SINGLE.hex(),
        'all_sections_BSS_cache_arenas_and_entire123040_staged_payload_unchanged':True,
        'actual_new_wording_gameplay_not_proven_by_this_stage':True,'experimental':True,'full_goal_complete':False}


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-sighting-grammar-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript)
    for key in ('native_context_proof','source_context_supplement','native_font_proof','visual_review','supersedes_manuscript'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],key
    draft=read(doc['supersedes_manuscript'])
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in draft['records']]
    context,supplement,font,visual=[read(doc[k]) for k in ('native_context_proof','source_context_supplement','native_font_proof','visual_review')]
    assert len(context['all208_original_actor_voice_selections'])==len(supplement['all208_original_attacked_voice_selections'])==208
    assert context['native_argument_order']==['relative-bearing-label','complete-faction-label']
    assert font['complete_native_font_cases']==len(font['cases'])==2700
    assert font['current_ROM_ARM9_sha256']==SOURCE_ARM
    assert visual['all15_source_meaning_voice_and_complete20_faction_substitutions_read_aloud']
    assert len(visual['15_invalid_source_control_printf_and_alignment_inputs_rejected'])==15
    for sheet in visual['all_current_review_sheets_visually_inspected']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    rows={r['message_id']:r for r in doc['records']}
    for case in font['cases']:
        assert compiled(rows[case['message_ID']]).hex()==case['compiled_hex']
        assert case['whole228x64_native_and_independent_font_match'] and case['complete_leading_trailing_letters_and_uniform_native_margin']
        assert not case['weak_line_end_indices'] and not case['short_final_row']
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    assert proof['directory_sha256']==config['directory_sha256']
    copies,audit=read(config['native_copy_proof']),read(config['native_consumer_audit'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    assert audit['batch_sha256']==sha(manuscript.read_bytes()) and len(audit['records'])==15
    assert audit['blocking_errors']==audit['unwaived_warnings']==0
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
