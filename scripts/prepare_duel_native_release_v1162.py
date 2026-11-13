"""Approve bounded native formatting and prepare final33 payload, not gameplay."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import duel_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.duel_editorial_layout_v1155 import IDS, ESCAPE_IDS, PROFILE, compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_native_release_v1162')
OLD = Path('translations/duel_editorial_manuscript_v3.json')
NEW = Path('translations/duel_editorial_manuscript_v4.json')
ROM = Path('out/all_routes_combined_v1105_candidate.nds')


def main():
    assert not ROOT.exists() and not NEW.exists() and not owned.COMPONENT.exists()
    old = read(OLD)
    checkpoint_path = Path('work/analysis/duel_resident_checkpoint_v1161/checkpoint.json')
    checkpoint = read(checkpoint_path)
    for value in checkpoint['completed_proofs'].values():
        assert sha(Path(value['path']).read_bytes()) == value['sha256']
    visual = read(checkpoint['visual_review'])
    assert not visual['visual_review_pending']
    assert sha(Path(checkpoint['visual_review']).read_bytes()) == checkpoint['visual_review_sha256']
    sources = {key: value['path'] for key, value in checkpoint['completed_proofs'].items()}
    resident, escape = read(sources['resident_fonts']), read(sources['escape_fonts'])
    assert len(resident['cases']) == 1356 and len(escape['cases']) == 1417
    rows = {r['message_id']: r for r in old['records']}
    assert tuple(rows) == IDS
    controls = {}
    sample = rows[1931]
    invalid = {
        'pregenerated_break': {'english': "So you're %s!\nLet's duel!"},
        'leading_alignment': {'english': " So you're %s! Let's duel!"},
        'double_alignment': {'english': "So  you're %s! Let's duel!"},
        'tab_control': {'english': "So you're\t%s! Let's duel!"},
        'translation_markup': {'english': "So you're %s!{LB}Let's duel!"},
        'CP932_authored_English': {'english': "Ｆight me, %s!"},
        'macro_IC': {'english': 'IC challenge %s!'},
        'macro_FI': {'english': 'FI challenge %s!'},
        'stray_percent': {'english': '%s has 5% of them!'},
        'missing_argument': {'english': "Let's duel!"},
        'duplicated_argument': {'english': '%s and %s!'},
        'wrong_conversion': {'english': '%d!'},
        'wrong_declared_argument_count': {'native_argument_count': 0},
        'wrong_family': {'source_family': 'acceptance'},
        'wrong_ID': {'message_id': 1980},
        'oversized_duel_paragraph': {'english': '%s '+'A'*100},
    }
    for label, fields in invalid.items():
        try:
            compiled({**sample, **fields})
        except ValueError:
            controls[label] = True
        else:
            raise AssertionError(label)
    rom = NdsImage.open(ROM)
    assert sha(ROM.read_bytes()) == '64b1da09fe0f75007af73b0f44a39ce9d2d3c6dedbb70cf6c0ca20223a7f1c29'
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    before = owned.previous_entries(common, arm)
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    accepted = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    doc = deepcopy(old)
    doc.update(consumer_layout_profile=PROFILE, formatting_review_pending=False,
        status='33-native-format-approved;registered-combined-ROM-and-original-duel-scenes-pending',
        current_ROM=str(ROM), current_ROM_sha256=sha(ROM.read_bytes()),
        current_COMMON_sha256=sha(common), current_ARM9_sha256=sha(arm),
        supersedes_manuscript=str(OLD), supersedes_manuscript_sha256=sha(OLD.read_bytes()),
        resident_font_proof=sources['resident_fonts'], resident_font_proof_sha256=sha(Path(sources['resident_fonts']).read_bytes()),
        escape_font_proof=sources['escape_fonts'], escape_font_proof_sha256=sha(Path(sources['escape_fonts']).read_bytes()),
        native_runtime_proof=sources['escape_runtime'], native_runtime_proof_sha256=sha(Path(sources['escape_runtime']).read_bytes()),
        visual_review=checkpoint['visual_review'], visual_review_sha256=checkpoint['visual_review_sha256'])
    for row in doc['records']:
        n = row['message_id']
        row['canonical_source_hex'] = accepted[n].text.hex()
        row['current_reference'] = {k: v for k, v in asdict(before[n]).items() if k != 'text'}
        row['current_text_hex'] = before[n].text.hex()
        row['current_English'] = before[n].text.decode('cp932')
        row['compiled_hex'] = compiled(row).hex()
        row['review']['formatting'] = True
        row['status'] = 'native-consumer-approved;original-gameplay-and-transitions-pending'
        row['formatting_note'] = ('One paragraph until original macro expansion. Distinct original duel24x3 consumer; '
            'all1356 unique expansions have complete native font planes and original crops, with an exact scoped existing-cache PIC component.'
            if n not in ESCAPE_IDS else 'Compiler-owned speech state and one paragraph before the original speech macro/wrap consumer; '
            'all1417 shared escape-name cases have complete228x64 native font planes and uniform margins. Actual defeat branch/transition remains pending.')
        if n == 1954:
            row['qa_waivers'] = ['weak_line_end']
            row['qa_waiver_reason'] = visual['contextual_weak_word_warning_retained']['decision']
    validate_natural_dialogue_batch(doc)
    compiler = read('work/analysis/duel_layout_native_v1141b/compiler_provenance.json')
    component = Path(compiler['binary']).read_bytes()
    assert sha(component) == owned.COMPONENT_SHA
    owned.COMPONENT.parent.mkdir(parents=True, exist_ok=True)
    owned.COMPONENT.write_bytes(component)
    ROOT.mkdir(parents=True)
    save(NEW, doc)
    c, a, proof = owned.plan(common, arm, doc)
    common_path, arm_path = ROOT/'target_COMMON.bin', ROOT/'target_ARM9.bin'
    common_path.write_bytes(c)
    arm_path.write_bytes(a)
    save(ROOT/'final_payload_plan.json', {**proof, 'source_ROM': str(ROM), 'source_ROM_sha256': sha(ROM.read_bytes()),
        'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
        'target_COMMON': str(common_path), 'target_ARM9': str(arm_path),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a),
        'new_code_prefix': {'block': 21, 'component_bytes': 1480, 'component_sha256': owned.COMPONENT_SHA},
        'manuscript': str(NEW), 'manuscript_sha256': sha(NEW.read_bytes()),
        'compiler_rejection_controls': controls,
        'all33_prose_and_source_glosses_exact_to_reviewed_v3': True,
        'native_formatting_approval_is_not_gameplay_or_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('33 native formatting approvals; final one-paragraph payload and scoped runtime prepared. Copies/registration/build/actual remain pending.', flush=True)


if __name__ == '__main__':
    main()
