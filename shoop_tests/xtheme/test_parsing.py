# -*- coding: utf-8 -*-
import pytest

from shoop.xtheme.parsing import NestingError, NonConstant
from shoop.xtheme.testing import override_current_theme_class
from shoop_tests.xtheme.utils import get_jinja2_engine


def test_parsing():
    with override_current_theme_class(None):
        jeng = get_jinja2_engine()
        template = jeng.get_template("complex.jinja")
        assert template  # it'sa me! template!


def test_nonconstant_placeholder_name_fails():
    with pytest.raises(NonConstant):
        get_jinja2_engine().from_string("""{% placeholder "foo" ~ foo %}{% endplaceholder %}""")


def test_bare_placeholder_name_succeeds():
    get_jinja2_engine().from_string("""{% placeholder foo %}{% endplaceholder %}""")


def test_unplaceheld_cola_fails():
    with pytest.raises(NestingError):
        get_jinja2_engine().from_string("""{% column %}{% endcolumn %}""")


def test_nondict_column_arg_fails():
    with pytest.raises(ValueError):
        get_jinja2_engine().from_string("""
        {% placeholder foo %}
        {% column 666 %}{% endcolumn %}
        {% endplaceholder %}
        """)


def test_nonconstant_column_arg_fails():
    with pytest.raises(ValueError):
        get_jinja2_engine().from_string("""
        {% placeholder foo %}
        {% column {"var": e} %}{% endcolumn %}
        {% endplaceholder %}
        """)


def test_argumented_row_fails():
    with pytest.raises(ValueError):
        get_jinja2_engine().from_string("""
        {% placeholder foo %}
        {% row {"var": e} %}{% endrow %}
        {% endplaceholder %}
        """)


def test_nested_placeholders_fail():
    with pytest.raises(NestingError):
        get_jinja2_engine().from_string("""
        {% placeholder foo %}
            {% placeholder bar %}{% endplaceholder %}
        {% endplaceholder %}
        """)


def test_nonconstant_plugin_content_fails():
    with pytest.raises(NonConstant):
        get_jinja2_engine().from_string("""
        {% placeholder foo %}
            {% plugin "text" %}
            text = {{ volcano }}
            {% endplugin %}
        {% endplaceholder %}
        """)


def test_nonstring_but_constant_plugin_content_fails():
    with pytest.raises(NonConstant):
        get_jinja2_engine().from_string("""
        {% placeholder foo %}
            {% plugin "text" %}
            text = {{ 8 }}
            {% endplugin %}
        {% endplaceholder %}
        """)
