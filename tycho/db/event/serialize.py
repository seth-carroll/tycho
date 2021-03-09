from datetime import datetime
from typing import Dict, List

from ...models.event import Event, DOT_CONVERTER, DOT_CONSTANT


def serialize_to_db_event(event: Event) -> Dict:
    """
    Transforms public event format to DB event format.
    Ignores key and value with NoneType.
    """

    new_event = {}

    new_event["tags"] = []

    if event.tags is not None:
        new_event["tags"].extend(_get_tags(event.tags))

    for key in ["source_id", "parent_id"]:
        if getattr(event, key):
            new_event["tags"].append(
                "{key}:{value}".format(key=key, value=getattr(event, key)))

    if event.id is not None:
        new_event["_id"] = str(event.id)

    new_event["time"] = []

    for key in ["start_time", "end_time"]:
        if getattr(event, key) is not None:
            new_event["time"].append(getattr(event, key))

    if getattr(event, "description") is not None:
        new_event["description"] = event.description

    if getattr(event, "detail_urls") is not None:
        new_event["detail_urls"] = {}
        for key, value in event.detail_urls.items():
            key = key.replace(DOT_CONSTANT, DOT_CONVERTER)
            new_event["detail_urls"][key] = value

    new_event["update_time"] = datetime.utcnow()

    return new_event


def _get_tags(event_tags: Dict) -> List:
    """
    Transforms dictionary of key-value pairs (not in untag_fields list)
    to list of key-value pair concatenated as strings inside tags field.
    """
    tags = []

    # event_tags will be an empty dictionary by default.
    # key and value in event_tags will never be of None Type.
    for key in event_tags:
        for value in event_tags[key]:
            tags.append(
             "{key}:{value}".format(key=key, value=value))

    return tags
