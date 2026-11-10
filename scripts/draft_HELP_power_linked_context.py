"""Seal the two complete linked stat articles before reading their current English bodies."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
DATA={181:dict(heading='Faction Info',
    english='Select a faction on the Route Map to view its information. See [[184|Power]], [[182|Base]], [[190|Friendliness]] and [[185|Relations]].',
    meaning='Selecting a faction onthe route map displays itsdata. Four source destinations arepower,base,friendliness andrelationship,inthat order.',
    note='Keep the selected faction generic;it neednot be theplayer faction. Base/Friendliness/Relations labels areprovisional until existing Help headings arebound.'),
184:dict(heading='Power (Faction Data)',
    english="Power measures a faction's strength in the displayed sea region. It increases as the faction's [[150|Market Share]] grows, when it wins battles against other factions, and when it discovers ruins or other sites.",
    meaning='Power isfaction size inthe displayed sea region. It rises fromincreased townshare,victory against otherfactions anddiscoveringruins etc.',
    note='Displayed region isnot necessarily theplayer currentlocation. Preserve allthree growth causes;do not invent shipcount,money,friendliness or a formula.')}

if __name__=='__main__':
    output=ROOT/'T181_T184_clean_meanings_independent_drafts_v1.json';assert not output.exists()
    source_path=ROOT/'clean_HELP_source_packet_v2.json';source=load(source_path);rows=[]
    for original in source['records']:
        if original['topic_id'] not in DATA:continue
        value=DATA[original['topic_id']]
        rows.append(dict(**original,independent_heading_draft=value['heading'],independent_English_draft=value['english'],
            faithful_source_meaning=value['meaning'],localization_note=value['note'],
            current_heading_previously_consulted_as_UI_term=True,current_body_unconsulted_before_this_draft=True,
            independent_draft_claim_applies_to_body_not_UI_heading=True,current_comparison_pending=True,new_credit=0))
    assert len(rows)==2
    save(output,dict(format='dk4-clean-help-linked-articles-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_packet=str(source_path),source_packet_sha256=sha(source_path.read_bytes()),records=rows,
        reason='Resolve theearly protagonist bonuses together withtheir complete stat definition andindex.',new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Sealed two complete clean meanings/body drafts;existing UI headings wereknown,older bodies notconsulted.')
