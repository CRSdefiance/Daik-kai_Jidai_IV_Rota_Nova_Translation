"""Reconstruct only the two complete reviewed Rafael blocks for stored and gameplay checks."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.rebuild_rafael_B141_B160_reviewed_v1 import source as previous
from scripts.seal_rafael_B166_B167_offline_display_v1 import OUT, CURRENT
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/rebuild_reviewed_editorial_batch_v4.py')
source=checked_text(previous,{
    "len(doc['records'])==557":"len(doc['records'])==186",
    "==len(native['records'])==549":"==len(native['records'])==186",
    '==(549,0,8)':'==(186,0,0)',
    'len(changed)==20':'len(changed)==2',
    'speech_count=549':'speech_count=186',
    'total_rendered_speech_count=549':'total_rendered_speech_count=186',
    'typed_choice_count=8,compound_objects=4':'typed_choice_count=0,compound_objects=0',
    'ordinary_speeches=549':'ordinary_speeches=186',
    'menu_labels=8,changed_blocks=20':'menu_labels=0,changed_blocks=2',
    'Rafael B141-B160 complete557-object source-bound reconstruction':
        'Rafael B166–B167 complete 186-speech source-bound reconstruction for native and gameplay QA',
    'args=parser.parse_args();assert not args.out.exists()':
        """args=parser.parse_args();assert not args.out.exists()
    visual=load(OUT/'visual_review.json')
    assert visual['all_body_and_name_sheets_directly_viewed'] and visual['body_pages']==187
    assert visual['native_sha256']==sha(args.native.read_bytes())
    assert Path(args.packet)==CURRENT""",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::two-source-bound-blocks-all-layout-controls-preserved','exec'),globals())
