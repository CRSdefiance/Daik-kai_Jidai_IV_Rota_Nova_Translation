"""Complete28 bridge-duty comments within the preserved proven single8KiB cache."""

import struct
from types import FunctionType
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import SINGLE, entries, repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.planning_finance_editorial_v2 import current_entries as previous_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.planning_finance_layout_v860 import compiled
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(1471,1499))
SOURCE_COMMON='0caab77a02c5e25399757be42d3dc7bc6f5811e92c042ebaa4e059dd7193f0e9'
SOURCE_ARM='2e02de94402b25a90d6889dd7b2ea6f0607a9658b9bda81c70983212aaff09c7'
CONFIG='translations/bridge_duties_editorial_release_v1.json'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['encoder']=='dialogue-relocatable-v1' and doc['consumer_layout_profile']=='deck-bridge-duties-visible-v1'
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
        assert row['current_text_hex']==before[n].text.hex() and row['native_argument_count']==0
        authored[n]=compiled(row)
    pack=FunctionType(repack.__code__,{**repack.__globals__,'previous_entries':previous_entries})
    before,blocks,first,last,selected,opaque,groups,attempts=pack(common,arm,authored)
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
    assert all(blocks[n]==rebuilt[n] for n in range(41) if not first<=n<=last)
    for n,payload in opaque.items():
        e=after[n];assert rebuilt[e.block][e.block_offset:e.copy_end]==payload
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==arm and cache_plan(a)==cache_plan(arm)
    old,new=MainCodeFile(arm,0x02000000),MainCodeFile(a,0x02000000)
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in old.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in new.sections]
    assert old.sections[3].data==new.sections[3].data and len(new.sections[3].data)-48==123040
    return c,a,{'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS if before[n].text!=after[n].text],
        'reviewed_native_IDs':list(IDS),'metadata_fields':fields,'directory_sha256':directory,
        'repacked_block_range':[first,last],'packing_attempts':attempts,'repacked_native_IDs':[e.message_id for e in selected],
        'repacked_block_lengths':[len(rebuilt[b]) for b in range(first,last+1)],
        'existing_single_cache_code_hex_preserved':SINGLE.hex(),
        'single8192_input_reuses_original_two4096_allocation':True,'output512_and216x36_crop_unchanged':True,
        'all3640_other_message_strings_exact':True,'opaque_payload_IDs':sorted(opaque),
        'all_opaque_payloads_and_unselected_blocks_exact':True,'all_other_ARM9_bytes_except_metadata_exact':True,
        'all_section_BSS_startup_cache_arena_and123040_staged_bounds_unchanged':True,
        'single_cache_may_increase_file_reads':True,'actual_RGB_gameplay_not_claimed_by_this_stage':True,
        'experimental':True,'full_goal_complete':False}


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-bridge-duties-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    for key in ('native_context_proof','native_font_proof','visual_review_proof','native_pronoun_terms_proof'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    assert len(context['all54_original_role_helper_selections'])==54
    assert {r['selected_message_ID'] for r in context['all54_original_role_helper_selections']}==set(IDS)
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==28
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes())
    assert visual['all28_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all28_source_numeric_selection_complete_ABI_words_and_visible_ink_pass']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['complete_ASCII_first_person1477_and_native_Xien1498_pass']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and compiled(row).hex()==case['text_hex']
        for gate in ('full252x96_native_and_independent_canvas_equal','independent_authored_words_at_x0_12px_rows_match_every_pixel',
                     'bitmap_and_input_guards_exact','all_body_ink_inside_registered216x36_crop'):assert case[gate]
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    terms=read(doc['native_pronoun_terms_proof']);assert len(terms['all25_current_and_clean_parser_control_cases'])==25
    assert terms['IC_is_first_person_not_actor_name'] and terms['native_actor10_given_name']=='Xien'
    audit=read(config['native_consumer_audit']);assert audit['batch_sha256']==sha(manuscript.read_bytes())
    assert audit['blocking_errors']==audit['unwaived_warnings']==0 and len(audit['records'])==28
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
