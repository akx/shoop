# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms
from shoop.xtheme.theme import Theme


class TestTheme(Theme):
    identifier = "test"
    name = "Xtheme Test Theme"
    author = "Aarni Koskela <aarni.koskela@shoop.io>"

    global_placeholders = [
        "header",
        "sidebar",
        "footer",
    ]


class AnotherTestTheme(Theme):
    identifier = "test2"
    name = "Another Test Theme"
    author = "Aarni Koskela <aarni.koskela@shoop.io>"

    fields = [
        ("huge_orange_text", forms.CharField(label="Huge orange text", required=False))
    ]
