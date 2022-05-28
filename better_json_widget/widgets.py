from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms import Media
from django.template.loader import get_template
from django.templatetags.static import static

if TYPE_CHECKING:
    from django.forms.renderers import BaseRenderer


DEFAULT_VUE_URL = static("better_json_widget/js/lib/vue.3.2.26.global.prod.js")


class BetterJsonWidget(AdminTextareaWidget):
    def __init__(
        self,
        attrs=None,
        schema: Union[dict, Callable[[], dict], None] = None,
        follow_field: str = "",
        schema_mapping: Union[dict, Callable[[], dict], None] = None,
    ):
        if schema and schema_mapping:
            raise ValueError("Cannot specify both schema and schema_mapping")
        if not schema and not schema_mapping:
            raise ValueError("Must specify either schema or schema_mapping")
        if schema and follow_field:
            raise ValueError(
                "Cannot specify both follow_field with schema. Use"
                " schema_mapping instead"
            )
        if schema_mapping and not follow_field:
            raise ValueError("Must specify follow_field with schema_mapping")

        super().__init__(attrs)

        self._schema = schema or {}
        self._follow_field = follow_field
        self._schema_mapping = schema_mapping or {}

    @property
    def media(self):
        vue = getattr(settings, "BETTER_JSON_WIDGET_VUE_URL", DEFAULT_VUE_URL)
        if not vue:
            return None
        return Media(js=[vue])

    def render(
        self,
        name: str,
        value: Any,
        attrs: Optional[dict[str, Any]] = None,
        renderer: Optional[BaseRenderer] = None,
    ):
        schema = self._schema
        if callable(schema):
            schema = schema()
        follow_field = self._follow_field
        schema_mapping = self._schema_mapping
        if callable(schema_mapping):
            schema_mapping = schema_mapping()

        attrs = attrs or {}
        html = super().render(name, value, attrs, renderer)
        template = get_template("better_json_widget/better_json_widget.html")

        html += template.render(
            {
                "field_name": name,
                "follow_field": follow_field,
                "schema_mapping": json.dumps(schema_mapping or {"": schema}),
            }
        )
        return html
