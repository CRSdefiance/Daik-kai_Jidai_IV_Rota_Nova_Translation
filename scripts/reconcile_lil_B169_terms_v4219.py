"""Bind current Proof/Tavern/ruins terms and preserve exact older consistency leads."""
import unicodedata
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_terms_v4219')
SOURCE = Path('work/analysis/lil_B169_source_v4211/all36_clean_current_complete_context.json')
CONTROL = Path('work/analysis/lil_B169_dispatches_v4214/all36_source_current_dispatches_FI5_FO2_and5_control_leaves.json')
NAMES = Path('work/analysis/lil_B169_names_v4217/twelve_original_name_consumers_and_owned_scratch_paths.json')
OLDER = Path('work/analysis/lil_B122_B127_terms_v3267/clean_current_items_Spirit_static_actors_and_related_terms.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    source, control, names, older = map(read, [SOURCE,CONTROL,NAMES,OLDER])
    image, clean = NdsImage.open(source['current_ROM']), NdsImage.open('work/clean.nds')
    help_raw = image.read_file('/COMMON/HELP.DK4')
    current_help, clean_help = [IlnkContainer.parse(im.read_file('/COMMON/HELP.DK4')).blocks for im in [image, clean]]
    skill = Path('translations/skill_terms_help_release_v1.json')
    assert sha(help_raw) == read(skill)['target_HELP_sha256']
    topics = []
    for ident, title in [(4,'Proof of Conquest'),(12,'Tavern'),(80,'Ruins / Church (Cities)'),(189,'Subordinate')]:
        raw, target = clean_help[ident], current_help[ident]
        source_title = raw.split(b'\0',1)[0].decode('cp932')
        target_title = target.split(b'\0',1)[0].decode('cp932')
        assert target_title == title
        if ident == 4:
            assert source_title == '覇者の証' and b"treasure proving its owner's supremacy" in target
        if ident == 189:
            assert b'Proof of Conquest' in target
        topics.append(dict(topic_id=ident,clean_title=source_title,current_title=target_title,
            clean_complete_title_hex=raw[:raw.index(0)+1].hex(),current_complete_title_hex=target[:target.index(0)+1].hex(),
            clean_topic_sha256=sha(raw),current_topic_sha256=sha(target),
            current_Proof_full_title_literal_offsets=[at for at in range(len(target)) if target.startswith(b'Proof of Conquest',at)]))
    faction = Path('translations/faction_help_manuscript_v1.json')
    row = next(row for row in read(faction)['records'] if row['id'] == 'HELP_TOPIC_189')
    assert all(row['review'].values()) and 'Proof of Conquest' in row['english']
    assert 'established Proof of Conquest term' in row['localization_note']
    binding_path = Path(control['registered_catalog_binding'])
    binding = read(binding_path)
    catalog = {bytes.fromhex(row['key_hex']):row for row in binding['records'] if row['route_mask'] & 4}
    current_blocks, clean_blocks = [IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]]
    variants = []
    for item in older['existing_completed_Proof_terminology_variants']:
        path = Path(item['final_review'])
        final = read(path)
        assert sha(path.read_bytes()) == item['final_review_sha256']
        old = next(row for row in final['records'] if row['id'] == item['id'])
        ref, raw = old['integrated_reference'], bytes.fromhex(old['integrated_hex'])
        block = current_blocks[old['block']]
        assert block[ref['offset']:ref['offset'] + len(raw)] == raw and block[ref['offset'] + len(raw)] == 0
        jp = bytes.fromhex(old['source_hex'])
        sa = old['source_reference']['offset']
        assert clean_blocks[old['block']][sa:sa + len(jp)] == jp
        replacement = catalog.get(raw[1:])
        effective = bytes.fromhex(replacement['target_hex']) if replacement else raw[1:]
        paragraph = ' '.join(unicodedata.normalize('NFKC',effective.decode('cp932')).split())
        variants.append({**item,current_complete_reference=ref,current_hex=raw.hex(),
            current_effective_paragraph=paragraph,current_registered_replacement=replacement is not None,
            clean_full_form_japanese_present='覇者の証' in jp[1:].decode('cp932')})
    assert any('Proof of Supremacy' in row['current_effective_paragraph'] for row in variants)
    assert any('Proof of Conquest' in row['current_effective_paragraph'] for row in variants)
    assert names['approved_prose_names']['21'] == 'Ian' and names['progressive_nameplate_values']['76'] == 'Mikhail Letzel'
    ROOT.mkdir(parents=True)
    save(ROOT / 'current_Proof_title_Tavern_ruins_names_and_older_variant_refs.json', dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_HELP_sha256=sha(help_raw),current_HELP_topics=topics,
        current_reviewed_faction_HELP189= row,exact_existing_story_Proof_variants=variants,
        B169_full_title='Proof of Conquest',B169_abbreviated_form='Proof or Proofs when source abbreviates',
        title_decision_reason='Use current Help4 title and reviewed Help189 term for the new quest explanation. Preserve source supremacy/strongest-power description without inventing military-only conquest, numeric thresholds or an immediate reward. Earlier Supremacy/Conquest variation remains open for separate exact-record reconciliation; no silent older edit.',
        B169_naturalist_title_flattery_preserved_without_inventing_PhD_Professor_or_rank=True,
        source_Mikhail_Letzel_printed_name_preserved_without_catalogue_Volk_insertion=True,
        source_seven_treasures_seven_sages_maps_of_various_shapes_legend_and_unknown_details_preserved=True,
        source_clue_versus_Proof_distinction_tentative_evil_holder_defeat_and_ruins_task_preserved=True,
        source_tavern_women_information_daily_worldwide_visitors_give_and_take_without_gift_price_or_romance_invention=True,
        older_Proof_consistency_lead_still_open_and_separate_from_later_technical_reaudit=True,
        no_completed_record_reopened_renamed_recounted_or_changed=True,new_actual_gameplay_or_UI_body_calls=0,
        evidence={str(path):sha(path.read_bytes()) for path in [SOURCE,CONTROL,NAMES,OLDER,skill,faction,binding_path,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('B169 terms bind Help4 Proof of Conquest,reviewed Help189,Tavern andruins;older Supremacy/Conquest records retained as an exact open lead. No older edit orcredit.')
