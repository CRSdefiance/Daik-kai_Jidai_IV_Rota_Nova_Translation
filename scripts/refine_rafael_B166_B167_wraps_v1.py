"""Bind visual wrap findings to their exact source, current and prose records."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B166_B167_ordinary_v1 import ROOT

OUT = ROOT/'ordinary_visual_preferences_v2.json'
FORMATTING = ROOT/'ordinary_formatting_manuscript_v4.json'
PRIOR = ROOT/'ordinary_FE_reserve_v5.json'
FINDINGS = {
    (166,35): (['Mind if I wait outside?'], 'Keep Claudio’s whole request together.'),
    (166,39): (["it's all right"], 'Keep Rafael’s concession intact.'),
    (166,85): (['Proofs of Conquest','Portuguese Crown'], 'Put the Pope’s response on page two after the complete condition.'),
    (166,100): (['King of Portugal','trading spheres'], 'Keep the title and the object of the appointment together.'),
    (166,201): (['some kind of'], 'Keep Claudio’s tentative qualifier together.'),
    (166,219): (['back to Athens','right?'], 'Keep the destination phrase and preserve the question tag.'),
    (166,459): (['putting on a show'], 'Keep the predicate together in Claudio’s stammered protest.'),
    (166,541): (['out here'], 'Keep the location phrase together.'),
    (166,555): (["Weren't they",'in front of a crowd'], 'Keep the question opening and crowd phrase together.'),
    (166,617): (['Why do you'], 'Avoid leaving the question word at the end of the previous clause.'),
    (166,642): (["I'm counting on you"], 'Keep Rafael’s full reassurance together.'),
    (166,695): (["can't afford to miss"], 'Keep the phrase that recalls the eavesdropping joke.'),
    (166,726): (['get some rest'], 'Keep Rafael’s invitation to rest together.'),
    (166,731): (["another country's expedition"], 'Keep the competitor’s identity together.'),
    (166,818): (['is clear, at least'], 'Avoid stranding the short concession on its own row.'),
    (166,869): (['studied Portuguese','did her best'], 'Keep the language and effort with their verbs.'),
    (167,25): (['wherever you please'], 'Keep the dismissive phrase together.'),
    (167,54): (["bright side, aren't you?"], 'Keep the tag beside the phrase it qualifies.'),
    (167,63): (['a guy like that'], 'Keep Claudio’s subject phrase together.'),
    (167,74): (['Come on'], 'Keep the idiomatic call together.'),
    (167,95): (['sure of himself'], 'Keep Claudio’s sarcastic observation intact.'),
    (167,166): (['hat in hand'], 'Keep Julio’s idiom together.'),
    (167,180): (['on our side'], 'Keep the alliance phrase together.'),
    (167,192): (["you're so proud of"], 'Keep the taunt’s modifier intact.'),
    (167,207): (["don't push yourself"], 'Keep Claudio’s feigned concern in one phrase.'),
    (167,214): (["what's your name?"], 'Keep Claudio’s question together.'),
}


def main():
    assert not OUT.exists()
    prefs,doc=map(load,(PRIOR,FORMATTING))
    byid={r['id']:r for r in doc['records']}
    for (block,index),(phrases,reason) in FINDINGS.items():
        ident=f'DK4_MES_B{block}_R{index:04d}'
        row=byid[ident]
        prefs['records'][ident]=dict(line_phrases=phrases,reason=reason,
            bindings={k:sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
    prefs['records']['DK4_MES_B166_R0085']['page_clause']="he'll press for the authority of the Portuguese Crown to be recognized again."
    prefs['initial_viewed_plan']=str(ROOT/'ordinary_plans_v7/automatic_plans.json')
    prefs['initial_viewed_plan_sha256']=sha(Path(prefs['initial_viewed_plan']).read_bytes())
    save(OUT,prefs)
    print(f'{len(FINDINGS)} source-bound visual wrap findings prepared.')


if __name__=='__main__':
    main()
