# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
from typing import Any, cast

from lisa import schema
from lisa.feature import Feature

FEATURE_NAME_HIBERNATION = "Hibernation"


class HibernationSettings(schema.FeatureSettings):
    type: str = FEATURE_NAME_HIBERNATION
    enabled: bool = False


class Hibernation(Feature):
    @classmethod
    def on_before_deployment(cls, *args: Any, **kwargs: Any) -> None:
        settings = cast(schema.FeatureSettings, kwargs.get("settings"))

        if (isinstance(settings, HibernationSettings) and settings.enabled) or (
            not isinstance(settings, HibernationSettings)
        ):
            cls._install_by_platform(*args, **kwargs)

    @classmethod
    def name(cls) -> str:
        return FEATURE_NAME_HIBERNATION

    @classmethod
    def enabled(cls) -> bool:
        return True

    @classmethod
    def can_disable(cls) -> bool:
        return True

    @classmethod
    def _install_by_platform(cls, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    @classmethod
    def _get_resource(cls, resources: Any, type_name: str) -> Any:
        resource: Any = None
        for item in resources:
            if item["type"] == type_name:
                resource = item
                break
        assert resource
        return resource
