"""Complete Palace menu strings in source-owned C-string allocations."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
SOURCE='e3074ecfb6196ddea857f92850720625d4c16da05d046a3899166d2bfa00a323'
ROOT=Path('work/analysis/palace_label_boundaries_v799')
TABLE=0x02118D24
OLD=(0x02143DF4,0x02143E04,0x02143E1C,0x02143E2C,0x02143E3C,0x02143E5C)
LABELS=('Contract','Military Investment','Recommendation','Introduction','Lend Item','Reclaim')
JAPANESE=('契約','軍事投資','推薦状を使う','紹介状を使う','アイテムを貸す','アイテムを引き取る')
SPANS=((0x02143DF4,0x02143DFC),(0x02143E1C,0x02143E4C),(0x02143E5C,0x02143E70))


def blobs():
    names={};group=bytearray()
    for label in ('Contract','Recommendation','Introduction','Lend Item'):
        names[label]=0x02143E1C+len(group);group.extend(label.encode()+b'\0')
    assert len(group)==47
    group.extend(b'\0')
    names['Military Investment']=0x02143E5C;names['Reclaim']=0x02143DF4
    return names,{0x02143DF4:b'Reclaim\0',0x02143E1C:bytes(group),
                  0x02143E5C:b'Military Investment\0'}


def verify_final(arm):
    names,_=blobs()
    for i,label in enumerate(LABELS):
        pointer=struct.unpack_from('<I',arm,TABLE-BASE+16*i)[0]
        assert pointer==names[label]
        raw=label.encode()+b'\0'
        assert any(lo<=pointer and pointer+len(raw)<=hi for lo,hi in SPANS)
        assert arm[pointer-BASE:pointer-BASE+len(raw)]==raw
    # The leading zero word of the following vtable is not spare text.
    assert arm[0x143E4C:0x143E50]==bytes(4)
    return {'all_six_complete_labels_NUL_terminated_inside_owned_strings':True,
        'original_menu_records_and_source_string_allocations':list(SPANS),
        'following_vtable_offset_word_preserved':True}


def plan(arm):
    assert sha(arm)==SOURCE
    names,patches=blobs();target=bytearray(arm)
    assert tuple(struct.unpack_from('<I',arm,TABLE-BASE+i*16)[0] for i in range(6))==OLD
    for at,data in patches.items():target[at-BASE:at-BASE+len(data)]=data
    for i,label in enumerate(LABELS):struct.pack_into('<I',target,TABLE-BASE+16*i,names[label])
    target=bytes(target);verify_final(target)
    original,target_code=[MainCodeFile(a,BASE) for a in (arm,target)]
    shape=lambda c:[(s.ramAddress,len(s.data),s.bssSize) for s in c.sections]
    assert shape(original)==shape(target_code) and bytes(original.sections[3].data)==bytes(target_code.sections[3].data)
    assert cache_plan(arm)==cache_plan(target) and len(target_code.sections[3].data)-48==123040
    restored=bytearray(target)
    for lo,hi in SPANS:restored[lo-BASE:hi-BASE]=arm[lo-BASE:hi-BASE]
    for i in range(6):
        at=TABLE-BASE+16*i;restored[at:at+4]=arm[at:at+4]
    assert bytes(restored)==arm
    return target,{'changed_records':['PALACE_MENU_'+str(i) for i in range(6)],
        'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'exact_source_owned_text_spans':list(SPANS),'only_six_existing_pointer_words_rebound':True,
        'all_other_bytes_sections_BSS_cache_and_staged123040_bytes_exact':True,
        'actual_revised_menu_playback_pending':True,'full_goal_complete':False}


def apply_release(arm,path):
    cfg=read(path);assert cfg['format']=='dk4-palace-label-boundaries-v1'
    assert cfg['source_arm9_sha256']==sha(arm)==SOURCE
    for p,h in cfg['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    doc=read(cfg['manuscript']);assert sha(Path(cfg['manuscript']).read_bytes())==cfg['manuscript_sha256']
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert tuple(r['english'] for r in doc['records'])==LABELS
    assert all(all(r['review'][g] for g in ('source','context','localization','naturalness','formatting')) for r in doc['records'])
    native=read(ROOT/'native_verification.json')
    assert native['all_six_original_strlen_and_full_copy_guards_and_ABI_pass'] and native['original_menu_initializer_copies_full96_bytes_exact']
    assert read(ROOT/'visual_review.json')['all_six_full_font_planes_reviewed']
    target,proof=plan(arm);assert sha(target)==cfg['target_arm9_sha256']==native['target_ARM9_sha256']
    return target,proof


def current_entries(common,arm):
    from scripts.prepare_recruitment_common_v772 import local_entries
    cfg=read('translations/palace_label_boundaries_release_v1.json')
    assert sha(common)==cfg['source_common_sha256'] and sha(arm)==cfg['target_arm9_sha256']
    previous=read('translations/palace_editorial_release_v1.json')
    return local_entries(previous['directory_sha256'])(common,arm,clean=False)
