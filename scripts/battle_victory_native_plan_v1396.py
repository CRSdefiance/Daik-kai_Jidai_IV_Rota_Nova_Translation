"""Eight reviewed short victory paragraphs;no runtime or selector changes."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.flagship_capture_precision import current_entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_payload_v1396')
MANUSCRIPT = Path('translations/battle_victory_editorial_manuscript_v1.json')
IDS = tuple(range(2130,2138))
PROFILE = 'battle-victory-portrait-postmacro-v1'
SOURCE_COMMON = '099be4645bb10fa27690dc9452cdf827e7b1168342baff09ad5edbd76238444c'
SOURCE_ARM = '42c074273755aa0157a6d508da8792065a5e4638c979164a49565666fc2eb04b'


def compiled(row):
    number,text = row['message_id'],row['english']
    if number not in IDS or not text or not text.isascii() or text!=' '.join(text.split()):
        raise ValueError('One natural unwrapped ASCII paragraph without alignment is required')
    if any(ord(c)<32 or ord(c)>126 or c in '{}%' for c in text):
        raise ValueError('No authored controls,layout markup or invented printf argument')
    if row['native_argument_count']!=0:
        raise ValueError('The original victory consumer has no substitution arguments')
    macros = row['source_native_macros']
    expected = ['IC first-person plus plural tachi localized grammatically as we'] if number==2132 else []
    if macros!=expected:
        raise ValueError('Preserve the explicitly reviewed source first-person-plural interpretation')
    if len(text)>35:
        raise ValueError('Longer prose requires a separately reviewed native layout;never truncate it')
    # The unchanged original nonmember formatter supplies its own leading cell.
    # No translator/compiler alignment byte is added to this legacy selector.
    return text.encode('ascii')


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['consumer_layout_profile']==PROFILE and tuple(r['message_id'] for r in doc['records'])==IDS
    clean,canonical = NdsImage.open('work/clean.nds'),NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    before = current_entries(common,arm)
    source = IlnkContainer.parse(common)
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert row['source_hex']==jp[n].text.hex() and row['canonical_source_hex']==base[n].text.hex()
        assert row['current_text_hex']==before[n].text.hex()
        assert all(row['review'][g] for g in ['source','context','localization','naturalness'])
        authored[n] = compiled(row)
    assert {before[n].block for n in IDS}=={23}
    changed = [n for n in IDS if authored[n]!=before[n].text]
    assert changed==[2136,2137]
    target,rebuilt = bytearray(arm),list(source.blocks)
    numbers = [r.message_id for r in before if r.block==23]
    assert numbers==list(range(numbers[0],numbers[-1]+1))
    body,fields,patches = bytearray(),[],[]
    def put(at,value):
        target[at:at+len(value)] = value
        fields.append([at,len(value)])
        patches.append({'address':0x02000000+at,'source_hex':arm[at:at+len(value)].hex(),'target_hex':value.hex()})
    for n in numbers:
        row = before[n]
        payload = source.blocks[23][row.block_offset:row.copy_end]
        assert 0<len(payload)<512 and payload.startswith(row.text+b'\0')
        if n in changed:
            assert not set(payload[len(row.text)+1:])-{0,32}
            payload = authored[n]+b'\0'
        put(TABLE_OFFSET+n*2,struct.pack('<H',len(body)))
        body.extend(payload)
    assert 0<len(body)<=8192
    rebuilt[23] = bytes(body)
    put(DIRECTORY_OFFSET+23*4,struct.pack('<HH',numbers[0],len(body)))
    a,c = bytes(target),IlnkContainer(rebuilt).to_bytes()
    directory = sha(a[DIRECTORY_OFFSET:TABLE_OFFSET])
    after = owned_entries(c,a,directory)
    assert len(before)==len(after)==3668
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    assert all(rebuilt[b]==source.blocks[b] for b in range(41) if b!=23)
    for n in numbers:
        if n not in changed:
            old,new = before[n],after[n]
            assert source.blocks[23][old.block_offset:old.copy_end]==rebuilt[23][new.block_offset:new.copy_end]
    restored = bytearray(a)
    for p in patches:
        at = p['address']-0x02000000
        restored[at:at+len(bytes.fromhex(p['source_hex']))] = bytes.fromhex(p['source_hex'])
    assert bytes(restored)==arm
    old,new = [MainCodeFile(v,0x02000000) for v in [arm,a]]
    shape = lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(a)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    return c,a,{'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(arm),
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'directory_sha256':directory,
        'changed_records':[f'COMMON_MESSAGE_{n}' for n in changed],'native_IDs':list(IDS),
        'actual_changed_message_IDs':changed,'metadata_fields':fields,'patches':patches,
        'runtime_plan':{'patches':[],'entire_existing_runtime_and_selector_bank_preserved':True},
        'all3666_unselected_or_retained_texts_and_native_copy_spans_preserved':True,
        'all40_other_blocks_and_opaque_duel_prefix_exact':True,
        'only_COMMON23_and_original_native_offset_directory_data_changed':True,
        'entire188_byte_selector_172_byte_gate_and_all_code_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact':True,
        'old_new_block23_bytes':[len(source.blocks[23]),len(body)],'all_ARM9_patches_restore_source_exact':True,
        'original_legacy_leading_cell_kept_no_new_formatter_membership':True}


if __name__=='__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    c,a,proof = plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c)
    ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Victory payload:only2136/2137 prose changes;all3666 other texts/copies and entire runtime/selector/123040 staged bytes preserved.',flush=True)
