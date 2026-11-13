"""COMMON730 full category arguments with every menu label preserved."""

from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.category_dialogue_lookup import transform as category_lookup
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.verify_village_wrap_v608 import read


def compile_template(english):
    text=english.removesuffix('{PAD}')
    if (not text or not text.isascii() or text!=' '.join(text.split()) or any(c in text for c in '{}')
            or text.count('%s')!=1 or '%' in text.replace('%s','')
            or any(s in text for s in ('FI','FA','FO','FU','IC'))):
        raise ValueError('One safe paragraph with the exact source category substitution is required')
    return b' '+text.encode('ascii')


def transform(common,arm,manuscript):
    assert manuscript['translation_policy']=='natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert [r['message_id'] for r in manuscript['records']]==[730]
    row=manuscript['records'][0];path='/COMMON/MESFILE.DK4'
    clean=NdsImage.open('work/clean.nds');canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(clean.read_file(path))==manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path))==manuscript['source_canonical_COMMON_sha256']
    source=common_message_entries(clean.read_file(path),clean.read_file('/__arm9__.bin'))[730]
    accepted=common_message_entries(canonical.read_file(path),canonical.read_file('/__arm9__.bin'),clean=False)[730]
    before=common_message_entries(common,arm,clean=False)
    assert source.text==bytes.fromhex(row['source_hex']) and source.text.count(b'%s')==1
    assert accepted.text==bytes.fromhex(row['canonical_source_hex']) and before[730].text==bytes.fromhex(row['current_text_hex'])
    entry=before[730];owner=entry.block,entry.record_index
    blocks=IlnkContainer.parse(common).blocks
    prefix=blocks[owner[0]].split(b'\0')[owner[1]][:entry.start]
    template=compile_template(row['english'])
    result=repack_native_records(common,arm,{730:template},{owner:prefix},generated_linebreaks=True,spare_padding_before_first_entry=True)
    target_arm,lookup=category_lookup(result.arm9)
    after=common_message_entries(result.common,target_arm,clean=False)
    for a,b in zip(before,after,strict=True):
        assert (a.message_id,a.block,a.record_index)==(b.message_id,b.block,b.record_index)
        assert b.text==(template if a.message_id==730 else a.text)
    assert all(a==b for i,(a,b) in enumerate(zip(blocks,IlnkContainer.parse(result.common).blocks,strict=True)) if i!=entry.block)
    return result.common,target_arm,{'changed_records':['COMMON_MESSAGE_730'],
        'changed_native_offset_fields':sorted(result.changed_offsets),'lookup':lookup,
        'all3667_unselected_message_texts_and40_other_blocks_exact':True,'source730_native_parent_and_caller_unchanged':True,
        'experimental':True,'full_goal_complete':False}


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-category-dialogue-editorial-v1'
    assert sha(common)==config['source_common_sha256'] and sha(arm)==config['source_arm9_sha256']
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    for filename,digest in config['dependencies'].items():assert sha(Path(filename).read_bytes())==digest
    common,arm,proof=transform(common,arm,read(manuscript))
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return common,arm,proof
