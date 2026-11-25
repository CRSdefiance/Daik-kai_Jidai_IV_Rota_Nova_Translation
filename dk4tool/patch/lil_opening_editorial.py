"""Runtime-bound, source-reviewed SC2 B22 editorial layer after frozen releases."""
import json
import struct
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH='/data/SC2.DK4'
CONFIG='translations/lil_opening_editorial_release_v1.json'
HEADER=b'\0\x40\xff\xff\0'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def apply_release(image,baseline,config_path=CONFIG):
    config=load(config_path)
    if config.get('format')!='dk4-lil-opening-editorial-release-v1':
        raise ValueError('Unknown Lil opening editorial release')
    for name,digest in config['dependencies'].items():
        if sha(Path(name).read_bytes())!=digest:
            raise ValueError('Lil opening reviewed dependency differs:'+name)
    arm=image.read_file('/__arm9__.bin');source=image.read_file(PATH)
    if sha(arm)!=config['required_runtime_arm9_sha256']:
        raise ValueError('Lil opening requires the proven native literal/cursor runtime')
    if sha(source)!=config['source_SC2_sha256'] or sha(baseline.read_file(PATH))!=config['canonical_SC2_sha256']:
        raise ValueError('Lil opening current/canonical source differs')
    clean_path=Path(config['clean_ROM'])
    if sha(clean_path.read_bytes())!=config['clean_ROM_sha256']:
        raise ValueError('Lil opening clean Japanese ROM differs')
    clean=NdsImage.open(clean_path).read_file(PATH)
    if sha(clean)!=config['clean_SC2_sha256']:
        raise ValueError('Lil opening clean script differs')
    doc=load(config['manuscript']);validate_natural_dialogue_batch(doc)
    if (doc['translation_policy']!='natural-dialogue-v2' or doc['target_locale']!='en-US'
        or doc['encoder']!='dialogue-relocatable-v1' or doc['dialogue_profile']!='lil-opening-editorial-native-v1'
        or doc['required_runtime_ARM9_sha256']!=sha(arm) or doc['formatting_review_pending']):
        raise ValueError('Lil opening source/native review contract differs')
    mapping=load(config['reference_map'])
    if (mapping.get('format')!='dk4-lil-opening-source-relocation-map-v1'
        or mapping.get('external_references_complete') is not True
        or mapping.get('entry_point_offset')!=8 or mapping.get('preserve_record_parity') is not True):
        raise ValueError('Lil opening complete source reference map required')
    font=load(doc['native_font_proof']);visual=load(doc['visual_review'])
    if not visual['all7_sheets_and49_panels_actually_viewed'] or len(font['cases'])!=49:
        raise ValueError('Lil opening complete native/visual approval required')
    refs={r['id']:r for r in mapping['records']};fonts={r['id']:r for r in font['cases']}
    if set(refs)!=set(fonts) or len(doc['records'])!=49:
        raise ValueError('Lil opening exhaustive49-record coverage differs')
    container=IlnkContainer.parse(source);block=container.blocks[22]
    original=IlnkContainer.parse(clean).blocks[22]
    if (sha(block)!=mapping['source_block_sha256'] or block[:4]!=b'CS\0\1'
        or len(block)!=8+struct.unpack_from('<H',block,4)[0]):
        raise ValueError('Lil opening source block/header differs')
    parts=block.split(b'\0');jp=original.split(b'\0');before=list(parts)
    profile=get_dialogue_profile(doc['dialogue_profile']);changes=[];seen=set()
    for row in doc['records']:
        ident=row['id'];ref=refs[ident];case=fonts[ident];index=row['record_index']
        if ident in seen or index!=ref['record_index']:
            raise ValueError('Lil opening record identity overlaps or differs')
        seen.add(ident)
        old=parts[index];raw=jp[index]
        at=sum(len(p)+1 for p in before[:index]);source_at=sum(len(p)+1 for p in jp[:index])
        if (old.hex()!=row['current_text_hex'] or raw.hex()!=row['source_hex']
            or at!=ref['old_offset'] or block[at-5:at]!=HEADER
            or original[source_at-5:source_at]!=HEADER or old[:1]!=raw[:1]):
            raise ValueError('Lil opening original/current text or speaker differs:'+ident)
        compiled=encode_relocatable_dialogue(raw,row['english'],profile)
        if compiled.encoded.hex()!=row['compiled_hex'] or compiled.encoded.hex()!=case['encoded_hex']:
            raise ValueError('Lil opening complete reviewed native text differs:'+ident)
        for diagnostic in compiled.diagnostics:
            if diagnostic.severity=='warning' and (diagnostic.code not in row.get('qa_waivers',[]) or not row.get('qa_waiver_reason')):
                raise ValueError('Lil opening unreviewed formatting warning:'+ident)
        value=compiled.encoded;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        if (value.hex()!=ref['target_hex'] or value[:1]!=old[:1] or b'\0' in value
            or len(value)%2!=len(old)%2):
            raise ValueError('Lil opening source speaker,parity or target bytes differ:'+ident)
        parts[index]=value
        changes.append({'id':ident,'file_path':PATH,'block':22,'record_index':index,
            'old_offset':at,'old_bytes':len(old),'new_bytes':len(value),'body_changed':value!=old,
            'parity_space_added':pad,'original_speaker_header_and_macro_contracts_preserved':True})
    if seen!=set(refs):
        raise ValueError('Lil opening missing reviewed record')
    logical=bytearray(b'\0'.join(parts))
    if len(logical)-8>0xFFFF:raise ValueError('Lil opening CS length exceeds original16-bit field')
    struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+b'\0'*(-len(logical)%4)
    if sha(target)!=mapping['target_block_sha256']:
        raise ValueError('Lil opening target block differs from complete reference proof')
    for row in changes:
        ref=refs[row['id']];index=row['record_index']
        at=sum(len(p)+1 for p in parts[:index]);row['new_offset']=at;row['offset_changed']=at!=row['old_offset']
        if at!=ref['new_offset'] or target[at-5:at]!=HEADER:
            raise ValueError('Lil opening relocated header/entry differs')
    container.blocks[22]=target;result=container.to_bytes()
    if sha(result)!=config['target_SC2_sha256']:
        raise ValueError('Lil opening complete target script differs')
    old_blocks=IlnkContainer.parse(source).blocks
    if [n for n,(a,b) in enumerate(zip(old_blocks,container.blocks,strict=True)) if a!=b]!=[22]:
        raise ValueError('Lil opening changes an unrelated script block')
    image.replace_file(PATH,result)
    if image.read_file('/__arm9__.bin')!=arm:
        raise ValueError('Lil opening changed native code')
    return {'source_SC2_sha256':sha(source),'target_SC2_sha256':sha(result),'required_runtime_ARM9_sha256':sha(arm),
        'manuscript':config['manuscript'],'changed_records':changes,'only_SC2_block22_changed':True,
        'all335_other_SC2_blocks_and_other_files_unchanged':True,'all49_original_source_controls_and_byte_parity_preserved':True,
        'reference_map':config['reference_map'],'native_90_command_and_external_entry_contract':True,
        'block_growth_bytes':len(target)-len(block),'native_code_and123040_staged_payload_unchanged':True}
