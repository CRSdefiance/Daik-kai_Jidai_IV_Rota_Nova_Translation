"""Source/runtime-bound B24 prose compiler after the frozen integrated stack."""
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
CONFIG='translations/lil_trade_routes_editorial_release_v1.json'
HEADER=bytes.fromhex('0040ffff00')

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def apply_release(image,baseline,config_path=CONFIG):
    config=load(config_path)
    if config.get('format')!='dk4-lil-trade-routes-editorial-release-v1':
        raise ValueError('Unknown Lil trade-routes release')
    for name,digest in config['dependencies'].items():
        if sha(Path(name).read_bytes())!=digest:raise ValueError('B24 reviewed dependency differs:'+name)
    arm=image.read_file('/__arm9__.bin');source=image.read_file(PATH)
    if sha(arm)!=config['required_runtime_arm9_sha256']:raise ValueError('B24 proven runtime differs')
    if sha(source)!=config['source_SC2_sha256']or sha(baseline.read_file(PATH))!=config['canonical_SC2_sha256']:
        raise ValueError('B24 current/canonical source differs')
    clean_path=Path(config['clean_ROM'])
    if sha(clean_path.read_bytes())!=config['clean_ROM_sha256']:raise ValueError('B24 clean ROM differs')
    clean=NdsImage.open(clean_path).read_file(PATH)
    if sha(clean)!=config['clean_SC2_sha256']:raise ValueError('B24 clean SC2 differs')
    doc=load(config['manuscript']);validate_natural_dialogue_batch(doc)
    if (doc['translation_policy']!='natural-dialogue-v2'or doc['target_locale']!='en-US'
        or doc['encoder']!='dialogue-relocatable-v1'or doc['dialogue_profile']!='lil-opening-editorial-native-v1'
        or doc['required_runtime_ARM9_sha256']!=sha(arm)or doc['formatting_review_pending']):
        raise ValueError('B24 source/native review contract differs')
    mapping=load(config['reference_map'])
    if (mapping.get('format')!='dk4-lil-trade-routes-source-relocation-map-v1'
        or mapping.get('external_references_complete')is not True or mapping.get('entry_point_offset')!=8
        or mapping.get('preserve_record_parity')is not True
        or mapping.get('all17_original_commands_all13_actual_speeches_and_normal_return_verified')is not True):
        raise ValueError('B24 complete source reference map required')
    if not load(doc['actual_visual_review'])['both_actual_sheets_all13_panels_and_normal_Amsterdam_return_actually_viewed']:
        raise ValueError('B24 actual visual approval required')
    refs={r['id']:r for r in mapping['records']};fonts={r['id']:r for r in load(doc['native_font_proof'])['cases']}
    if len(doc['records'])!=13 or len(refs)!=13 or set(refs)!=set(fonts):raise ValueError('B24 exhaustive13-record coverage differs')
    container=IlnkContainer.parse(source);block=container.blocks[24];japanese=IlnkContainer.parse(clean).blocks[24]
    if sha(block)!=mapping['source_block_sha256']or block[:4]!=b'CS\0\1':raise ValueError('B24 source block differs')
    end=8+struct.unpack_from('<H',block,4)[0]
    if end>len(block)or len(block)-end>3 or any(block[end:]):raise ValueError('B24 source CS extent differs')
    profile=get_dialogue_profile(doc['dialogue_profile']);patches=[];seen=set();changes=[]
    for row in doc['records']:
        ident=row['id'];ref=refs[ident];case=fonts[ident]
        if ident in seen:raise ValueError('B24 duplicate record')
        seen.add(ident);at=ref['old_offset'];old=bytes.fromhex(row['current_text_hex']);raw=bytes.fromhex(row['source_hex'])
        ja=row['source_reference']['offset']
        if (block[at:at+len(old)]!=old or block[at+len(old)]!=0
            or block[at-5:at]!=HEADER or japanese[ja-5:ja]!=HEADER
            or japanese[ja:ja+len(raw)]!=raw or japanese[ja+len(raw)]!=0
            or block[:at].count(b'\0')!=row['current_reference']['record_index']
            or japanese[:ja].count(b'\0')!=row['record_index']or raw[:1]!=old[:1]):
            raise ValueError('B24 exact current/source text or speaker differs:'+ident)
        compiled=encode_relocatable_dialogue(raw,row['english'],profile)
        if compiled.encoded.hex()!=row['compiled_hex']or compiled.encoded.hex()!=case['encoded_hex']:
            raise ValueError('B24 complete reviewed native text differs:'+ident)
        for diagnostic in compiled.diagnostics:
            if diagnostic.severity=='error':raise ValueError('B24 formatting error:'+ident)
            if diagnostic.severity=='warning'and(diagnostic.code not in row.get('qa_waivers',[])or not row.get('qa_waiver_reason')):
                raise ValueError('B24 unreviewed formatting warning:'+ident)
        value=compiled.encoded;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        if (value.hex()!=ref['encoded_hex']or value[:1]!=old[:1]or b'\0'in value
            or len(value)%2!=len(old)%2 or len(old)!=ref['old_bytes']):
            raise ValueError('B24 source speaker/parity or mapped text differs:'+ident)
        patches.append({'start':at,'end':at+len(old),'value':value,'old':old,'id':ident})
        changes.append({'id':ident,'file_path':PATH,'block':24,'record_index':row['record_index'],
            'old_offset':at,'new_offset':ref['new_offset'],'old_bytes':len(old),'new_bytes':len(value),
            'body_changed':old!=value,'parity_space_added':pad,'original_complete_header_and_macro_contracts_preserved':True})
    if seen!=set(refs):raise ValueError('B24 missing record')
    patches.sort(key=lambda r:r['start'])
    if any(a['end']>b['start']for a,b in zip(patches,patches[1:])):raise ValueError('B24 patches overlap')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            if p['start']<offset<p['end']:raise ValueError('B24 unclassified interior target')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    parts=[];last=0
    for p in patches:
        if mapped(p['start'])!=refs[p['id']]['new_offset']:raise ValueError('B24 mapped speech destination differs')
        parts.extend((block[last:p['start']],p['value']));last=p['end']
    parts.append(block[last:end]);logical=bytearray(b''.join(parts))
    if len(logical)!=mapped(end)or len(logical)-8>0xFFFF:raise ValueError('B24 resized CS extent differs')
    struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4)
    if len(target)>0x2400 or sha(target)!=mapping['target_block_sha256']:raise ValueError('B24 target block differs')
    if len(mapping['commands'])!=17:raise ValueError('B24 command map incomplete')
    for command in mapping['commands']:
        old=command['old_offset'];new=mapped(old);extent=command['old_extent']
        if new!=command['new_offset']or mapped(old+extent)-new!=command['new_extent']:
            raise ValueError('B24 mapped command destination differs')
        size=6 if command['word']==0x4000 else extent
        if block[old:old+size]!=target[new:new+size]:raise ValueError('B24 original command/header changed')
    inverse=bytearray(logical)
    for p in reversed(patches):inverse[mapped(p['start']):mapped(p['end'])]=p['old']
    struct.pack_into('<H',inverse,4,end-8)
    if bytes(inverse)!=block[:end]:raise ValueError('B24 inverse reconstruction differs')
    container.blocks[24]=target;result=container.to_bytes()
    if sha(result)!=config['target_SC2_sha256']:raise ValueError('B24 complete target SC2 differs')
    if [n for n,(a,b)in enumerate(zip(IlnkContainer.parse(source).blocks,container.blocks,strict=True))if a!=b]!=[24]:
        raise ValueError('B24 changed unrelated block')
    # Mutation happens only after every source,QA,reference andtarget guard passes.
    image.replace_file(PATH,result)
    return {'source_SC2_sha256':sha(source),'target_SC2_sha256':sha(result),'required_runtime_ARM9_sha256':sha(arm),
        'manuscript':config['manuscript'],'reference_map':config['reference_map'],'changed_records':changes,
        'only_SC2_block24_changed':True,'all335_other_blocks_preserved':True,
        'all13_original_six_byte_preambles_macros_and_parity_preserved':True,
        'all17_mapped_commands_and_inverse_reconstruction_verified':True,'block_growth_bytes':len(target)-len(block),
        'native_code_fonts_graphics_and123040_staged_payload_unchanged':True}
