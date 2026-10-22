"""Registered source-locked ceremony paragraphs and bounded native consumers."""

from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.inn_editorial import current_entries as previous_entries
from dk4tool.patch.palace_label_boundaries import verify_final
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.ceremony_runtime_v808 import SOURCE as SOURCE_ARM,ROOT as RUNTIME_ROOT
from scripts.prepare_ceremony_common_v809 import ROOT,IDS,compiled,plan
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read

SOURCE_COMMON='027e272120e9ce2a657ee3cd72490c4caae101af5c19b4427e75412766d93967'


def current_entries(common,arm):
    cfg=read('translations/ceremony_editorial_release_v1.json')
    assert sha(common)==cfg['target_common_sha256'] and sha(arm)==cfg['target_arm9_sha256']
    return local_entries(cfg['directory_sha256'])(common,arm,clean=False)


def apply_release(common,arm,path):
    cfg=read(path);assert cfg['format']=='dk4-ceremony-editorial-v1'
    assert sha(common)==cfg['source_common_sha256']==SOURCE_COMMON
    assert sha(arm)==cfg['source_arm9_sha256']==SOURCE_ARM
    for name,h in cfg['dependencies'].items():assert sha(Path(name).read_bytes())==h,name
    manuscript=Path(cfg['manuscript']);assert sha(manuscript.read_bytes())==cfg['manuscript_sha256']
    doc=read(manuscript);validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert tuple(r['message_id'] for r in doc['records'])==IDS
    draft_path=Path(doc['reviewed_research_manuscript'])
    assert sha(draft_path.read_bytes())==doc['reviewed_research_manuscript_sha256']
    draft=read(draft_path)
    keys=lambda rows:[(r['message_id'],r['english'],r['source_meaning']) for r in rows if r['message_id']!=64]
    assert keys(doc['records'])==keys(draft['records'])
    clean,canonical=[NdsImage.open(p) for p in ('work/clean.nds','out/raphael_natural_v2_accepted_base.nds')]
    jp=parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    accepted=parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    prior=previous_entries(common,arm)
    for row in doc['records']:
        n=row['message_id'];assert row['source_hex']==jp[n].text.hex()
        assert row['canonical_source_hex']==accepted[n].text.hex() and row['current_text_hex']==prior[n].text.hex()
        assert all(row['review'][g] for g in ('source','context','localization','naturalness','formatting'))
    c,a,proof=plan(common,arm,doc['records'])
    assert sha(c)==cfg['target_common_sha256'] and sha(a)==cfg['target_arm9_sha256']
    native=read(ROOT/'production_layout.json');copies=read(ROOT/'complete_native_copies.json')
    assert native['ARM9_sha256']==copies['ARM9_sha256']==sha(a)
    assert native['COMMON_sha256']==copies['COMMON_sha256']==sha(c)
    assert native['native_layouts']==native['full_font_planes']==201 and not native['findings']
    assert copies['count']==7336 and copies['every3668_selection_warm_and_cold_full_span_verified']
    assert read(RUNTIME_ROOT/'scope_proof.json')['cases']==35704
    assert read(RUNTIME_ROOT/'status_contracts.json')['count']==140
    assert read(RUNTIME_ROOT/'literal_equivalence.json')['count']==2326
    modal=read(RUNTIME_ROOT/'modal_scope.json')
    assert modal['exact_six_new_modal_IDs']==[289,290,291,293,294,295]
    assert modal['all_other3662_modal_ID_outputs_and_wrap_selection_exact'] and len(modal['wrong_parent_controls'])==231
    source_layout=read('work/analysis/ceremony_layout_v807_name_bounds/research_report.json')
    visual=read('work/analysis/ceremony_layout_v807_name_bounds/visual_review.json')
    assert visual['all17_sheets_visually_inspected'] and len(source_layout['complete_font_planes'])==202
    after=local_entries(proof['directory_sha256'])(c,a,clean=False)
    assert all(after[n].text==prior[n].text for n in (64,292,346,347,348,676,677))
    assert all(after[r['message_id']].text==compiled(r) for r in doc['records'])
    verify_final(a)
    return c,a,proof
