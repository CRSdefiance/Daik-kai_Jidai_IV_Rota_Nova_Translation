"""Keep We shall meet again together; reuse the other 22 exact native panels."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_hodram_B156_cinematic_English.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "ROOT=Path('work/analysis/Hodram_B156_cinematic_English_v2_20261102')":
        "ROOT=Path('work/analysis/Hodram_B156_cinematic_English_v3_20261102')\nPRIOR=Path('work/analysis/Hodram_B156_cinematic_English_v2_20261102/compiled_cinematic_pages.json')",
    "weak=int(not final and last in WEAK_LINE_ENDINGS)":
        "weak=int(not final and (last in WEAK_LINE_ENDINGS or (words[stop-1],words[stop])==('shall','meet')))",
    "    for row in doc['records']:":
        "    prior=load(PRIOR);assert prior['runtime']==ctx.receipt()\n    reuse={r['id']:r for r in prior['records']}\n    for row in doc['records']:",
    "        source=row['source_Japanese'];text=row['english'];heading=source.lstrip('\\n').startswith('＜')":
        """        if ident!='DK4_MES_B156_R0188':
            prior_row=reuse[ident]
            assert all(prior_row[k]==row[k] for k in ['source_hex','current_hex','source_reference','current_reference'])
            assert prior_row['logical_English']==row['english']
            for prefix in ['physical','logical']:
                assert sha(Path(prior_row['native'][prefix+'_plane']).read_bytes())==prior_row['native'][prefix+'_sha256']
            assert sha(Path(prior_row['preview']).read_bytes())==prior_row['preview_sha256']
            rows.append(prior_row);continue
        source=row['source_Japanese'];text=row['english'];heading=source.lstrip('\\n').startswith('＜')""",
    "        complete_native_macro_alignments=92,":
        "        previous_native=str(PRIOR),previous_native_sha256=sha(PRIOR.read_bytes()),exact_native_panels_reused=22,fresh_native_panels=1,complete_native_macro_alignments=92,",
    "for p in [INPUT,GEOMETRY,":
        "for p in [PRIOR,original,INPUT,GEOMETRY,",
    "print('23 cinematic English pages/92 macro alignments pass native checks; individual source staging retained. Two new sheets require direct visual review; stored/gameplay/release gates pending.')":
        "print('One cinematic phrase reflowed and native-checked;22 unchanged native panels reused. One fresh page needs direct review; stored/gameplay/release gates pending.')",
})
exec(compile(source,__file__+'::one-source-bound-phrase-reflow-with-exact-proof-reuse','exec'),globals())
