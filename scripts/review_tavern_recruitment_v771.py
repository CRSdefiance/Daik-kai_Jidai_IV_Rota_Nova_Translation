"""Natural English from verified recruitment and town-condition contexts."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.recruitment_runtime_research_v771 import STATUS_PHRASES,STATUS_SUFFIX
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_recruitment_editorial_v771')
MANUSCRIPT=Path('translations/recruitment_editorial_manuscript_v2.json')
TEXT={
883:"Admiral, we don't have enough money.",
884:"Admiral, it looks like we're short on money.",
885:"Um... Admiral, we don't have enough money.",
886:"Admiral, we're short on cash.",
887:"We don't have the money, Admiral.",
888:"Admiral, we don't have enough money!",
889:"Admiral, we're short on funds...",
890:"I'll recruit sailors for %s gold.",
891:"I'll recruit some sailors for %s gold.",
892:"I'll spend %s gold to recruit sailors.",
893:"I'll find us some sailors for %s gold.",
894:"I'll spend %s gold recruiting sailors.",
895:"I'll find some sailors for %s gold.",
896:"I'll use %s gold to recruit sailors.",
897:"Who wants to sail with the Admiral?",
898:"Who'll join the Admiral's crew?",
899:"Step forward if you'd like to sail with the Admiral!",
900:"Anyone here want to sail with the Admiral?",
901:"Who'll sail with the Admiral?",
902:"Want to join the Admiral's crew? Step forward!",
903:"Anyone for the Admiral's crew?",
904:"We've got %s willing to join.",
905:"I hear %s has been experiencing %s lately.",
906:"Word is, %s's been going through %s lately.",
907:"Aye!",
}
GLOSS={
883:'Addresses the admiral and states there is not enough money.',
884:'Addresses the admiral and conversationally says there seems to be insufficient money;the ending is not a gender claim.',
885:'Hesitantly addresses the admiral and reports insufficient money.',
886:'Casually and emphatically tells the admiral there is not enough money.',
887:'An older speaker tells the admiral there is not enough money.',
888:'A young/familiar voice calls to the admiral and complains that there is not enough money.',
889:'Politely addresses the admiral and trails off while noting insufficient funds.',
890:'The officer says they will gather sailors for the specified gold cost,politely.',
891:'The officer casually says they will gather sailors for the specified gold cost.',
892:'The officer warmly says they will spend the specified gold amount to gather sailors.',
893:'The officer confidently says they will spend the specified gold amount to gather sailors,with rough conversational emphasis.',
894:'The officer decisively says they will spend the specified gold amount to gather sailors.',
895:'The young/familiar officer casually says they will gather sailors for the specified gold cost.',
896:'The officer politely says they will spend the specified gold amount to gather sailors.',
897:'Calls for anyone who wants to board the admiral\'s ship.',
898:'Asks who wants to board the admiral\'s ship,as an emphatic recruiting call.',
899:'Politely commands anyone who wants to board the admiral\'s ship to step forward or identify themselves.',
900:'Roughly calls out asking whether anyone here wants to board the admiral\'s ship.',
901:'An older speaker invitingly asks whether anyone wants to board the admiral\'s ship.',
902:'Calls for people who want to board the admiral\'s ship to come forward.',
903:'Politely calls out asking whether anyone wants to board the admiral\'s ship.',
904:'Reports that the supplied number of people have gathered in response to recruiting.',
905:'Politely reports hearsay that a named town has recently been experiencing a major instance of the supplied condition.',
906:'Casually reports hearsay that a named town has recently been experiencing quite an instance of the supplied condition.',
907:'An enthusiastic short acknowledgement,following the call for volunteers in this original scene.',
}
RETAINED={883,886,889,897,898,899,901,902,903}
ARGUMENTS={**{n:['native_gold_cost'] for n in range(890,897)},904:['native_number_gathered'],
    905:['town_name','native_city_status_label'],906:['town_name','native_city_status_label']}


def main():
    packet=read(ROOT/'source_and_neighbors.json');context=read(ROOT/'native_context.json')
    assert len(context['original_rumor_and_interjection_fragments'])==2737
    assert len(context['original_role_call_core_bindings'])==4
    records=[]
    for old in packet['rows']:
        n=old['id']
        if n not in TEXT:continue
        if 883<=n<=889:
            speaker='Officer assigned to original role1; eight-voice table021183A0 with voice1 fallback'
            scene='Original5745C..57464 insufficient-funds path. Original53D44 resolves the role1 officer and chooses this complete independent alternative; core mode0,parent53DB8.'
            note='Keep the admiral address,insufficient-money fact and source voice. Use natural American English without artificial elderly syntax or adding a family relationship.'
        elif 890<=n<=896:
            speaker='Officer assigned to original role1; eight-voice cost table02118380 with voice1 fallback'
            scene='Original57470..57484 formats the actual recruitment cost using ABF50. Original53CB0 resolves role1 and selects this independent Yes/No cost statement; parent53D24. This is recruitment,not the earlier round-purchase cost.'
            note='Restore a complete first-person recruitment plan and preserve the original fullwidth number. Gold is a mass noun for every amount. The source statement is followed by Yes/No UI;do not invent an extra spoken question or a promised recruit count.'
        elif 897<=n<=903:
            speaker='Officer assigned to original role1; eight-voice recruiting-call table02118360 with voice1 fallback'
            scene='Original575B4..575BC invokes the role1 invitation once at the first recruiting attempt. The crowd907 acknowledges it;904 then reports the number gathered. These seven voices are alternatives,not successive sentence fragments.'
            note='Retain the complete admiral/ship/crew invitation and any explicit step-forward command. Most V627 localization already reads naturally.900 uses an idiomatic rough call without implying repeated unsuccessful recruiting.'
        elif n==904:
            speaker='Officer assigned to original role1; direct numeric-ID role wrapper53DCC'
            scene='Original575DC..575F0 passes the number gathered from R9 through ABF50 to original53DCC(role1,904,number). Core mode0,parent53E38;the saved R1 word is numeric904,not a voice-table pointer. Assign Sailors follows later.'
            note='Report willingness/count in the recruitment context,without implying completed ship assignments. A numeric direct object in We\'ve got %s willing to join is natural after the invitation and works for one or many,without a new pluralization runtime or invented quota.'
        elif n in(905,906):
            speaker='Original Tavern NPC/current-town role13'
            scene='Original578F4 filters all114 town objects by its native virtual+10 eligibility flag,same region and status<12. Original579D0..57A14 supplies town name first and B2D58 status label second. Context+8 selects polite905 or casual906; Normal12 is excluded.'
            note='Preserve hearsay,recency and the source severity emphasis in complete condition phrases. Positive economic booms remain positive. Localize the typed final status field after original printf,including its article: a serious shortage of luxury goods reads naturally,unlike a major luxury shortage. Preserve town-name capitalization,all original UI labels and provider outputs. Normal is source-ineligible and falls through unchanged.'
        else:
            speaker='Original crowd/Patron NPC resolved from current town and role13'
            scene='Original575C0..575D0 displays907 immediately after the first role1 recruiting invitation,and before the officer reports the number gathered. It is independent of905/906 town rumors.'
            note='Use the nautical affirmative Aye! for the crowd\'s enthusiastic acknowledgement. Whoa! suggests surprise or a request to stop,which is misleading in this invitation/response context.'
        english=TEXT[n]
        assert english==' '.join(english.split()) and english.isascii()
        assert english.count('%s')==len(ARGUMENTS.get(n,[]))
        if n in RETAINED:assert english==' '.join(old['current_English'].split())
        records.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'interaction_group':'Tavern-recruitment-voices-and-town-condition-rumors',
            'source_hex':old['source_hex'],'japanese':old['Japanese'],'source_reference':old['source_reference'],
            'canonical_source_hex':old['canonical_hex'],'current_text_hex':old['current_hex'],
            'current_English':old['current_English'],'current_reference':old['current_reference'],
            'english':english+'{PAD}','source_meaning':GLOSS[n],'speaker':speaker,'context':scene,'localization_note':note,
            'source_native_arguments':ARGUMENTS.get(n,[]),'English_argument_source_indices':list(range(len(ARGUMENTS.get(n,[])))),
            'decision':'retain' if n in RETAINED else 'revise','typed_status_phrase_expansion_after_printf':n in(905,906),
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            'status':'source-context-prose-reviewed-runtime-layout-gameplay-integration-pending'})
    assert len(records)==25 and sum(r['decision']=='revise' for r in records)==16
    save(MANUSCRIPT,{'format':'dk4-common-entry-manuscript-v1','translation_policy':'natural-dialogue-v2',
        'encoder':'dialogue-fixed-v1','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],
        'file_path':'/COMMON/MESFILE.DK4','source_clean_COMMON_sha256':packet['pins'][0]['COMMON_sha256'],
        'source_canonical_COMMON_sha256':packet['pins'][1]['COMMON_sha256'],'source_pins':packet['pins'],
        'native_context_proof':str(ROOT/'native_context.json'),'native_context_proof_sha256':sha((ROOT/'native_context.json').read_bytes()),
        'typed_condition_phrases':[{**row,'English_phrase':phrase} for row,phrase in zip(context['all13_source_status_names_and_UI_labels'][:12],STATUS_PHRASES)],
        'typed_condition_suffix':STATUS_SUFFIX.decode(),
        'supersedes_unintegrated_research_draft':'translations/recruitment_editorial_manuscript_v1.json',
        'status':'research-draft-runtime-and-presentation-pending','records':records,
        'remaining_gates':['Scoped native role/table/ID dispatch and status-phrase ABI proof','Full substituted layout and independent font review',
            'Owned no-growth implementation and complete native copies','Registered integration/exact patch and actual scenes'],
        'full_goal_complete':False})
    print('25 source/context/prose-reviewed drafts:16 revisions,9 retained. Formatting/runtime/integration/gameplay gates remain open.',flush=True)


if __name__=='__main__':main()
