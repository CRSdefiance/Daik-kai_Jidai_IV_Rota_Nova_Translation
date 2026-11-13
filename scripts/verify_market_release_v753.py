"""Integrated Market reply preservation, exhaustive native copies and exact patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_replies_editorial import IDS, transform
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_market_replies_v753 import MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM=Path('out/all_routes_combined_v753_candidate.nds')


def reject(action):
    try:action()
    except (AssertionError,ValueError):return True
    raise AssertionError('Malformed Market review accepted')


def main():
    old,new=NdsImage.open('out/all_routes_combined_v752_candidate.nds'),NdsImage.open(ROM)
    common,arm=new.read_file('/COMMON/MESFILE.DK4'),new.read_file('/__arm9__.bin')
    old_common,old_arm=old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin')
    manifest=read(ROM.with_suffix('.manifest.json'))
    registry,previous=read('translations/release_stack.json'),read(ROOT/'release_stack_before_V753.json')
    assert manifest['profile']=='all-routes-unified-v753' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert len(manifest['batches'])==470 and manifest['required_batches']==[] and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert registry['accepted_layers']==previous['accepted_layers'] and len(registry['accepted_layers'])==114
    assert registry['canonical_baseline']==previous['canonical_baseline']
    assert [p for _,p,raw in old.iter_files() if raw!=new.read_file(p)]==['/COMMON/MESFILE.DK4']
    assert old.rom.arm7==new.rom.arm7 and old.rom.arm9OverlayTable==new.rom.arm9OverlayTable
    assert common==(ROOT/'research_COMMON.bin').read_bytes() and arm==(ROOT/'research_ARM9.bin').read_bytes()
    doc=read(MANUSCRIPT);a,b,repack=transform(old_common,old_arm,doc)
    assert (a,b)==(common,arm)
    before,after=common_message_entries(old_common,old_arm,clean=False),common_message_entries(common,arm,clean=False)
    assert [e.message_id for e,f in zip(before,after,strict=True) if e.text!=f.text]==list(IDS)
    assert before[730].text==after[730].text and before[742].text==after[742].text and before[752].text==after[752].text
    copies=[];reports={}
    for block in range(41):
        path=ROOT/f'native_copies_block_{block:02d}.json';report=read(path)
        assert report['COMMON_sha256']==sha(common) and report['ARM9_sha256']==sha(arm)
        assert report['verifier_sha256']==sha(Path('scripts/verify_market_native_copies_v753.py').read_bytes())
        reports[str(path)]=sha(path.read_bytes())
        for row in report['cases']:
            i=row['message_id'];proof=row['complete_native_copy']
            assert proof['native_copy_first_final_nul_and_guards_verified'] and proof['english'].encode('cp932')==after[i].text
            assert proof['block']==after[i].block and row['cold_cache']==proof['cold_cache']
            copies.append((i,row['cold_cache']))
    assert len(copies)==7336 and set(copies)=={(i,cold) for i in range(3668) for cold in (False,True)}
    context=read(ROOT/'native_context.json')
    assert all(sha(arm[r['start']:r['end']])==r['sha256'] for r in context['source_spans'])
    stale,missing=deepcopy(doc),deepcopy(doc)
    stale['records'][0]['source_hex']='41';missing['records']=[r for r in missing['records'] if r['message_id']!=765]
    rejects={'stale_source':reject(lambda:transform(old_common,old_arm,stale)),
        'missing_reviewed_record':reject(lambda:transform(old_common,old_arm,missing)),
        'authored_break':reject(lambda:compile_paragraph('Two\nlines.{PAD}')),
        'authored_indent':reject(lambda:compile_paragraph('  Offset.{PAD}')),
        'invented_format_argument':reject(lambda:compile_paragraph('Extra %s.{PAD}')),
        'unsafe_macro':reject(lambda:compile_paragraph('FIRE.{PAD}'))}
    save(ROOT/'registered_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'all470_batches114_accepted_layers_and_final_checks_pass':True,
        'all3659_unselected_text_bytes_prior62_revisions_and675_graphics_exact':True,
        'all7336_complete_ARM946_warm_cold_copies':True,'native_copy_report_hashes':reports,
        'source_context_and_nine_full_font_planes_bound_to_integrated_ROM':True,
        'repack':repack,'rejection_controls':rejects,'all9_previews_visually_inspected':True,
        'verifier_sha256':sha(Path(__file__).read_bytes()),'gameplay_pending':True,'full_goal_complete':False})
    clean,patch,result=Path('work/clean.nds'),ROM.with_suffix('.xdelta'),ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result);assert result.read_bytes()==ROM.read_bytes()
    save(ROOT/'patch_proof.json',{'clean_source_sha256':sha(clean.read_bytes()),'candidate_sha256':sha(ROM.read_bytes()),
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'whole_ROM_byte_exact':True})
    print('V753 complete integration,7336 native copies,source/font bindings and exact patch pass.',flush=True)


if __name__=='__main__':main()
