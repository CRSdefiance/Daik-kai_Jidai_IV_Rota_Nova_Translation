"""Successor recognizes the prior refined Deck View FE proof's distinct schema."""
from pathlib import Path

SOURCE = Path('scripts/checkpoint_lil_lessons_native_v1979.py')

if __name__ == '__main__':
    assert not Path('work/analysis/lil_lessons_native_checkpoint_v1979').exists()
    text = SOURCE.read_text(encoding='utf-8')
    old = "            assert sha(Path(case['logical_228x48_plane']).read_bytes()) == case['logical_plane_sha256']"
    new = """            if 'logical_228x48_plane' in case:
                assert sha(Path(case['logical_228x48_plane']).read_bytes()) == case['logical_plane_sha256']
            else:
                assert row['id'] == 'DK4_MES_B23_R0166'
                refined_FE_proof = Path(case['current_native_plane_proof'])
                refined = read(refined_FE_proof)
                assert refined['only_changed_id'] == row['id']
                assert refined['storage_target_hex'] == current.hex()
                assert refined['encoded_hex'] == encoded.hex()
                assert refined['captured_actual_FE_context_replayed_source12_to_display16_contract']
                assert all(r['complete_one_page_and_independent_plane_exact'] for r in refined['cases'])
                assert [r['label'] for r in refined['cases']] == ['compiled','parity_storage']
                assert sha(Path(refined['preview']).read_bytes()) == refined['preview_sha256']
                assert refined['preview_sha256'] == case['display_preview_sha256']"""
    assert text.count(old) == 1
    text = text.replace(old,new)
    changes = {
        'lil_lessons_native_checkpoint_v1979':'lil_lessons_native_checkpoint_v1979b',
        "evidence={str(p):sha(p.read_bytes()) for p in (DOC,MENU,OLD,OLD_FONT,OLD_FE,NEW_FONT,old_menu_path)}":
            "evidence={str(p):sha(p.read_bytes()) for p in (DOC,MENU,OLD,OLD_FONT,OLD_FE,NEW_FONT,old_menu_path,refined_FE_proof,SOURCE)}",
        'Allninecomplete FElogicalplanes/displaypreviews verified byhash andsource target bytes.':
            'Eightstoredlogicalplanes andallnineFEdisplaypreviews verified byhash andsource target bytes;refinedR0166 hasexact compiled/storage native-plane proof ratherthan astandalonebitmap path.',
        '- Alltest/build jobs terminal. Frozenfailed opening1976':
            '- Alltest/build jobs terminal. Frozen1979 rejected thehistorical refinedR0166 FEproof\'s distinct schema beforeoutputs;1979b validates itscompiled/storage native-plane proof explicitly. Frozenfailed opening1976',
    }
    for old,new in changes.items():
        assert old in text,old
        text = text.replace(old,new)
    # Escape apostrophes inside the generated single-quoted chapter string.
    text = text.replace("FEproof's distinct",'FEproof distinct')
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__,'SOURCE':SOURCE})
