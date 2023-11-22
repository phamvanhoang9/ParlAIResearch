#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
File for Message object and associated functions.

The Message object's key function is to prevent users from editing fields in an action
or observation dict unintentionally.
"""

from __future__ import annotations # for type hints of classmethods, the purpose of this is to allow you to type hint a classmethod as returning the same type as the class that declares it.
from typing import Any, Dict
"""
Any: Any type is acceptable
Dict: A dictionary is a collection which is unordered, changeable and indexed. In Python dictionaries are written with curly brackets, and they have keys and values.
"""


UNSAFE_FIELDS = {'metrics'} # metrics is a field that is used to store metrics for the agent, and is not safe to send to a client.


class Message(dict):
    """
    Class for observations and actions in ParlAI.

    Functions like a dict, but triggers a RuntimeError when calling __setitem__ for a
    key that already exists in the dict.
    """

    def __setitem__(self, key, val): # __setitem__ is a method that is called when you assign a value to an item in a dictionary.
        if key in self:
            raise RuntimeError(
                'Message already contains key `{}`. If this was intentional, '
                'please use the function `force_set(key, value)`.'.format(key)
            )
        super().__setitem__(key, val)

    def force_set(self, key, val):
        super().__setitem__(key, val)

    def copy(self):
        return type(self)(self)
    """
    type() returns the type of the object or creates a new type object with the specified name, bases (or tuple of bases) and dict(dict describes the attributes of the class).
    """
    @classmethod # classmethod is a method that is bound to a class rather than its object.
    def padding_example(cls) -> Message:
        """
        Create a Message for batch padding.
        """
        return cls({'batch_padding': True, 'episode_done': True})

    def is_padding(self) -> bool:
        """
        Determine if a message is a padding example or not.
        """
        return bool(self.get('batch_padding'))

    def json_safe_payload(self) -> Dict[str, Any]: # Dict[str, Any] is a dictionary with string keys and any type of values.
        """
        Prepare a Message for delivery to a client via json.

        Useful for chat-services, external libraries, and mephisto delivery.

        Works by stripping known unsafe fields from the message, and converting
        the object to a dict.
        """
        return {k: v for k, v in self.items() if k not in UNSAFE_FIELDS} # items() returns a list of tuple pairs (key, value) in the dictionary.
