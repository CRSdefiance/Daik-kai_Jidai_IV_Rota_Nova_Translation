"""Independent Cook15 editorial successor; completed work-comment layers stay frozen."""

import struct
from pathlib import Path
from types import FunctionType,SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.work_comments_editorial import current_entries as previous_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.work_comments_layout_v843 import compiled
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(1410,1423))
SOURCE_COMMON='2b0d8dda1e4dd01dc606cc2c9f4cbff9ffcfcea8b5ddc4c055128231da3db849'
SOURCE_ARM='75d78d530b3b57fa2cc83f27509c31a1fd3b146f2a879d95d16826a3305965d1'
CONFIG='translations/cooking_comments_editorial_release_v1.json'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['encoder']=='dialogue-relocatable-v1' and doc['consumer_layout_profile']=='deck-cooking-comments-visible-v1'
    assert tuple(r['message_id'] for r in doc['records'])==IDS
    assert doc['current_COMMON_sha256']==SOURCE_COMMON and doc['current_ARM9_sha256']==SOURCE_ARM
    clean,canonical=map(NdsImage.open,('work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']
    jp=parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    accepted=parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    before=previous_entries(common,arm);authored={}
    for row in doc['records']:
        n=row['message_id']
        assert row['source_hex']==jp[n].text.hex() and row['canonical_source_hex']==accepted[n].text.hex()
        assert row['current_text_hex']==before[n].text.hex() and row['native_argument_count']==0
        authored[n]=compiled(row)
    scoped=SimpleNamespace(common_message_entries=lambda c,a,clean=False:previous_entries(c,a))
    pack=FunctionType(repack.__code__,{**repack.__globals__,'parser':scoped})
    before,blocks,first,last,selected,opaque,groups,attempts=pack(common,arm,authored)
    target,rebuilt,fields=bytearray(arm),list(blocks),[]
    for block,(group,body) in zip(range(first,last+1),groups,strict=True):
        rebuilt[block]=body;at=parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target,at,group[0][0],len(body));fields.append((at,4))
        for n,offset,payload in group:
            at=parser.TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,offset);fields.append((at,2))
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target)
    directory=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET]);after=local_entries(directory)(c,a,clean=False)
    assert len(before)==len(after)==3668
    assert all(b.text==authored.get(e.message_id,e.text) for e,b in zip(before,after,strict=True))
    assert all(blocks[n]==rebuilt[n] for n in range(41) if not first<=n<=last)
    for n,payload in opaque.items():
        e=after[n];assert rebuilt[e.block][e.block_offset:e.copy_end]==payload
    assert all(before[n].text==after[n].text for n in (64,292,346,347,348,676,677,*range(1361,1410)))
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==arm and cache_plan(a)==cache_plan(arm)
    old,new=MainCodeFile(arm,0x02000000),MainCodeFile(a,0x02000000)
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in old.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in new.sections]
    assert old.sections[3].data==new.sections[3].data and len(new.sections[3].data)-48==123040
    return c,a,{'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS if before[n].text!=after[n].text],
        'reviewed_native_IDs':list(IDS),'metadata_fields':fields,'directory_sha256':directory,
        'repacked_block_range':[first,last],'packing_attempts':attempts,'repacked_native_IDs':[e.message_id for e in selected],
        'all3655_other_message_strings_exact':True,'opaque_payload_IDs':sorted(opaque),
        'all_opaque_payloads_and_unselected_blocks_exact':True,'existing216x36_crop_and_all_native_code_preserved':True,
        'all_other_ARM9_bytes_except_native_metadata_exact':True,'all_section_BSS_cache_and123040_staged_bounds_unchanged':True,
        'actual_RGB_gameplay_not_claimed_by_this_stage':True,'experimental':True,'full_goal_complete':False}


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return local_entries(config['directory_sha256'])(common,arm,clean=False)


def apply_release(common,arm,path):
    config=read(path)
    assert config['format']=='dk4-cooking-comments-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    context=Path(doc['native_context_proof']);assert sha(context.read_bytes())==doc['native_context_proof_sha256']
    assert len(read(context)['all25_original_role_helper_selections'])==25 and read(context)['special_Sera_actor24_ID']==1422
    font_path=Path(doc['native_font_proof']);assert sha(font_path.read_bytes())==doc['native_font_proof_sha256']
    fonts=read(font_path);visual=Path(doc['visual_review_proof'])
    assert sha(visual.read_bytes())==doc['visual_review_proof_sha256'];review=read(visual)
    assert review['native_font_proof_sha256']==sha(font_path.read_bytes())
    assert review['all13_previews_visually_reviewed'] and not review['visual_review_pending']
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and fonts['all13_source_numeric_selection_complete_ABI_words_and_visible_ink_pass']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and len(fonts['cases'])==13
    assert fonts['cases'][-1]['actor_ID']==24 and fonts['cases'][-1]['message_id']==1422
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and compiled(row).hex()==case['text_hex']
        assert case['full252x96_native_and_independent_canvas_equal'] and case['independent_authored_words_at_x0_12px_rows_match_every_pixel']
        assert case['bitmap_and_input_guards_exact'] and case['all_body_ink_inside_registered216x36_crop']
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof']);assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert len(copies['all3668_native_IDs_warm_and_cold7336_complete_copies'])==3668
    return c,a,proof
