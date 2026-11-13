"""Respect the original COMMON22/23 boundary inside the surrender family.

V1444 stopped before output at its single-block assumption. IDs2100-2105 live
in23;all other selected records live in22. Repack only those two native blocks.
"""
import inspect
from pathlib import Path
from scripts import ship_loss_surrender_native_plan_v1444 as previous
from scripts.ship_loss_surrender_native_plan_v1444 import MANUSCRIPT,IDS,PROFILE,SOURCE_COMMON,SOURCE_ARM,compiled
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_loss_surrender_payload_v1444b')

def plan(common,arm,doc):
    source = inspect.getsource(previous.plan)
    start = source.index('    numbers = [r.message_id for r in before if r.block==22]')
    end = source.index('    a,c = bytes(target)',start)
    replacement = '''    fields,metadata,block_sizes = [],[],[]
    def put(at,value):
        target[at:at+len(value)] = value;fields.append([at,len(value)])
        metadata.append({'address':0x02000000+at,'source_hex':arm[at:at+len(value)].hex(),'target_hex':value.hex()})
    for block in [22,23]:
        numbers = [r.message_id for r in before if r.block==block]
        assert numbers==list(range(numbers[0],numbers[-1]+1))
        body = bytearray()
        for n in numbers:
            row = before[n];payload = source.blocks[block][row.block_offset:row.copy_end]
            assert 0<len(payload)<512 and payload.startswith(row.text+b'\\0')
            if n in changed:
                assert not set(payload[len(row.text)+1:])-{0,32}
                payload = authored[n]+b'\\0'
            put(TABLE_OFFSET+n*2,struct.pack('<H',len(body)));body.extend(payload)
        assert 0<len(body)<=8192
        rebuilt[block] = bytes(body);put(DIRECTORY_OFFSET+block*4,struct.pack('<HH',numbers[0],len(body)))
        block_sizes.append({'block':block,'before_bytes':len(source.blocks[block]),'after_bytes':len(body)})
'''
    source = source[:start]+replacement+source[end:]
    for old,new in [
        ('=={22}','=={22,23}'),('if b!=22','if b not in [22,23]'),
        ('    for n in numbers:\n        if n not in changed:',
         '    for n in [r.message_id for r in before if r.block in [22,23]]:\n        if n not in changed:'),
        ('source.blocks[22][old.block_offset:old.copy_end]==rebuilt[22][new.block_offset:new.copy_end]',
         'source.blocks[old.block][old.block_offset:old.copy_end]==rebuilt[new.block][new.block_offset:new.copy_end]'),
        ('all40_other_blocks_and_opaque_duel_prefix_exact','all39_other_blocks_and_opaque_duel_prefix_exact'),
        ('only_COMMON22_native_metadata_and_existing188_172_selector_spans_changed',
         'only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed'),
        ("'old_new_block22_bytes':[len(source.blocks[22]),len(body)]","'old_new_block_bytes':block_sizes")]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = dict(previous.__dict__)
    exec(compile(source,__file__,'exec'),env)
    return env['plan'](common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT);rom = NdsImage.open(doc['current_ROM'])
    c,a,proof = plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('24 loss/surrender reports repacked in native COMMON22/23;23 revisions,one retention;3645 other texts/copies and all allocations preserved.',flush=True)
