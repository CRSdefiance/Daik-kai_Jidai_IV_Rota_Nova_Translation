"""Source-locked32 reaction paragraphs in original COMMON23;no new ROM."""
import inspect
from pathlib import Path
from scripts import ship_loss_surrender_native_plan_v1444 as previous
from scripts import battle_reaction_runtime_v1483 as runtime
from dk4tool.patch.ship_loss_surrender_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reaction_payload_v1484')
MANUSCRIPT=Path('translations/battle_reactions_editorial_manuscript_v1.json')
IDS=tuple(range(2147,2179))
PROFILE='battle-reactions-actor-postmacro-v1'
SOURCE_COMMON='241fd00c63d1677ac6d00593868f635ee4bfb3a30c46f4cc143ec4d1796790f4'
SOURCE_ARM=runtime.SOURCE

def compiled(row):
    text=row['english']
    if row['message_id'] not in IDS or not text or not text.isascii() or text!=' '.join(text.split()):
        raise ValueError('One natural unwrapped paragraph without alignment is required')
    if any(ord(c)<32 or ord(c)>126 or c in '{}%' for c in text):
        raise ValueError('No authored controls,layout markup or invented printf arguments')
    if row['native_argument_count']!=0 or row['source_native_macros']:
        raise ValueError('Original reactions have no runtime substitutions or speech macros')
    if len(text.encode('ascii'))>=160:
        raise ValueError('Longer paragraphs require a separately reviewed native input contract')
    return text.encode('ascii')

def plan(common,arm,doc):
    source=inspect.getsource(previous.plan)
    replacements=[
        ("row['current_text_hex']","row['current_hex']"),
        ('assert changed==[n for n in IDS if n!=2100]',"assert changed==[r['message_id'] for r in doc['records'] if r['editorial_decision']=='revise']"),
        ('=={22}','=={23}'),('r.block==22','r.block==23'),('source.blocks[22]','source.blocks[23]'),
        ('rebuilt[22]','rebuilt[23]'),('DIRECTORY_OFFSET+22*4','DIRECTORY_OFFSET+23*4'),('if b!=22','if b!=23'),
        ('all3645_unselected_or_retained_texts_and_native_copy_spans_preserved','all3652_unselected_or_retained_texts_and_native_copy_spans_preserved'),
        ('only_COMMON22_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON23_native_metadata_and_existing188_selector_span_changed'),
        ('old_new_block22_bytes','old_new_block23_bytes')]
    for old,new in replacements:
        assert old in source,old
        source=source.replace(old,new)
    env={**previous.__dict__,'SOURCE_COMMON':SOURCE_COMMON,'SOURCE_ARM':SOURCE_ARM,'IDS':IDS,'PROFILE':PROFILE,
        'runtime':runtime,'current_entries':current_entries,'compiled':compiled}
    exec(compile(source,__file__,'exec'),env)
    return env['plan'](common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);rom=NdsImage.open(doc['current_ROM'])
    common,arm,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp=ROOT/'COMMON_RESEARCH_ONLY.DK4';ap=ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(common);ap.write_bytes(arm)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('32 reaction paragraphs repacked;16 byte revisions,3652 other native texts/copies and40 blocks exact;184/188 selector bytes,gate/staged allocations exact.')
