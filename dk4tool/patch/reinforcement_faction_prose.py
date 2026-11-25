"""Exact-allocation late COMMON prose after all frozen cumulative stages."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read

CONFIG='translations/reinforcement_faction_prose_release_v1.json'
PATH='/COMMON/MESFILE.DK4'
IDS=tuple(range(1911,1917))


def transform(common,arm,doc,directory):
    validate_natural_dialogue_batch(doc)
    if doc['translation_policy']!='natural-dialogue-v2'or doc['target_locale']!='en-US'or doc['formatting_review_pending']:
        raise ValueError('Reviewed natural-dialogue-v2 formatting required')
    old=entries(common,arm,directory);container=IlnkContainer.parse(common);original=list(container.blocks)
    rows={r['message_id']:r for r in doc['records']}
    if sorted(rows)!=list(range(1911,1931)):raise ValueError('All20 source-reviewed announcement rows required')
    changes=[]
    for n in IDS:
        row=rows[n];entry=old[n];before=entry.text;after=compiled(row)
        if before.hex()!=row['current_text_hex']or not all(row['review'].values()):
            raise ValueError('Exact current paragraph and per-record review required')
        if len(after)>len(before)or not after.startswith(b' ')or b'\n'in after or b'\0'in after:
            raise ValueError('Whole native paragraph must fit existing allocation')
        block=bytearray(container.blocks[entry.block]);at=entry.block_offset
        if block[at:at+len(before)]!=before or block[at+len(before)]!=0:
            raise ValueError('Exact native text span and original terminator required')
        replacement=after+bytes(len(before)-len(after));block[at:at+len(before)]=replacement
        container.blocks[entry.block]=bytes(block)
        changes.append({'id':row['id'],'message_ID':n,'block':entry.block,'block_offset':at,
            'copy_end':entry.copy_end,'original_allocation_bytes':len(before),'new_paragraph_bytes':len(after),
            'internal_unused_bytes_zeroed_after_new_terminator':len(before)-len(after),
            'before_hex':before.hex(),'after_hex':after.hex(),'replacement_hex':replacement.hex()})
    target=container.to_bytes();new=entries(target,arm,directory)
    for a,b in zip(old,new,strict=True):
        if(a.message_id,a.block,a.table_offset,a.block_offset,a.copy_end)!=(b.message_id,b.block,b.table_offset,b.block_offset,b.copy_end):
            raise ValueError('Native offset or copy span changed')
        if b.text!=(compiled(rows[a.message_id])if a.message_id in IDS else a.text):raise ValueError('Unselected text changed')
    for n,(a,b)in enumerate(zip(original,container.blocks,strict=True)):
        owned={j for c in changes if c['block']==n for j in range(c['block_offset'],c['block_offset']+c['original_allocation_bytes'])}
        if len(a)!=len(b)or any(x!=y and j not in owned for j,(x,y)in enumerate(zip(a,b,strict=True))):
            raise ValueError('Unowned native block bytes changed')
    return target,{'manuscript':doc.get('release_manuscript_path','translations/reinforcement_sniping_editorial_manuscript_v4.json'),
        'changed_records':changes,'all3668_native_offsets_and_copy_spans_exact':True,
        'all3662_unselected_strings_and_all_unowned_block_bytes_exact':True,
        'all41_decompressed_block_lengths_and_original_final_terminators_exact':True,
        'no_authored_line_breaks_alignment_spaces_or_native_metadata_changes':True,
        'no_runtime_font_graphic_story_macro_or_RNG_changes':True}


def apply_release(image,baseline,config_path=CONFIG):
    config=read(config_path)
    if config['format']!='dk4-reinforcement-faction-prose-v1':raise ValueError('Unknown faction prose release')
    for name,digest in config['dependencies'].items():
        if sha(Path(name).read_bytes())!=digest:raise ValueError('Faction prose dependency differs:'+name)
    common,arm=image.read_file(PATH),image.read_file('/__arm9__.bin')
    if sha(common)!=config['source_COMMON_sha256']or sha(arm)!=config['required_ARM9_sha256']:
        raise ValueError('Exact inherited COMMON and runtime required')
    if sha(baseline.read_file(PATH))!=config['canonical_COMMON_sha256']:raise ValueError('Exact canonical COMMON required')
    doc=read(config['manuscript']);clean=NdsImage.open(config['clean_ROM'])
    if sha(Path(config['clean_ROM']).read_bytes())!=config['clean_ROM_sha256']:raise ValueError('Exact clean Japanese ROM required')
    source=common_message_entries(clean.read_file(PATH),clean.read_file('/__arm9__.bin'))
    for row in doc['records']:
        if row['source_hex']!=source[row['message_id']].text.hex():raise ValueError('Japanese source differs')
    target,proof=transform(common,arm,doc,config['directory_sha256'])
    if sha(target)!=config['target_COMMON_sha256']:raise ValueError('Faction prose target COMMON differs')
    image.replace_file(PATH,target)
    return proof
