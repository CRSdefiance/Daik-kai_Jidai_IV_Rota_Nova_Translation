"""Verify the combined candidate,hard editorial gates and exact clean patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import tavern_schemes_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_schemes_common_v776 import ROOT,MANUSCRIPT
from scripts.register_schemes_release_v776 import CONFIG
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v776_candidate.nds')


def reject(action):
    try:action()
    except(ValueError,AssertionError):return True
    raise AssertionError('Invalid editorial contract accepted')


def main():
    old,new=[NdsImage.open(p) for p in ('out/all_routes_combined_v773_candidate.nds',ROM)]
    oc,oa=old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin')
    c,a=new.read_file('/COMMON/MESFILE.DK4'),new.read_file('/__arm9__.bin')
    m=read(ROM.with_suffix('.manifest.json'))
    registry=read('translations/release_stack.json')
    before=read(ROOT/'release_stack_before_v776.json')
    assert m['profile']=='all-routes-unified-v776' and m['candidate_sha256']==sha(ROM.read_bytes())
    assert m['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert all(m['checks'].values()) and len(m['batches'])==470 and not m['required_batches']
    assert registry['canonical_baseline']==before['canonical_baseline']
    assert registry['accepted_layers']==before['accepted_layers'] and len(registry['accepted_layers'])==114
    files=[{p:v for _,p,v in r.iter_files()} for r in (old,new)]
    components=[dict(r.iter_components()) for r in (old,new)]
    assert files[0].keys()==files[1].keys() and components[0].keys()==components[1].keys()
    assert {p for p in files[0] if files[0][p]!=files[1][p]}=={'/COMMON/MESFILE.DK4'}
    assert {p for p in components[0] if components[0][p]!=components[1][p]}=={'/__arm9__.bin'}
    assert old.rom.arm9OverlayTable==new.rom.arm9OverlayTable
    assert owned.apply_release(oc,oa,CONFIG)[:2]==(c,a)
    assert c==(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a==(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    old_entries=common_message_entries(oc,oa,clean=False)
    entries=common_message_entries(c,a,clean=False)
    doc=read(MANUSCRIPT)
    assert all(entries[r['message_id']].text==owned.compile_text(r) for r in doc['records'])
    assert all(x.text==y.text for x,y in zip(old_entries,entries,strict=True) if x.message_id not in owned.IDS)
    copies=[read(ROOT/f'native_copies/native_copies_block_{n:02d}.json') for n in range(41)]
    assert sum(len(p['cases']) for p in copies)==7336
    assert all(p['COMMON_sha256']==sha(c) and p['ARM9_sha256']==sha(a) for p in copies)
    negative={}
    for name in ('source','current','formatting','legacy'):
        d=deepcopy(doc)
        if name=='source':d['records'][0]['source_hex']='41'
        elif name=='current':d['records'][0]['current_text_hex']='41'
        elif name=='formatting':d['records'][0]['review']['formatting']=False
        else:d['translation_policy']='natural-dialogue-v1'
        negative[name]=reject(lambda d=d:owned.transform(oc,oa,d))
    example=next(r for r in doc['records'] if r['message_id']==956)
    for name,text in (('indent','  Hello %s %s.{PAD}'),('padding','Hello  %s %s.{PAD}'),
            ('linebreak','Hello\n%s %s.{PAD}'),('lost_argument','Hello %s.{PAD}'),
            ('extra_argument','Hello %s %s %s.{PAD}'),('macro','Hello %s %s {FO}.{PAD}')):
        negative[name]=reject(lambda text=text:owned.compile_text({**example,'english':text}))
    negative['reversed_town_faction_order']=reject(lambda:owned.compile_text({**example,'English_argument_source_indices':[1,0]}))
    save(ROOT/'registered_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'all470_batches114_accepted_layers_and_graphics_retained':True,
        'only_COMMON_ARM9_change_from_V773':True,'all3612_other_strings_exact':True,
        'all7336_complete_native_copies':True,'negative_gates':negative,
        'producer_sha256':sha(Path(__file__).read_bytes()),'actual_scenes_pending':True,'full_goal_complete':False})
    clean=Path('work/clean.nds')
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta')
    rebuilt=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,ROM,patch)
    apply_xdelta(clean,patch,rebuilt)
    assert rebuilt.read_bytes()==ROM.read_bytes()
    save(ROOT/'patch_proof.json',{'clean_source_sha256':sha(clean.read_bytes()),'candidate_sha256':sha(ROM.read_bytes()),
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'byte_exact_reconstruction':True,
        'canonical_base_sha256':registry['canonical_baseline']['sha256']})
    print('V776 complete inheritance,exact scoped contents,7336 copies,11 negative gates and clean-source patch pass. Actual scenes pending.',flush=True)


if __name__=='__main__':main()
