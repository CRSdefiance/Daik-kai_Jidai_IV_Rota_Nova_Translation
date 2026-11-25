"""Copy complete personality commands andqualify expected runtime-role headers in QA fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_reviewed_dialogue_fixtures_v1.py').read_text(encoding='utf-8'),{
    '    args = parser.parse_args()':"    parser.add_argument('--roles',type=Path,required=True)\n    args = parser.parse_args()",
    "    parent = Path(rebuilt['research_ROM'])":
        """    roles=load(args.roles);assert roles['runtime']==stored['runtime']
    resolved={r['source_selector']:r['resolved_actor_ID'] for r in roles['native_roles']['rows']}
    voice={r['source_selector']:r['source_voice_class'] for r in roles['native_roles']['rows']}
    styles=load(rebuilt['styles']);assert styles['runtime']==stored['runtime']
    parent = Path(rebuilt['research_ROM'])""",
    "for r in stored['records']}":"for r in [*stored['records'],*stored['style_records']]}",
    "            else:\n                request = action['menu']":
        """            elif 'style' in action:
                request=action['style'];group=groups[request['block']]
                proof=next(p for p in styles['objects'] if p['block']==request['block'] and p['source_command_offset']==request['source_command_offset'])
                raw=bytes.fromhex(proof['target_object_hex']);selector=raw[19]
                assert selector in resolved and selector in voice
                selected_style=voice[selector]
                if 'expected_style' in request:assert selected_style==request['expected_style']
                slot=proof['native_slots'][selected_style];ident=slot['record_id'];row=byid[ident]
                command=next(c for c in group['all_target_commands'] if c['whole_command_hex']==raw.hex())
                assert command['word']==0x4100 and raw[18:20]==bytes.fromhex(row['source_header_hex'])[18:20]
                body=bytes.fromhex(slot['target_hex']);assert body.hex()==expanded[ident]
                at=len(logical);logical+=raw
                bindings.append(dict(id=ident,block=row['block'],selector=selector,fixture_offset=at,
                    stored_command_offset=command['offset'],stored_hex=body.hex(),expected_expanded_body_hex=expanded[ident],
                    logical_English=row['english'],native_object_kind='4100-style-alternative',expected_style=selected_style,
                    expected_header_actor_ID=resolved[selector],whole_eight_slot_command_copied_without_state_override=True))
                copied.append(dict(block=row['block'],original_offset=command['offset'],fixture_offset=at,whole_command_hex=raw.hex(),word=0x4100))
                pages+=len(bynative[ident]['complete_native_English_display']['pages'])
            else:
                request = action['menu']""",
    'assert len(actual_texts) == len(bindings)':
        "assert len(actual_texts)+sum(c['word']==0x4100 for c in actual) == len(bindings)",
    "            ordinary_actor_IDs=sorted({r['selector'] for r in bindings if r['selector'] != 254}),":
        """            ordinary_actor_IDs=sorted({r['selector'] for r in bindings if r['selector'] != 254}),
            source_selectors_with_header=sorted({r['selector'] for r in bindings if r['selector']!=254}),
            expected_header_actor_ID_by_selector={str(r['selector']):resolved.get(r['selector'],r['selector']) for r in bindings if r['selector']!=254},
            expected_header_IDs_qualified_offline_not_inferred_from_pixels=True,
            dynamic_role_proof=str(args.roles),dynamic_role_proof_sha256=sha(args.roles.read_bytes()),
            source_personality_tables_copied_complete=sum(c['word']==0x4100 for c in copied),
            no_original_conditional_menu_outcome_orstat_claim=True,""",
    'ORDINARY, Path(__file__)]':'ORDINARY,args.roles,Path(__file__)]',
})
exec(compile(source,__file__+'::same-initialized-native-command-fixtures-with-complete-style-objects', 'exec'),globals())
