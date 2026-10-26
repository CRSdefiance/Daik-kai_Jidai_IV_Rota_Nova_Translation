"""Source-locked hot-spring13 repack;retain all other text and copy spans."""
import inspect
from pathlib import Path
from dk4tool.patch.duel_editorial import owned_entries
from scripts import ship_loss_surrender_native_plan_v1444 as previous
from scripts import hot_spring_runtime_v1614 as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hot_spring_payload_v1615')
MANUSCRIPT=Path('translations/hot_spring_editorial_manuscript_v1.json')
IDS=tuple(range(2275,2288))
PROFILE='expedition-hot-spring-role1-postmacro-v1'
SOURCE_COMMON='d91e1b835cf48b6949c1f484de7779756d72727e7ef87b363fb9d3cfcc9cba0b'
SOURCE_ARM=runtime.SOURCE
SOURCE_DIRECTORY=read('translations/fatigue_status_editorial_release_v1.json')['directory_sha256']

def current_entries(common,arm):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    return owned_entries(common,arm,SOURCE_DIRECTORY)

def compiled(row):
    text=row['english']
    if row['message_id'] not in IDS or not text or not text.isascii() or text!=' '.join(text.split()):raise ValueError('One natural unwrapped paragraph required')
    if any(ord(c)<32 or ord(c)>126 or c in '%{}' for c in text):raise ValueError('No authored controls,arguments or layout markup')
    if row['native_argument_count']!=0 or row['source_native_macros']:raise ValueError('No original argument or macro in this family')
    table=0x02116D80 if row['message_id']<=2281 else 0x02116D60
    if row['source_table']!=table or row['original_role']!=1:raise ValueError('Preserve the original role1 speech-table contract')
    if len(text.encode('ascii'))>=160:raise ValueError('Longer paragraphs need a reviewed native contract')
    return text.encode('ascii')

def plan(common,arm,doc):
    source=inspect.getsource(previous.plan)
    for old,new in [('assert changed==[n for n in IDS if n!=2100]',"assert changed==[r['message_id'] for r in doc['records'] if r['editorial_decision']=='revise'] and len(changed)==12"),
        ('=={22}','=={24}'),('r.block==22','r.block==24'),('source.blocks[22]','source.blocks[24]'),('rebuilt[22]','rebuilt[24]'),
        ('DIRECTORY_OFFSET+22*4','DIRECTORY_OFFSET+24*4'),('if b!=22','if b!=24'),
        ('all3645_unselected_or_retained_texts_and_native_copy_spans_preserved','all3656_unselected_or_retained_texts_and_native_copy_spans_preserved'),
        ('only_COMMON22_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON24_native_metadata_and_existing188_172_selector_spans_changed'),
        ('old_new_block22_bytes','old_new_block24_bytes')]:
        assert old in source,old;source=source.replace(old,new)
    env={**previous.__dict__,'SOURCE_COMMON':SOURCE_COMMON,'SOURCE_ARM':SOURCE_ARM,'IDS':IDS,'PROFILE':PROFILE,
        'runtime':runtime,'current_entries':current_entries,'compiled':compiled}
    exec(compile(source,__file__,'exec'),env);return env['plan'](common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);rom=NdsImage.open(doc['current_ROM']);c,a,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp,ap=ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin';cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),'manuscript':str(MANUSCRIPT),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Hot-spring13 repacked:12 revisions1 retained;3656 other/retained copies,40 blocks and later screenshot corrections preserved;188/172/123040 sizes fixed.')
