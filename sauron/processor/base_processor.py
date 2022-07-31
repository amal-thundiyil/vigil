import logging

from sauron.processor.base_backend import BackendTypes
from sauron.processor.base_backend import BaseBackend

LOG = logging.getLogger("sauron.processor.base_processor")


class BaseProcessor:
    def __init__(self, name, type, url, backend, domain) -> None:
        self.name = name
        self.type = type
        self.url = url
        self.backend = backend
        self.domain = domain

    @classmethod
    def get_processor_class(cls, domain, url, name, type, token):
        c = processor_mapping(domain)
        return cls.from_input(c, domain, url, name, type, token)

    @staticmethod
    def from_input(cls, domain, *args, **kwargs) -> None:
        backend = BaseBackend.from_input(*args, **kwargs)
        obj = cls(backend.name, backend.type, backend.url, backend, domain)
        return obj

    def process(self):
        raise NotImplementedError("No processor for given identifiers.")

    def server_ts(self):
        return None

    def summarize(self, data):
        raise NotImplementedError("No processor for given identifiers.")


class ValidationError(Exception):
    def __init__(self, message="Input fields are incorrect"):
        self.message = message
        super().__init__(self.message)


def validate(url, name, type):
    if not url and (not name and not (type in BackendTypes)):
        raise ValidationError(f"Please enter either the name, type or url")
    if not url and (not name or not (type in BackendTypes)):
        raise ValidationError(f"One of name and type is invalid ({name}, {type})")
    if not url and not (name and (type in BackendTypes)):
        raise ValidationError(f"Please enter a valid URL ({url})")


def final_summary(scores):
    final_score = round(sum(scores) / max(1, len(scores)), 2)
    final_description = f"Got score of {final_score}"
    return final_score, final_description


def processor_mapping(domain):
    from sauron.processor.processors.community import CommunityProcessor
    from sauron.processor.processors.maintainence import MaintainenceProcessor
    from sauron.processor.processors.popularity import PopularityProcessor
    from sauron.processor.processors.security import SecurityProcessor

    mapping = {
        "community": CommunityProcessor,
        "maintainence": MaintainenceProcessor,
        "popularity": PopularityProcessor,
        "security": SecurityProcessor,
    }
    return mapping.get(domain)
