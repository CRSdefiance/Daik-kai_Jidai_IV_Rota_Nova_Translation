"""Verify exact integrated contents,negative gates and clean patch reconstruction."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import recruitment_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta,make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_recruitment_release_v773 import CURRENT,CONFIG,MANUSCRIPT,ROOT,RESEARCH
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v773_candidate.nds')


def reject(action):
    try:action()
    except(ValueError,AssertionError):return True
    raise AssertionError('Malformed recruitment prose accepted')


def main():
    old,new=[NdsImage.open(p) for p in(CURRENT,ROM)]
    oc,oa=old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin')
    c,a=new.read_file('/COMMON/MESFILE.DK4'),new.read_file('/__arm9__.bin')
    manifest=read(ROM.with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    before=read(ROOT/'release_stack_before_v773.json')
    assert manifest['profile']=='all-routes-unified-v773' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and len(manifest['batches'])==470 and not manifest['required_batches']
    assert registry['accepted_layers']==before['accepted_layers'] and len(registry['accepted_layers'])==114
    assert registry['canonical_baseline']==before['canonical_baseline']
    files=[{p:v for _,p,v in r.iter_files()} for r in(old,new)]
    components=[dict(r.iter_components()) for r in(old,new)]
    assert files[0].keys()==files[1].keys() and components[0].keys()==components[1].keys()
    assert {p for p in files[0] if files[0][p]!=files[1][p]}=={'/COMMON/MESFILE.DK4'}
    assert {p for p in components[0] if components[0][p]!=components[1][p]}=={'/__arm9__.bin'}
    assert old.rom.arm9OverlayTable==new.rom.arm9OverlayTable
    assert owned.apply_release(oc,oa,CONFIG)[:2]==(c,a)
    assert c==(RESEARCH/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a==(RESEARCH/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    entries=common_message_entries(c,a,clean=False);old_entries=common_message_entries(oc,oa,clean=False)
    doc=read(MANUSCRIPT)
    assert all(entries[r['message_id']].text==owned.compile_text(r) for r in doc['records'])
    assert all(x.text==y.text for x,y in zip(old_entries,entries,strict=True) if x.message_id not in owned.IDS)
    assert all(entries[n].text==old_entries[n].text for n in(676,677))
    copies=[read(RESEARCH/f'native_copies/native_copies_block_{k:02d}.json') for k in range(41)]
    assert sum(len(r['cases']) for r in copies)==7336
    assert all(r['COMMON_sha256']==sha(c) and r['ARM9_sha256']==sha(a) for r in copies)
    variants={}
    for name in('source','current','formatting','legacy'):
        d=deepcopy(doc)
        if name=='source':d['records'][0]['source_hex']='41'
        elif name=='current':d['records'][0]['current_text_hex']='41'
        elif name=='formatting':d['records'][0]['review']['formatting']=False
        else:d['translation_policy']='natural-dialogue-v1'
        variants[name]=reject(lambda d=d:owned.transform(oc,oa,d))
    example=next(r for r in doc['records'] if r['message_id']==905)
    for name,text in(('indent','  Hello %s %s.{PAD}'),('padding','Hello  %s %s.{PAD}'),
            ('linebreak','Hello\n%s %s.{PAD}'),('lost_argument','Hello %s.{PAD}'),('extra_argument','Hello %s %s %s.{PAD}')):
        variants[name]=reject(lambda text=text:owned.compile_text({**example,'english':text}))
    row=deepcopy(example);row['English_argument_source_indices']=[1,0]
    variants['wrong_town_status_order']=reject(lambda:owned.compile_text(row))
    save(ROOT/'registered_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'all470_batches114_accepted_layers_and_graphics_retained':True,
        'only_COMMON_ARM9_change_from_V770':True,'all3643_other_strings_and_user676_677_exact':True,
        'all7336_complete_native_copies':True,'negative_gates':variants,
        'producer_sha256':sha(Path(__file__).read_bytes()),'actual_scenes_pending':True,'full_goal_complete':False})
    clean=Path('work/clean.nds');assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');reconstructed=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstructed);assert reconstructed.read_bytes()==ROM.read_bytes()
    save(ROOT/'patch_proof.json',{'clean_source_sha256':sha(clean.read_bytes()),'candidate_sha256':sha(ROM.read_bytes()),
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'byte_exact_reconstruction':True,
        'canonical_base_sha256':registry['canonical_baseline']['sha256']})
    print('V773 exact integrated contents,470/114 layers,7336 whole copies,10 negative gates and clean patch pass;actual scenes pending.',flush=True)


if __name__=='__main__':main()
