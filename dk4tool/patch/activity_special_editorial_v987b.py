"""Complete17 activity,Chapel-refusal and special-character comments within the preserved proven single8KiB cache."""



import struct

from types import FunctionType

from pathlib import Path



from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch

from dk4tool.formats.ilnk import IlnkContainer

from dk4tool.patch.common_single_cache_v861 import SINGLE, entries, repack

from dk4tool.patch.grand_race_menu_release import sha

from dk4tool.patch.mood_comments_editorial_v981b import current_entries as previous_entries

from dk4tool.patch.main_pool_cache_visibility import cache_plan

from dk4tool.rom.nds import NdsImage

from dk4tool.script import common_message_table as parser

from scripts.activity_special_layout_v986b import compiled

from scripts.verify_village_wrap_v608 import read



IDS=tuple(range(1872,1889))

SOURCE_COMMON='eb50d15cdc33306b2c321795719e7f03a58a4867fedafcaa59b1695d0fa8258d'

SOURCE_ARM='a446afb0ea754456351b9257b34edc8526d9c437bd2af7fe0f9cb2fe3e0ddadb'

CONFIG='translations/activity_special_editorial_release_v1.json'





def plan(common,arm,doc):

    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM

    validate_natural_dialogue_batch(doc)

    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'

    assert doc['encoder']=='dialogue-relocatable-v1' and doc['consumer_layout_profile']=='activity-special-mixed-consumers-v1'

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

        assert row['source_native_macros']==[]

        assert row['actor_ID'] in (6,11,12,14,15,17,20,22,25,26,27) and row['consumer'] in ('Deck-CabinInfoView','assignment-refusal-modal')

        authored[n]=compiled(row)

    # Reviewed retained strings need no replacement. Keep their complete original
    # copy spans, including nontext bytes after the owned NUL.
    authored={n:payload for n,payload in authored.items() if payload!=before[n].text}
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

        'all3651_other_message_strings_exact':True,'opaque_payload_IDs':sorted(opaque),

        'all_opaque_payloads_and_unselected_blocks_exact':True,'all_other_ARM9_bytes_except_metadata_exact':True,

        'all_section_BSS_startup_cache_arena_and123040_staged_bounds_unchanged':True,

        'single_cache_may_increase_file_reads':True,'actual_RGB_gameplay_not_claimed_by_this_stage':True,

        'experimental':True,'full_goal_complete':False}





def current_entries(common,arm):

    config=read(CONFIG)

    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']

    return entries(common,arm,config['directory_sha256'])





def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-activity-special-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    for key in ('native_context_proof','native_font_proof','visual_review_proof','source_context_supplement'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    assert context['candidate_sha256']==doc['current_ROM_sha256']
    assert len(context['all52_activity2_direct_and_main_priority_cases'])==52
    assert len(context['all16_special_ordinary_battle_direct_and_main_bit2_controls'])==16
    assert len(context['all12_original_actor_role_legality_controls'])==12
    refusals=context['all3_original_Chapel_assignment_refusal_owner_and_speaker_calls'];assert len(refusals)==3
    for r in refusals:
        assert r['all28_actor_records_and31_room_occupants_preserved_no_assignment_performed'] and r['original_ABI_and_stack_pass']
        assert r['requested_role']==18 and r['dialogue_dispatcher']==0x02053FE4
    assert {(r['actor_ID'],r['original_legality_and_actor_specific_refusal_calls'][0]['message_ID']) for r in refusals}=={(17,1878),(25,1879),(12,1880)}
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==17
    assert fonts['complete_Deck_native_font_cases']==20 and fonts['complete_modal_native_font_cases']==3
    assert fonts['all17_complete_words_leading_trailing_letters_and_native_bounds_pass']
    assert fonts['modal3_use_existing_native_balanced_formatter_as_offline_compiler_no_runtime_code_or_membership_changes']
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes()) and visual['all17_previews_visually_reviewed'] and not visual['visual_review_pending']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        n=row['message_id'];assert n==case['message_id'] and row['actor_ID']==case['actor_ID']==context['actor_by_message_ID'][str(n)]
        assert compiled(row).hex()==case['compiled_hex'] and case['consumer']==row['consumer']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        if case['consumer']=='Deck-CabinInfoView':
            assert case['complete_words_and216x36_body_bounds_pass']
            assert len(case['native_controls'])==(2 if n<1878 else 1)
            for v in case['native_controls']:
                assert v['text_hex']==case['compiled_hex'] and v['original_numeric_selector_selected_expected_message']
                for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal','independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact'):
                    assert v[gate]
        else:
            assert n in (1878,1879,1880) and case['original_54014_COMMON_dispatch_keeps_compiled_bytes_exact']
            assert case['whole228x64_native_and_independent_font_canvas_equal'] and case['all_leading_trailing_glyphs_and_uniform_visible_left_margin_pass']
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    supplement=read(doc['source_context_supplement'])
    assert supplement['candidate_sha256']==doc['current_ROM_sha256'] and supplement['all17_source_IC_and_printf_counts_zero']
    assert supplement['Yifa1879_personal_training_not_universal_Taoist_ban'] and supplement['Al1878_Arab_pride_without_invented_religion']
    assert supplement['Yukihisa1880_explicit_Christian_refusal_with_formal_voice'] and supplement['Aziza1884_1888_addressee_identity_gender_kinship_and_bit2_meaning_not_invented']
    assert supplement['activity2_after_original_event_no_invented_Scold_button']
    for name,digest in supplement['established_term_documents'].items():assert sha(Path(name).read_bytes())==digest
    audit=read(config['native_consumer_audit']);assert audit['batch_sha256']==sha(manuscript.read_bytes())
    assert audit['blocking_errors']==audit['unwaived_warnings']==0 and len(audit['records'])==17
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
