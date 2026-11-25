"""Bind item/location labels andthe established full Proof term to exact current consumers."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from dk4tool.patch.grand_race_menu_release import sha


def main():
    out = ROOT/'scoped_terms_reference_v1.json'
    assert not out.exists()
    current_path = ROOT/'current_v1/current_effective.json'
    current = load(current_path)
    runtime = current['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    assert ctx.receipt() == runtime
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')

    def field(offset, source, english):
        a,b = [string(raw,struct.unpack_from('<I',arm,offset)[0]) for arm,raw in [(clean,clean),(ctx.arm,ctx.raw)]]
        assert a['text'] == source and b['text'] == english
        return dict(pointer_field_offset=offset,source=a,current=b,
            source_field_hex=clean[offset:offset+4].hex(),current_field_hex=ctx.arm[offset:offset+4].hex())

    item_path = Path('translations/all_item_names_arm9_v1.json')
    labels = {r['offset']:r for r in load(item_path)['records'] if 'english' in r}
    items = []
    for offset, source, english in [
        (1173136,'妖刀村正','Muramasa'), (1173448,'孔雀かたびら','Peacock Mail'),
        (1173544,'ジャガー神の宿る胴着',"Jaguar God's Vest"), (1173736,'ミネルヴァの盾','Minerva Shield'),
        (1174432,'ヘスティアの釜',"Hestia's Pot"), (1175008,'アリスタルコスの望遠鏡','Aristarchus Telescope')]:
        row = field(offset,source,english)
        assert labels[offset]['english'] == english
        row['registered_record'] = labels[offset]['id']
        items.append(row)
    location = field(1162288,'サンチャゴ大聖堂','Santiago Cathedral')
    short = [field(1295216,'覇者の証','Proof'),field(1503776,'覇者の証','Conq Proof')]
    prior_path = Path('translations/maria310_integrated_final_review_v1.json')
    prior = load(prior_path)
    anchor = next(r for r in prior['records'] if r['id']=='DK4_MES_B53_R0006')
    assert anchor['english'] == 'That makes all the Proofs of Conquest...' and all(anchor['review'].values())
    old_image = NdsImage.open(prior['target_ROM'])
    assert digest(prior['target_ROM']) == prior['target_ROM_sha256']
    assert old_image.read_file('/__arm9__.bin') == ctx.arm and old_image.read_file('/COMMON/MESFILE.DK4') == ctx.common
    old_blocks = IlnkContainer.parse(old_image.read_file('/data/SC3.DK4')).blocks
    blocks = IlnkContainer.parse(ctx.image.read_file('/data/SC3.DK4')).blocks
    assert blocks[53] == old_blocks[53]
    ref = anchor['planned_integrated_reference']
    raw = bytes.fromhex(ref['exact_stored_hex'])
    assert blocks[53][ref['offset']:ref['offset']+len(raw)+1] == raw+b'\0'
    save(out,dict(runtime=runtime,items=items,locations=[location],short_Proof_UI_consumers=short,
        full_Proof_term=dict(source='覇者の証',singular='Proof of Conquest',plural='Proofs of Conquest',short='Proof',
            approved_integrated_reference=dict(path=str(prior_path),id=anchor['id'],source_reference=anchor['source_reference'],
                source_hex=anchor['source_hex'],current_stored_reference=ref,english=anchor['english'],review=anchor['review']),
            exact_current_block53_sha256=sha(blocks[53]),same_ARM9_COMMON_andcomplete_anchor_block=True,
            legacy_Conquerors_Proof_variants_in_current_unreviewed_dialogue_not_new_approval=True),
        body_Santiago_punctuation_variant_matches_native_location_identity=True,
        no_named_sword_lamp_cross_orrescuer_reward_invented=True,
        term_reference_only_not_new_font_oractual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [current_path,item_path,prior_path,Path(__file__)]}))
    print('Bound six items,Santiago Cathedral,two short Proof UI consumers andexact registered Proofs of Conquest story anchor.')


if __name__ == '__main__':
    main()
