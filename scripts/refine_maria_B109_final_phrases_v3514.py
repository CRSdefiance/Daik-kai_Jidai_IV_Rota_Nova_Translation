"""Preserve three complete source meanings in automatically wrappable prose."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/maria_B109_final_phrases_v3514')
    old=Path('translations/maria_B109_editorial_manuscript_v5.json')
    new=Path('translations/maria_B109_editorial_manuscript_v7.json')
    assert not root.exists() and not new.exists()
    doc=deepcopy(read(old));changes=[]
    edits={
        25:("...Ming was a great maritime power. Zheng He led a vast fleet of junks across the Indian Ocean to distant Africa.",
            "The past tense preserves the former maritime power. The vast junk fleet, Zheng He's leadership, Indian Ocean crossing and distant African destination remain explicit. This complete sentence avoids splitting maritime power or all the way; no manual break or semantic exemption is used."),
        28:("The maritime ban eroded seamanship and ended trade. New powers in Western Europe threaten to plunder Asia's wealth...",
            "New powers in Western Europe preserves the newcomer countries and their location. Declining seamanship, ended trade, and the threat rather than accomplished plunder of Asia's wealth remain explicit. Only clause phrasing changes."),
        45:("You all know how the great powers keep sending one fleet after another for trading profits.",
            "Keep sending one fleet after another preserves continuous successive fleets; for trading profits preserves the purpose. The crew's shared knowledge and great powers remain explicit. No event, motive or outcome is added.")}
    for r in doc['records']:
        i=r['source_record_index']
        if i not in edits:continue
        words,note=edits[i];before=r['english'];r['english']='{SPEAKER:03}'+words
        r['localization_note']+=' '+note;r.pop('compiled_hex',None)
        r.update(prose_refinement_producer=str(Path(__file__)),prose_refinement_producer_sha256=sha(Path(__file__).read_bytes()))
        changes.append(dict(id=r['id'],source_Japanese=r['source_Japanese'],before=before,after=r['english'],reason=note))
    assert len(changes)==3
    doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()))
    save(new,doc)
    pairs=[]
    for src,dst,edits in [
        ('scripts/plan_maria_B109_layout_v3512.py','scripts/plan_maria_B109_layout_v3514.py',[
            ('maria_B109_layout_v3512','maria_B109_layout_v3514'),
            ('editorial_manuscript_v5.json','editorial_manuscript_v7.json'),
            ('editorial_manuscript_v6.json','editorial_manuscript_v8.json')]),
        ('scripts/verify_maria_B109_fonts_v3513.py','scripts/verify_maria_B109_fonts_v3515.py',[
            ('maria_B109_fonts_v3513','maria_B109_fonts_v3515'),
            ('editorial_manuscript_v6.json','editorial_manuscript_v8.json'),
            ('current_original_macro_alignment_calls=208,','current_original_macro_alignment_calls=208,macro_count_includes_hash_bound_prior_cases=True,')])]:
        a,b=Path(src),Path(dst);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in edits:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
        pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    root.mkdir(parents=True)
    save(root/'three_complete_meaning_phrase_successors.json',dict(previous_manuscript=str(old),previous_sha256=sha(old.read_bytes()),manuscript=str(new),manuscript_sha256=sha(new.read_bytes()),changes=changes,tools=pairs,all_prior_artifacts_preserved=True,no_manual_breaks_or_warning_exemptions=True,no_ROM_or_registry_mutation=True,review_credit_added=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
