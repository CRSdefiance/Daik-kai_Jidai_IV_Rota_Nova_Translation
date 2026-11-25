"""Original alliance/assistance and war methods; actual encounter selects the message."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_reinforcement_location_v1038 import apply_fixture as prior
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000


def apply_fixture(arm,raw,request):
    if request!={'reinforcement_context':'prepareAssistancePactAtFirstSight'}:return prior(arm,raw,request)
    after,receipt=prior(arm,raw,{'reinforcement_context':'approachOwn57'})
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x3C8F4,0x3CB30),(0x3C740,0x3C748),(0x3CFC8,0x3CFEC),
                  (0x773D8,0x77E68),(0x3CB30,0x3CBF0)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,after);companies=get(0xCB160)
    player=companies+4+2*76;ally=companies+4+7*76;enemy=companies+4+8*76
    assert get(0x397D8,companies)==2
    assert get(0x3CB30,ally,2)==get(0x3CB30,enemy,2)==0 and get(0x3C740,ally)==21
    get(0x3C8F4,ally,2,1,8)
    get(0x3C8F4,enemy,2,2,21)
    assert get(0x3CB30,ally,2)==1 and get(0x3C740,ally)==8
    assert get(0x3CB30,enemy,2)==2
    native=bytes(cpu.mem_read(BASE,len(raw)))
    extra={player+0x1F+7,player+0x1F+8,ally+0x47}
    delta={BASE+i for i,(a,b) in enumerate(zip(after,native,strict=True)) if a!=b}
    assert delta==extra
    owned=set(receipt['owned_bytes'])|extra
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,native,strict=True)) if a!=b]
    assert len(owned)==19 and all(c['address'] in owned for c in changes)
    receipt.update(context='prepareAssistancePactAtFirstSight',owned_bytes=sorted(owned),changes=changes,
        original_relation_and_support_method=0x0203C8F4,
        original_assistance_setter=0x0203CB00,original_assistance_getter=0x0203C740,
        original_method_calls=[{'company_ID':7,'arguments':[2,1,8]},{'company_ID':8,'arguments':[2,2,21]}],
        source_native_faction_state_fields=sorted(extra),
        original_supporting_company_ID=7,original_existing_opponent_company_ID=8,
        source_native_relations={'company7_to_player':1,'company8_to_player':2},
        source_native_assistance_target=8,
        every_other_RAM_byte_including_all_actor_identities_and_ship_stats_exact=True,
        no_numeric_message_event_selection_or_battle_outcome_injection=True,
        fixture_sha256=sha(Path(__file__).read_bytes()),after_RAM_sha256=sha(native))
    return native,receipt
