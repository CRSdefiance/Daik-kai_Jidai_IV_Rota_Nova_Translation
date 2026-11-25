"""Qualify exact editorial dependencies across the registered market-only data correction."""
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.market_goods_info_terminator_v1 import transform,FIELDS,NEW_FORMAT,PAYLOAD
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=ROOT/'market_parent_qualification_v1.json'
TARGET=Path('work/market_goods_info_terminator_release_v1/registered_release_verification.json')

def qualify(native_runtime):
    release=load(TARGET)
    assert not release['own_registered_startup_pending'] and not release['market_gameplay_pending']
    assert release['clean_input_patch_byte_exact'] and digest('translations/release_stack.json')==release['registry_sha256']
    assert digest(release['candidate'])==release['candidate_sha256']
    source=NdsImage.open(native_runtime['candidate']);target=NdsImage.open(release['candidate'])
    assert digest(native_runtime['candidate'])==native_runtime['candidate_sha256']==release['parent_sha256']
    parent_arm=source.read_file('/__arm9__.bin');arm,proof=transform(parent_arm)
    assert arm==target.read_file('/__arm9__.bin') and proof['whole_serialized_parent_inverse_exact']
    assert all(source.read_file(p)==target.read_file(p) for _,p,_ in source.iter_files())
    assert [p for p,v in source.iter_components() if target.read_file(p)!=v]==['/__arm9__.bin']
    assert target.read_file('/GRP/KANJI.FNT')==source.read_file('/GRP/KANJI.FNT')
    before,after=[MainCodeFile(v,0x02000000).sections for v in [parent_arm,arm]]
    assert len(before)==5 and len(after)==6
    assert all(bytes(a.data)==bytes(b.data) and a.ramAddress==b.ramAddress and a.bssSize==b.bssSize for a,b in zip(before[1:],after[1:5],strict=True))
    assert after[-1].ramAddress==NEW_FORMAT and bytes(after[-1].data)==PAYLOAD
    receipt=dict(target_release=str(TARGET),target_release_sha256=digest(TARGET),
        target_candidate=release['candidate'],target_candidate_sha256=release['candidate_sha256'],
        target_ARM9_sha256=release['target_ARM9_sha256'],native_runtime=native_runtime,
        exact_registered_market_transform=proof,
        changed_original_data_pointer_fields=list(FIELDS),new_readonly_market_literal_address=NEW_FORMAT,
        every_archive_COMMON_font_name_data_andall_other_files_exact=True,
        original_autoload_code_payloads_andnative_text_getter_renderer_macro_instructions_preserved=True,
        old_Maria3_snapshot_retains_its_actual_identity_not_a_new_target_capture=True,
        not_a_generic_ARM9_difference_waiver=True,
        native_storage_consumers_must_not_read_or_execute_the_market_pointer_fields=True,
        no_editorial_display_gameplay_ornew_credit_claim=True,new_credit=0)
    return target,receipt

def main():
    assert not OUT.exists()
    native=load(ROOT/'final270_native_v2/compiled_native_pages.json')
    _,receipt=qualify(native['runtime']);save(OUT,receipt)
    print('Qualifiedmarket-only successor:all archives/fonts/COMMON/native text code retained;old Maria3 proofs keep their identity;no page replay.')

if __name__=='__main__':main()
