"""Resolve two ordinary-name orphans with faithful idiomatic prose, not padding."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_prose_v1332')
OLD = Path('translations/ship_sinking_editorial_manuscript_v1.json')
OUT = Path('translations/ship_sinking_editorial_manuscript_v2.json')


def main():
    assert not ROOT.exists() and not OUT.exists()
    doc = deepcopy(read(OLD))
    fonts_path = Path('work/analysis/ship_sinking_fonts_v1331/native_font_proof.json')
    fonts = read(fonts_path)
    actual = [r for r in fonts['findings'] if r['name_case']['kind']=='original-live-ship-getter']
    assert [r['message_id'] for r in actual]==[2068,2073]
    changes = {
        2068:("Admiral! We've sent the enemy ship %s to the bottom!",
              'Use the idiomatic naval phrase sent to the bottom for sinking the enemy ship. Preserve the excited address,our agency and the specific vessel. The sentence is expanded naturally rather than truncated or manually positioned;it also avoids stranding the ordinary ship name.'),
        2073:('The enemy ship %s has been sunk!',
              'A complete passive report is natural formal English for the original emphatic sinking announcement. The preceding original projectile path establishes our shot as the cause;the passive adds no new agent or outcome. It avoids an artificially expanded We have prefix and leaves the ship name within the sentence.')}
    for row in doc['records']:
        if row['message_id'] in changes:
            row['english'],row['localization_note'] = changes[row['message_id']]
            row['editorial_decision'] = 'revise'
            row['review']['formatting'] = False
            row['status'] = 'source-context-prose-rereviewed;new-native-fonts-name-bound-release-gameplay-pending'
    doc.update(revised=5,retained=11,supersedes_manuscript=str(OLD),supersedes_manuscript_sha256=sha(OLD.read_bytes()),
        ordinary_name_wrap_findings=str(fonts_path),ordinary_name_wrap_findings_sha256=sha(fonts_path.read_bytes()),
        all6_V1331_sheets_actually_visually_reviewed=True,
        source_meaning_and_voice_rereviewed_after_native_findings=True,
        remaining_synthetic_name_findings_require_supported_editor_bound_and_layout_review=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    assert sum(r['editorial_decision']=='revise' for r in doc['records'])==5
    save(OUT,doc)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_prose_revisions.json',{'original_manuscript':str(OLD),'original_sha256':sha(OLD.read_bytes()),
        'successor_manuscript':str(OUT),'successor_sha256':sha(OUT.read_bytes()),
        'ordinary_name_findings':actual,'all6_sheets_visually_reviewed':fonts['sheets_for_required_visual_review'],
        'old_native_proof_preserved_new_native_proof_required':True,
        'no_authored_padding_or_breaks_no_completed_or_new_source_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('2068/2073 rereviewed against Japanese and revised naturally;v1/native findings preserved. New native proof required.',flush=True)


if __name__=='__main__':
    main()
