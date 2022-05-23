import pytest

from better_json_widget.widgets import BetterJsonWidget


@pytest.fixture()
def schema():
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "chat_id": {
                "type": "string",
                "title": "Chat ID",
                "description": "Telegram chat id",
            },
            "disable_link_preview": {
                "type": "boolean",
                "description": "Disable link preview",
                "default": False,
            },
        },
        "required": ["chat_id"],
    }


def test_render(schema):
    widget = BetterJsonWidget(schema=schema)

    result = widget.render(name="content", value=None)

    assert ".esm-browser.js" in result
    assert "icon-changelink.svg" in result
    assert "better-json-textarea" in result


def test_cant_pass_both_schema_and_schema_mapping():
    with pytest.raises(
        ValueError, match="Cannot specify both schema and schema_mapping"
    ):
        BetterJsonWidget(
            schema={"type": "object"},
            schema_mapping={"selected": {"type": "object"}},
        )


def test_must_pass_schema_or_schema_mapping():
    with pytest.raises(
        ValueError, match="Must specify either schema or schema_mapping"
    ):
        BetterJsonWidget()


def test_cant_pass_follow_field_when_schema_is_passed():
    with pytest.raises(
        ValueError, match="Cannot specify both follow_field with schema"
    ):
        BetterJsonWidget(schema={"type": "object"}, follow_field="foo")


def test_must_pass_follow_field_for_schema_mapping():
    with pytest.raises(
        ValueError, match="Must specify follow_field with schema_mapping"
    ):
        BetterJsonWidget(schema_mapping={"selected": {"type": "object"}})


def test_cant_pass_only_follow_field():
    with pytest.raises(ValueError):
        BetterJsonWidget(follow_field="foo")


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({"schema": {"type": "object"}}, '{"type": "object"}'),
        (
            {"schema": (lambda: {"type": "object"})},
            '{"type": "object"}',
        ),
        (
            {
                "schema_mapping": {"foobar": {"type": "string"}},
                "follow_field": "bazooka",
            },
            "bazooka",
        ),
        (
            {
                "schema_mapping": {"foobar": {"type": "string"}},
                "follow_field": "bazooka",
            },
            '{"type": "string"}',
        ),
        (
            {
                "schema_mapping": (lambda: {"foobar": {"type": "string"}}),
                "follow_field": "bazooka",
            },
            '{"type": "string"}',
        ),
        (
            {
                "schema_mapping": {"foobar": {"type": "string"}},
                "follow_field": "bazooka",
            },
            "foobar",
        ),
    ],
    ids=[
        "Render schema",
        "Render schema callable",
        "Render follow_field",
        "Render schema_mapping",
        "Render schema_mapping callable",
        "Render schema_mapping key",
    ],
)
def test_render_schema(kwargs, expected):
    widget = BetterJsonWidget(**kwargs)

    result = widget.render(name="content", value=None)

    assert expected in result
