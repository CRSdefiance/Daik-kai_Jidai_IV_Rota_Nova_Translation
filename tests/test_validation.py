from dk4tool.script.validate import validate_rows


def row(**changes):
    value = {
        "id": "DK4_1",
        "status": "draft",
        "japanese": "質問{END}",
        "english": "Question{END}",
        "encoding": "shift_jis",
        "source_length": "20",
        "max_bytes": "20",
        "allow_expand": "false",
        "wrap_width": "32",
    }
    value.update(changes)
    return value


def test_missing_control_token_fails():
    issues = validate_rows([row(english="Question")])
    assert any("control tokens missing" in issue.message for issue in issues)


def test_overflow_fails():
    issues = validate_rows([row(max_bytes="3")])
    assert any("maximum is 3" in issue.message for issue in issues)


def test_valid_row_has_no_errors():
    assert not [issue for issue in validate_rows([row()]) if issue.severity == "error"]


def test_mesfile_wrap_width_ignores_control_tokens():
    issues = validate_rows(
        [
            row(
                japanese="質問",
                english="{HEX:05}A short line{LB}Another short line{PAD}",
                control_profile="mesfile",
                source_length="40",
                max_bytes="40",
                wrap_width="18",
            )
        ]
    )
    assert issues == []
