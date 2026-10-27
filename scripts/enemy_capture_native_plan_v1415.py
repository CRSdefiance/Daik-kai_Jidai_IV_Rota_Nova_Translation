"""Repack only three reviewed capture messages in COMMON22;retain all runtime."""
import inspect
from pathlib import Path
from dk4tool.patch.battle_victory_editorial import current_entries
from scripts import battle_victory_native_plan_v1396 as previous
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/enemy_capture_payload_v1415')
MANUSCRIPT = Path('translations/enemy_capture_editorial_manuscript_v1.json')
IDS = tuple(range(2082,2090))
PROFILE = 'enemy-capture-direct-portrait-postmacro-v1'
SOURCE_COMMON = 'a54229478e6f5ede8f589891f381e914aaa8ddc5eaadbd5057e91c111b4fbc08'
SOURCE_ARM = 'e804968623fea7cd645fa78d34d53517374c6ff8df9a421ff40515fa7991bdd3'

def compiled(row):
    text = row['english']
    if row['message_id'] not in IDS or not text or not text.isascii() or text!=' '.join(text.split()):
        raise ValueError('One natural unwrapped ASCII paragraph without alignment is required')
    if any(ord(c)<32 or ord(c)>126 or c in '{}' for c in text):
        raise ValueError('No authored controls or layout markup')
    if row['native_argument_count']!=1 or text.count('%s')!=1 or '%' in text.replace('%s','') or row['source_native_macros']:
        raise ValueError('Exactly the one original ship-name argument and no invented source macros are required')
    if len(text.encode('ascii'))>=160:
        raise ValueError('Native input contract requires separately reviewed relocation for longer paragraphs')
    return text.encode('ascii')

def plan(common,arm,doc):
    source = inspect.getsource(previous.plan)
    replacements = [
        ('=={23}','=={22}'),('[2136,2137]','[2083,2086,2088]'),
        ('block==23','block==22'),('source.blocks[23]','source.blocks[22]'),
        ('rebuilt[23]','rebuilt[22]'),('DIRECTORY_OFFSET+23*4','DIRECTORY_OFFSET+22*4'),
        ('if b!=23','if b!=22'),
        ('all3666_unselected_or_retained_texts_and_native_copy_spans_preserved','all3665_unselected_or_retained_texts_and_native_copy_spans_preserved'),
        ('only_COMMON23_and_original_native_offset_directory_data_changed','only_COMMON22_and_original_native_offset_directory_data_changed'),
        ('old_new_block23_bytes','old_new_block22_bytes'),
        ('original_legacy_leading_cell_kept_no_new_formatter_membership','original_direct_consumer_no_authored_alignment_or_new_formatter_membership')]
    for old,new in replacements:
        assert old in source,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'current_entries':current_entries,'compiled':compiled,
        'IDS':IDS,'PROFILE':PROFILE,'SOURCE_COMMON':SOURCE_COMMON,'SOURCE_ARM':SOURCE_ARM}
    exec(compile(source,__file__,'exec'),env)
    return env['plan'](common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    c,a,proof = plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'source_plan_producer':'scripts/battle_victory_native_plan_v1396.py',
        'source_plan_producer_sha256':sha(Path('scripts/battle_victory_native_plan_v1396.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Research payload changes only2083/2086/2088;all3665 other texts/copies and entire runtime/selector/staged bytes preserved.',flush=True)
