"""Bind actual item/stat names and the preserved Proof convention for Lil residual A."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    out = ROOT/'scoped_terms_reference_v1.json'
    assert not out.exists()
    currentpath = ROOT/'current_v1/current_effective.json'
    current = load(currentpath)
    runtime = current['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=2)
    assert ctx.receipt() == runtime
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    def field(offset, source, english):
        a, b = [string(raw, struct.unpack_from('<I', arm, offset)[0])
                for arm, raw in [(clean, clean), (ctx.arm, ctx.raw)]]
        assert a['text'] == source and b['text'] == english
        return dict(pointer_field_offset=offset, source=a, current=b,
            source_field_hex=clean[offset:offset+4].hex(), current_field_hex=ctx.arm[offset:offset+4].hex())
    itempath = Path('translations/all_item_names_arm9_v1.json')
    registered = {r['offset']:r for r in load(itempath)['records'] if 'english' in r}
    items = []
    for at, jp, en in [
        (1172848, '血塗られたシャムシール', 'Bloodstained Shamshir'),
        (1173136, '妖刀村正', 'Muramasa'),
        (1173760, '魔法の革手袋', 'Magic Leather Gloves'),
        (1174264, '悪魔を貫く矢', 'Demon-Piercing Arrow'),
        (1174624, 'グプタの霊獣', 'Gupta Spirit Beast'),
        (1175032, '凍てついたバラ', 'Frozen Rose')]:
        row = field(at, jp, en)
        assert registered[at]['english'] == en
        row['registered_record'] = registered[at]['id']
        items.append(row)
    spirit = field(1344424, '精神', 'Spirit')
    short = [field(1295216, '覇者の証', 'Proof'), field(1503776, '覇者の証', 'Conq Proof')]
    priorpath = Path('translations/maria310_integrated_final_review_v1.json')
    prior = load(priorpath)
    anchor = next(r for r in prior['records'] if r['id'] == 'DK4_MES_B53_R0006')
    assert anchor['english'] == 'That makes all the Proofs of Conquest...' and all(anchor['review'].values())
    assert digest(prior['target_ROM']) == prior['target_ROM_sha256']
    old = NdsImage.open(prior['target_ROM'])
    assert old.read_file('/__arm9__.bin') == ctx.arm
    assert old.read_file('/COMMON/MESFILE.DK4') == ctx.common
    before = IlnkContainer.parse(old.read_file('/data/SC3.DK4')).blocks[53]
    now = IlnkContainer.parse(ctx.image.read_file('/data/SC3.DK4')).blocks[53]
    assert before == now
    ref = anchor['planned_integrated_reference']
    raw = bytes.fromhex(ref['exact_stored_hex'])
    assert now[ref['offset']:ref['offset']+len(raw)+1] == raw+b'\0'
    save(out, dict(runtime=runtime, items=items, stats=[spirit], short_Proof_UI_consumers=short,
        full_Proof_term=dict(singular='Proof of Conquest', plural='Proofs of Conquest', short='Proof',
            approved_integrated_reference=dict(path=str(priorpath), id=anchor['id'], source_reference=anchor['source_reference'],
                current_reference=ref, english=anchor['english'], review=anchor['review'])),
        only_source_spoken_item_titles_may_be_inserted=True,
        Gupta_statue_gloves_andfigurehead_remain_descriptive_where_source_unnamed=True,
        term_bindings_not_gameplay_effect_orfont_approval=True, new_credit=0,
        evidence={str(p):digest(p) for p in [currentpath,itempath,priorpath,Path(__file__)]}))
    print('PASS six item titles,Spirit and exact preserved Proofs of Conquest anchor;no ROM changes.')


if __name__ == '__main__':
    main()
