"""Seven source-reviewed retreat paragraphs and their exact role-table scope."""
import inspect
from pathlib import Path
from scripts import ship_loss_surrender_native_plan_v1444 as previous
from scripts import retreat_transfer_runtime_v1509 as runtime
from dk4tool.patch.battle_reaction_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/retreat_transfer_payload_v1511')
MANUSCRIPT=Path('translations/retreat_transfer_editorial_manuscript_v1.json')
IDS=tuple(range(2683,2690))
PROFILE='flagship-transfer-role1-postmacro-v1'
SOURCE_COMMON='b79f4fb98c4652b7f2a0c1bda0ab370243c6df885c8b47330804c1bfc2b45055'
SOURCE_ARM=runtime.SOURCE

def compiled(row):
    text=row['english']
    if row['message_id'] not in IDS or not text or not text.isascii() or text!=' '.join(text.split()):
        raise ValueError('One natural unwrapped paragraph without alignment is required')
    if any(ord(c)<32 or ord(c)>126 or c in '{}' for c in text):raise ValueError('No authored controls or layout markup')
    if row['native_argument_count']!=1 or text.count('%s')!=1 or '%' in text.replace('%s','') or row['source_native_macros']:
        raise ValueError('Exactly one original replacement-ship name and no invented macros are required')
    if len(text.encode('ascii'))>=160:raise ValueError('Longer paragraphs require a separately reviewed native contract')
    return text.encode('ascii')

def plan(common,arm,doc):
    source=inspect.getsource(previous.plan)
    for old,new in [
        ('assert changed==[n for n in IDS if n!=2100]',"assert changed==[r['message_id'] for r in doc['records'] if r['editorial_decision']=='revise'] and len(changed)==3"),
        ('=={22}','=={28}'),('r.block==22','r.block==28'),('source.blocks[22]','source.blocks[28]'),
        ('rebuilt[22]','rebuilt[28]'),('DIRECTORY_OFFSET+22*4','DIRECTORY_OFFSET+28*4'),('if b!=22','if b!=28'),
        ('all3645_unselected_or_retained_texts_and_native_copy_spans_preserved','all3665_unselected_or_retained_texts_and_native_copy_spans_preserved'),
        ('only_COMMON22_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON28_native_metadata_and_existing188_selector_span_changed'),
        ('old_new_block22_bytes','old_new_block28_bytes')]:
        assert old in source,old
        source=source.replace(old,new)
    env={**previous.__dict__,'SOURCE_COMMON':SOURCE_COMMON,'SOURCE_ARM':SOURCE_ARM,'IDS':IDS,'PROFILE':PROFILE,
        'runtime':runtime,'current_entries':current_entries,'compiled':compiled}
    exec(compile(source,__file__,'exec'),env)
    return env['plan'](common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);rom=NdsImage.open(doc['current_ROM'])
    c,a,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp=ROOT/'COMMON_RESEARCH_ONLY.DK4';ap=ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Retreat7 repacked in COMMON28;3 revisions,3665 other/retained texts/copy spans,40 blocks and all allocations exact;185/188 selector bytes,gate unchanged.')
