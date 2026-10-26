"""Generate a bound delta verifier; unchanged native cases retain provenance."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

OLD = Path('scripts/verify_lil_shrines_fonts_v3179.py')
NEW = Path('scripts/verify_lil_shrines_fonts_v3183b.py')
ROOT = Path('work/analysis/lil_Shrines_Temples_delta_tools_v3183')

if __name__ == '__main__':
    assert not NEW.exists() and not ROOT.exists()
    text = OLD.read_text(encoding='utf-8')
    for old, new in [
        ('lil_Shrines_Temples_fonts_v3179', 'lil_Shrines_Temples_fonts_v3183b'),
        ('lil_shrines_temples_editorial_manuscript_v3.json', 'lil_shrines_temples_editorial_manuscript_v5.json'),
        ('lil_shrines_temples_actor_style_manuscript_v2.json', 'lil_shrines_temples_actor_style_manuscript_v3.json'),
        ('lil_shrines_temples_layout_v1', 'lil_shrines_temples_layout_v2')]:
        assert old in text
        text = text.replace(old, new)
    anchor = '    cases=[];qa_reports=[];pictures=[];macro_calls=0'
    assert text.count(anchor) == 1
    text = text.replace(anchor, """    priorpath=Path('work/analysis/lil_Shrines_Temples_fonts_v3179/current_macro_QA_and_progressive_font_proof.json')
    prior=read(priorpath)
    assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['ARM9_sha256']==sha(arm) and prior['COMMON_sha256']==sha(common)
    for key,hashkey in [('manuscript','manuscript_sha256'),('actor_style_manuscript','actor_style_manuscript_sha256'),('scoped_profile','scoped_profile_sha256'),('native_formatter_module','native_formatter_module_sha256')]:
        assert sha(Path(prior[key]).read_bytes())==prior[hashkey]
    assert prior['scoped_profile']==doc['scoped_profile_module'] and prior['scoped_profile_sha256']==doc['scoped_profile_module_sha256']
    prior_rows={r['id']:r for path in [prior['manuscript'],prior['actor_style_manuscript']] for r in read(path)['records']}
    prior_cases={r['id']:r for r in prior['cases']}
    reused=0;changed=[]
""" + anchor)
    anchor = "        if row['kind']=='system-FE':continue"
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + """
        oldrow,oldcase=prior_rows[row['id']],prior_cases[row['id']]
        for key in ['block','current_hex','source_reference','current_reference','kind']:
            assert row[key]==oldrow[key],(row['id'],key)
        original_source=row.get('source_stored_alternative_hex',row['source_hex'])
        assert original_source==oldrow['source_hex']
        caption=('D0 styles'+str(row['style_indices'])) if row['kind']=='typed-4100-actor-style-alternative' else 'selector'+row['source_presentation_prefix_hex']
        if row['english']==oldrow['english'] and result.encoded.hex()==oldcase['encoded_hex']:
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            cases.append({**oldcase,'reused_current_native_case':True,'reused_proof':str(priorpath),'reused_proof_sha256':sha(priorpath.read_bytes())})
            pictures.append((row['id'],caption,Image.open(oldcase['preview']).convert('RGB')))
            macro_calls+=8;reused+=1;continue
        changed.append(row['id'])
""")
    anchor = "    negatives=[]"
    assert text.count(anchor) == 1
    text = text.replace(anchor, """    assert set(changed)=={'DK4_MES_B101_R0072','DK4_MES_B108_R0030','DK4_MES_B109_R0266'} and reused==187,(changed,reused)
""" + anchor)
    anchor = '        current_original_macro_alignment_calls=1520,'
    assert text.count(anchor) == 1
    text = text.replace(anchor, """        newly_executed_font_cases=190-reused,reused_unchanged_font_cases=reused,
        newly_executed_current_macro_alignment_cases=(190-reused)*8,reused_current_macro_alignment_cases=reused*8,
        reused_proof=str(priorpath),reused_proof_sha256=sha(priorpath.read_bytes()),changed_IDs=changed,
""" + anchor)
    text = text.replace("print('190current progressive planes/1520macro alignments/220QA plans/31source-scope negatives pass;24sheets need visual review. ThirtyFE/fifteen three-choice labels/reference/release gates pending.')",
        "print('190current progressive planes:3new/187bound reused;24new/1496reused macro cases. All220QA/31negatives pass;changed sheets need visual review. Three-choice/release gates pending.')")
    NEW.write_text(text, encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT/'delta_verifier_provenance.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),no_executed_predecessor_modified=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
