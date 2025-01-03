# vim: set fileencoding=utf-8
"""
pythoneda/shared/artifact/events/infrastructure/dbus/dbus_change_staged.py

This file defines the DbusChangeStaged class.

Copyright (C) 2023-today rydnr's pythoneda-shared-artifact/events-infrastructure

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from dbus_next import Message
from dbus_next.service import signal
import json
from pythoneda.shared import Event, Invariants, PythonedaApplication
from pythoneda.shared.infrastructure.dbus import DbusEvent
from pythoneda.shared.artifact.events import Change, ChangeStaged
from pythoneda.shared.artifact.events.infrastructure.dbus import DBUS_PATH
from typing import List, Tuple, Type


class DbusChangeStaged(DbusEvent):
    """
    D-Bus interface for ChangeStaged

    Class name: DbusChangeStaged

    Responsibilities:
        - Define the d-bus interface for the ChangeStaged event.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new DbusChangeStaged.
        """
        super().__init__(DBUS_PATH)

    @classmethod
    @property
    def name(cls) -> str:
        """
        Retrieves the d-bus interface name.
        :return: Such value.
        :rtype: str
        """
        return "Pythoneda_Artifact_ChangeStaged"

    @signal()
    def ChangeStaged(self, change: "s"):
        """
        Defines the ChangeStaged d-bus signal.
        :param change: The change.
        :type change: str
        """
        pass

    @classmethod
    def transform(cls, event: ChangeStaged) -> List[str]:
        """
        Transforms given event to signal parameters.
        :param event: The event to transform.
        :type event: pythoneda.shared.artifact.events.ChangeStaged
        :return: The event information.
        :rtype: List[str]
        """
        return [
            event.change.to_json(),
            json.dumps(event.previous_event_ids),
            Invariants.instance().to_json(event),
            event.id,
        ]

    @classmethod
    def sign(cls, event: ChangeStaged) -> str:
        """
        Retrieves the signature for the parameters of given event.
        :param event: The domain event.
        :type event: pythoneda.shared.artifact.events.ChangeStaged
        :return: The signature.
        :rtype: str
        """
        return "ssss"

    @classmethod
    def parse(
        cls, message: Message, app: PythonedaApplication
    ) -> Tuple[str, ChangeStaged]:
        """
        Parses given d-bus message containing a ChangeStaged event.
        :param message: The message.
        :type message: dbus_next.Message
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.PythonedaApplication
        :return: A tuple with the invariants and the ChangeStaged event.
        :rtype: Tuple[str, pythoneda.shared.artifact.events.ChangeStaged]
        """
        change, prev_event_ids, invariants, event_id = message.body
        return (
            invariants,
            ChangeStaged(
                Change.from_json(change), json.loads(prev_event_ids), event_id
            ),
        )

    @classmethod
    def event_class(cls) -> Type[Event]:
        """
        Retrieves the specific event class.
        :return: Such class.
        :rtype: type(pythoneda.shared.Event)
        """
        return ChangeStaged


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
