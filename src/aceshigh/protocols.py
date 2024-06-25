import functools
import logging
from typing import Protocol, Tuple

from django.conf import settings
from django.forms import Form
from django.http import HttpRequest
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


class ServerSideContentProcessor(Protocol):
    """
    This class is used to process content in the server side.
    """

    TITLE: str | None = None
    DESCRIPTION: str | None = None

    def __init__(self, request: HttpRequest) -> None: ...

    def get_form_class(self, mode: str | None = None) -> Form | None: ...

    def process(
        self, content: str, mode: str | None = None, data: dict = {}
    ) -> str: ...

    def is_available(self, request: HttpRequest) -> bool:
        return True


@functools.lru_cache(maxsize=128)
def get_processors_classes() -> dict[str, dict[str, ServerSideContentProcessor]]:
    if not hasattr(settings, "ACESHIGH"):
        return {}
    if "processors" not in settings.ACESHIGH:
        return {}

    result = {}
    for mode in settings.ACESHIGH.get("processors", []):
        result[mode] = {}
        for import_path in settings.ACESHIGH["processors"][mode]:
            try:
                result[mode][import_path] = import_string(import_path)
            except ImportError:
                logger.exception("Failed to import processor %s", import_path)
    return result


def get_processor_choices(
    request: HttpRequest, mode: str | None = None
) -> list[Tuple[str, str]]:
    result = []
    for processor_mode, processor_paths in get_processors_classes().items():
        if processor_mode == "default" or processor_mode == mode:
            for processor_path, klass in processor_paths.items():
                processor = klass(request)  # type: ignore noqa
                if processor.is_available(request):
                    result.append(
                        (
                            processor_path,
                            processor.TITLE or processor.__class__.__name__,
                        )
                    )
    return result


def get_processor_class(
    request: HttpRequest, requested_processor_path: str
) -> ServerSideContentProcessor | None:
    for _, processor_paths in get_processors_classes().items():
        for processor_path, klass in processor_paths.items():
            if requested_processor_path != processor_path:
                continue
            processor = klass(request)  # type: ignore noqa
            if processor.is_available(request):
                return klass
    return None
