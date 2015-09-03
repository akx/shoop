# This file is part of Shoop.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shoop.apps import AppConfig


class XThemeTestThemeAppConfig(AppConfig):
    name = "shoop.xtheme.test_theme"
    verbose_name = "Shoop XTheme test theme"
    label = "shoop_xtheme_test"

    provides = {
        "xtheme": [
            "shoop.xtheme.test_theme.theme:TestTheme",
            "shoop.xtheme.test_theme.theme:AnotherTestTheme",
        ],
        "xtheme_plugin": [
            "shoop.xtheme.test_theme.plugins:ProductHighlightPlugin",
            "shoop.xtheme.test_theme.plugins:ProductDescriptionPlugin",
            "shoop.xtheme.test_theme.plugins:ProductAttributesPlugin",
            "shoop.xtheme.test_theme.plugins:ProductPackagePlugin",
            "shoop.xtheme.test_theme.plugins:ProductRelatedPlugin",
            "shoop.xtheme.test_theme.plugins:ProductImagesPlugin",
            "shoop.xtheme.test_theme.plugins:ProductInfoPlugin",
        ]
    }


default_app_config = "shoop.xtheme.test_theme.XThemeTestThemeAppConfig"
