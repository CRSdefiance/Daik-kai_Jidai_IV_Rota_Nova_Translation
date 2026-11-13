"""Preserve the stopped raw-only comparison and bind the actual registered R58 override."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_comparison_correction_v5783c')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/compare_lil_B199_exchange_v5783.py','scripts/compare_lil_B199_exchange_v5783b.py',{
        'lil_B199_comparison_v5783':'lil_B199_comparison_v5783b',
        "    rows=[]\n":"    binding_path=Path(dispatch['registered_catalog_binding']);binding=read(binding_path)\n    assert sha(binding_path.read_bytes())==dispatch['registered_catalog_binding_sha256']\n    rows=[];matched=[]\n",
        "        assert current['registered_catalog_match'] is None\n        expanded=body.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')":
        """        match=current['registered_catalog_match']
        effective=body
        entry=None
        if match is not None:
            assert r['source_record_index']==58 and match['route_mask']==4 and match['table_index']==305
            entry=binding['records'][305]
            assert entry['key_hex']==raw[1:].hex() and entry['route_mask']&4
            assert entry['requests']==[dict(owner=['/data/SC2.DK4',r['id']],form='body')]
            effective=bytes.fromhex(entry['target_hex']).decode('cp932')
            assert ' '.join(effective.split())==\"Camille! What are you doing? Come on, let's go!\"
            matched.append(r['id'])
        expanded=effective.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')""",
        "        paragraph=' '.join(body.split())":"        paragraph=' '.join(effective.split())",
        'row.update(previous_display_body=body,previous_paragraph=paragraph':
        'row.update(previous_raw_storage_body=body,previous_effective_template_body=effective,previous_registered_catalog_match=match,previous_registered_catalog_entry=entry,previous_display_body=effective,previous_paragraph=paragraph',
        '    ROOT.mkdir(parents=True)':'    assert matched==[\'DK4_MES_B199_R0058\']\n    ROOT.mkdir(parents=True)',
        '[SOURCE,GLOSS,ACTUAL,DISPATCH,CONTROLS,NAMES,NAME_FIELDS,CAPTION,Path(__file__)]':
        "[SOURCE,GLOSS,ACTUAL,DISPATCH,CONTROLS,NAMES,NAME_FIELDS,CAPTION,binding_path,Path('scripts/compare_lil_B199_exchange_v5783.py'),Path(__file__)]",
        'current_registered_catalog_matches=0':'current_registered_catalog_matches=1,registered_R58_effective_Camille_question_and_summons_previously_integrated=True',
        "print('31 source/current paragraphs reconciled;all31 Japanese panels observed,ten source sheets viewed. Project Rocco Alemkel retained;English layout/release pending.')":
        "print('31 source/runtime paragraphs reconciled;R58 existing catalog305 corrects Camille and restores question. All31 source panels observed;ten sheets viewed. English layout/release pending.')"})
    ROOT.mkdir(parents=True);save(ROOT/'correction_receipt.json',dict(derivation=result,
        earlier_raw_only_comparison_stopped_before_ROOT_or_prose_approval=True,
        exact_registered_R58_override_must_be_used_for_retention_decision=True,
        all_native_numeric_constants_preserved=True,no_ROM_or_review_credit=True))
