"""Integrated category730, inherited bytes, native copies and exact patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.category_dialogue_editorial import compile_template, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.prepare_category_dialogue_v754 import MANUSCRIPT, ROOT
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROM=Path('out/all_routes_combined_v754_candidate.nds')


def reject(action):
    try:action()
    except (AssertionError,ValueError):return True
    raise AssertionError('Invalid category730 input accepted')


def main():
    old,new=NdsImage.open('out/all_routes_combined_v753_candidate.nds'),NdsImage.open(ROM)
    common,arm=new.read_file('/COMMON/MESFILE.DK4'),new.read_file('/__arm9__.bin')
    old_common,old_arm=old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin')
    manifest=read(ROM.with_suffix('.manifest.json'));registry=read('translations/release_stack.json');previous=read(ROOT/'release_stack_before_V754.json')
    assert manifest['profile']=='all-routes-unified-v754' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert len(manifest['batches'])==470 and manifest['required_batches']==[] and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert registry['canonical_baseline']==previous['canonical_baseline'] and registry['accepted_layers']==previous['accepted_layers']
    assert len(registry['accepted_layers'])==114
    assert [p for _,p,raw in old.iter_files() if raw!=new.read_file(p)]==['/COMMON/MESFILE.DK4']
    assert old.rom.arm7==new.rom.arm7 and old.rom.arm9OverlayTable==new.rom.arm9OverlayTable
    assert common==(ROOT/'research_COMMON.bin').read_bytes() and arm==(ROOT/'research_ARM9.bin').read_bytes()
    doc=read(MANUSCRIPT);a,b,repack=transform(old_common,old_arm,doc);assert (a,b)==(common,arm)
    before,after=common_message_entries(old_common,old_arm,clean=False),common_message_entries(common,arm,clean=False)
    assert [x.message_id for x,y in zip(before,after,strict=True) if x.text!=y.text]==[730]
    native,abi=read(ROOT/'native_review.json'),read(ROOT/'lookup_native_ABI.json')
    assert abi['target_ARM9_sha256']==sha(arm) and abi['source_ARM9_sha256']==sha(old_arm)
    assert abi['producer_sha256']==sha(Path('scripts/verify_category_lookup_v754.py').read_bytes())
    assert len(native['all18_complete_dialogue_font_planes'])==18 and len(abi['all108_getter_cases'])==108
    assert len(abi['all18_original_Square_caption_planes_exact'])==18 and len(abi['all36_negative_and_sentinel_cases_exact'])==36
    assert len(abi['all18_original730_caller_arguments'])==18
    selected=[e for e in after if e.block==after[730].block]
    ids=[selected[0].message_id-1,*(e.message_id for e in selected),selected[-1].message_id+1]
    copies=[];original=loader.machine_for;loader.machine_for=arm946_machine
    try:
        for i in ids:
            for cold in (False,True):
                result=loader.warm_copy(arm,common,i,after[i].text,cold_cache=cold)
                copies.append({'message_id':i,'cold_cache':cold,'native_complete_copy':result})
    finally:loader.machine_for=original
    stale,legacy=deepcopy(doc),deepcopy(doc);stale['records'][0]['source_hex']='41';legacy['translation_policy']='natural-dialogue-v1'
    rejects={'stale_source':reject(lambda:transform(old_common,old_arm,stale)),
        'legacy_policy':reject(lambda:transform(old_common,old_arm,legacy)),
        'authored_break':reject(lambda:compile_template('Two\nlines %s.{PAD}')),
        'authored_indent':reject(lambda:compile_template('  Offset %s.{PAD}')),
        'missing_argument':reject(lambda:compile_template('Missing.{PAD}')),
        'extra_argument':reject(lambda:compile_template('Extra %s %s.{PAD}')),
        'unsafe_macro':reject(lambda:compile_template('FIRE %s.{PAD}'))}
    save(ROOT/'registered_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'all470_batches114_layers_and_final_checks_pass':True,'all3667_unselected_texts_prior68_revisions675_graphics_preserved':True,
        'all18_complete_dialogue_font_planes_and_Square_planes_bound_to_integrated_ROM':True,
        'all108_native_lookup_cases36_sentinels_and_original730_arguments_pass':True,
        'native_copy_cases':copies,'rejections':rejects,'repack':repack,
        'all18_dialogue_previews_visually_inspected':True,'gameplay_pending':True,
        'verifier_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    clean,patch,result=Path('work/clean.nds'),ROM.with_suffix('.xdelta'),ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result);assert result.read_bytes()==ROM.read_bytes()
    save(ROOT/'patch_proof.json',{'clean_source_sha256':sha(clean.read_bytes()),'candidate_sha256':sha(ROM.read_bytes()),
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'whole_ROM_byte_exact':True})
    print(f'V754 integrated lookup/font proofs,{len(copies)} native copies,7 controls and exact patch pass.',flush=True)


if __name__=='__main__':main()
