from qdrant_client.http.models import Filter


def qdrant_filter_from_dict(self, filter: dict) -> Filter:
    if not filter:
        return None

    return Filter(
        must=[
            condition
            for key, value in filter.items()
            for condition in self._build_condition(key, value)
        ]
    )

