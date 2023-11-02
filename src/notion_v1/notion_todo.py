import re
from notion_client import Client
from enum import StrEnum
from typing import Any, List
from collections import ChainMap


class NotionTodoProperties(StrEnum):
    name = 'Name:title'
    complete = 'Complete:checkbox'
    tags = 'Tags:multi_select'
    parent_todo = 'Parent todo:relation'
    child_todo = 'Child todos:relation'

    @classmethod
    def get_type(cls, prop_name: str):
        name_type_map = (
            str(e).split(":") for e in cls
        )
        try:
            return next(
                t for (n, t) in name_type_map if n == prop_name
            )
        except StopIteration:
            raise ValueError(f"{prop_name=} not defined in {cls}")


class NotionPropertyConstructors:
    @classmethod
    def build(cls, name: str, type: str, value: Any):
        return getattr(cls, type)(name, value)

    @staticmethod
    def title(name: str, value: str):
        return {
            name: {
                "title": [{
                    "text": {
                        "content": value,
                    },
                },],
            }
        }

    @staticmethod
    def checkbox(name: str, value: bool):
        return {
            name: {
                'checkbox': value
            }
        }

    @staticmethod
    def multi_select(name: str, selections: List[str]):
        return {
            name: {
                "multi_select": [
                    {"name": tag}for tag in selections
                ]
            }
        }

    @staticmethod
    def relation(name: str, relation_id: str):
        return {
            name: {
                'relation': [{
                    'id': relation_id,
                },]
            }
        }


class NotionTodo:
    id: str
    database_id: str
    notion_cli: Client

    def __init__(self, notion_api_page: dict, notion_cli: Client):
        self.notion_cli = notion_cli
        self.id = notion_api_page['id']
        self.database_id = notion_api_page['parent']['database_id']
        properties = notion_api_page['properties']
        for property_name, property_data in properties.items():
            property_type = property_data['type']
            if property_type == 'relation':
                relations = property_data['relation']
                relation_ids = [r['id'] for r in relations]
                if len(relation_ids) == 1:
                    self._set_property(property_name, relation_ids[0])
                elif len(relation_ids) > 1:
                    self._set_property(property_name, relation_ids)
                else:
                    self._set_property(property_name, None)
            elif property_type == 'checkbox':
                checkbox_value = property_data['checkbox']
                self._set_property(property_name, checkbox_value)
            elif property_type == 'multi_select':
                multi_select_names = [
                    v['name'] for v in property_data['multi_select']
                ]
                self._set_property(property_name, multi_select_names)
            elif property_type == 'title':
                plain_text = property_data['title'][0]['plain_text']
                self._set_property(property_name, plain_text)
            else:
                raise NotImplementedError(
                    f"{property_type=}, {property_data=}")

    def _set_property(self, property_name, property_value):
        property_name = re.sub('\s+', '_', property_name.lower())
        setattr(self, property_name, property_value)

    def __iter__(self):
        return (items for items in self.__dict__.items() if items[0] != "notion_cli")

    def __repr__(self) -> str:
        return f'<NotionTodo "{self.name}" {self.id=}>'

    @classmethod
    def new(cls, notion_client: Client, database_id: str, properties: dict):
        prop_name_val_type = (
            (p_name, NotionTodoProperties.get_type(p_name), p_value)
            for p_name, p_value in properties.items()
            if p_value is not None
        )
        properties = [
            NotionPropertyConstructors.build(*args)
            for args in prop_name_val_type
        ]
        properties = dict(ChainMap(*properties))

        r = notion_client.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        return cls(r, notion_client)
