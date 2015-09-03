# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms
from shoop.front.template_helpers.general import get_newest_products, get_best_selling_products, get_random_products
from shoop.xtheme.plugins import TemplatedPlugin, templated_plugin_factory
from django.utils.translation import ugettext_lazy as _


class ProductHighlightPlugin(TemplatedPlugin):
    identifier = "product_highlight"
    name = _("Product Highlights")
    template_name = "test_theme/highlight_plugin.jinja"
    fields = [
        ("title", forms.CharField(required=False, initial="")),
        ("type", forms.ChoiceField(choices=[
            ("newest", "Newest"),
            ("best_selling", "Best Selling"),
            ("random", "Random"),
        ], initial="newest")),
        ("count", forms.IntegerField(min_value=1, initial=4))
    ]

    def get_context_data(self, context):
        type = self.config.get("type", "newest")
        count = self.config.get("count", 4)
        if type == "newest":
            products = get_newest_products(context, count)
        elif type == "best_selling":
            products = get_best_selling_products(context, count)
        elif type == "random":
            products = get_random_products(context, count)
        else:
            products = []

        return {
            "request": context["request"],
            "title": self.config.get("title"),
            "products": products
        }


ProductDescriptionPlugin = templated_plugin_factory(
    identifier="product_description",
    template_name="test_theme/product_description.jinja",
    required_context_variables=["product"],
    inherited_variables=["shop_product"],
)

ProductAttributesPlugin = templated_plugin_factory(
    identifier="product_attributes",
    template_name="test_theme/product_attributes.jinja",
    required_context_variables=["product"],
    inherited_variables=["shop_product"],
)

ProductPackagePlugin = templated_plugin_factory(
    identifier="product_package",
    template_name="test_theme/product_package.jinja",
    required_context_variables=["product"],
    inherited_variables=["shop_product"],
)

ProductRelatedPlugin = templated_plugin_factory(
    identifier="product_related",
    template_name="test_theme/product_related.jinja",
    required_context_variables=["product"],
    config_copied_variables=("title", "type"),
)

ProductImagesPlugin = templated_plugin_factory(
    identifier="product_images",
    template_name="test_theme/product_images.jinja",
    required_context_variables=["product"],
    inherited_variables=("images",),
)

ProductInfoPlugin = templated_plugin_factory(
    identifier="product_info",
    template_name="test_theme/product_info.jinja",
    required_context_variables=["product"],
    inherited_variables=["shop_product"],
)
