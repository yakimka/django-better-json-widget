from unittest.mock import Mock

import pytest

from better_json_widget import widgets


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
    widget = widgets.BetterJsonWidget(schema=schema)

    result = widget.render(name="content", value=None)

    assert "icon-changelink.svg" in result
    assert "better-json-textarea" in result


def test_media():
    widget = widgets.BetterJsonWidget(schema=schema)

    result = widget.media

    assert result._js == [  # noqa: PLW0212
        "better_json_widget/js/lib/vue.3.2.26.global.prod.js"
    ]


def test_can_disable_bundled_vuejs(monkeypatch):
    monkeypatch.setattr(
        widgets, "settings", Mock(BETTER_JSON_WIDGET_VUE_URL=None)
    )
    widget = widgets.BetterJsonWidget(schema=schema)

    result = widget.media

    assert result is None


def test_cant_pass_both_schema_and_schema_mapping():
    with pytest.raises(
        ValueError, match="Cannot specify both schema and schema_mapping"
    ):
        widgets.BetterJsonWidget(
            schema={"type": "object"},
            schema_mapping={"selected": {"type": "object"}},
        )


def test_must_pass_schema_or_schema_mapping():
    with pytest.raises(
        ValueError, match="Must specify either schema or schema_mapping"
    ):
        widgets.BetterJsonWidget()


def test_cant_pass_follow_field_when_schema_is_passed():
    with pytest.raises(
        ValueError, match="Cannot specify both follow_field with schema"
    ):
        widgets.BetterJsonWidget(schema={"type": "object"}, follow_field="foo")


def test_must_pass_follow_field_for_schema_mapping():
    with pytest.raises(
        ValueError, match="Must specify follow_field with schema_mapping"
    ):
        widgets.BetterJsonWidget(
            schema_mapping={"selected": {"type": "object"}}
        )


def test_cant_pass_only_follow_field():
    with pytest.raises(ValueError):
        widgets.BetterJsonWidget(follow_field="foo")


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
    widget = widgets.BetterJsonWidget(**kwargs)

    result = widget.render(name="content", value=None)

    assert expected in result
