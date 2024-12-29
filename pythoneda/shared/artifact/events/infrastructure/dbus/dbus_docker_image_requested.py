# vim: set fileencoding=utf-8
"""
pythoneda/shared/artifact/events/infrastructure/dbus/dbus_docker_image_requested.py

This file defines the DbusDockerImageRequested class.

Copyright (C) 2024-today rydnr's pythoneda-shared-artifact/events-infrastructure

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
from pythoneda.shared.artifact.events import DockerImageRequested
from pythoneda.shared.artifact.events.infrastructure.dbus import DBUS_PATH
from typing import List, Tuple, Type


class DbusDockerImageRequested(DbusEvent):
    """
    D-Bus interface for DockerImageRequested

    Class name: DbusDockerImageRequested

    Responsibilities:
        - Define the d-bus interface for the DockerImageRequested event.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new DbusDockerImageRequested.
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
        return "Pythoneda_Artifact_DockerImageRequested"

    @signal()
    def DockerImageRequested(self, imageName: "s", imageVersion: "s", medatada: "s"):
        """
        Defines the DockerImageRequested d-bus signal.
        :param imageName: The image name.
        :type imageName: str
        :param imageVersion: The version.
        :type imageVersion: str
        :param metadata: The metadata.
        :type metadata: str
        """
        pass

    def build_path(self, event: Event) -> str:
        """
        Retrieves the d-bus path for given event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: Such value.
        :rtype: str
        """
        return self.path + "/" + event.image_name.replace("-", "_")

    @classmethod
    def transform(cls, event: DockerImageRequested) -> List[str]:
        """
        Transforms given event to signal parameters.
        :param event: The event to transform.
        :type event: pythoneda.shared.artifact.events.DockerImageRequested
        :return: The event information.
        :rtype: List[str]
        """
        return [
            event.image_name,
            event.image_version,
            json.dumps(event.metadata, ensure_ascii=False),
            json.dumps(event.previous_event_ids),
            Invariants.instance().to_json(event),
            event.id,
        ]

    @classmethod
    def sign(cls, event: DockerImageRequested) -> str:
        """
        Retrieves the signature for the parameters of given event.
        :param event: The domain event.
        :type event: pythoneda.shared.artifact.events.DockerImageRequested
        :return: The signature.
        :rtype: str
        """
        return "ssssss"

    @classmethod
    def parse(
        cls, message: Message, app: PythonedaApplication
    ) -> Tuple[str, DockerImageRequested]:
        """
        Parses given d-bus message containing a DockerImageRequested event.
        :param message: The message.
        :type message: dbus_next.Message
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.PythonedaApplication
        :return: A tuple with the invariants and the DockerImageRequested event.
        :rtype: Tuple[str, pythoneda.shared.artifact.events.DockerImageRequested]
        """
        (
            image_name,
            image_version,
            metadata,
            prev_event_ids,
            invariants,
            event_id,
        ) = message.body
        return (
            invariants,
            DockerImageRequested(
                image_name,
                image_version,
                json.loads(metadata),
                json.loads(prev_event_ids),
                event_id,
            ),
        )

    @classmethod
    def event_class(cls) -> Type[Event]:
        """
        Retrieves the specific event class.
        :return: Such class.
        :rtype: type(pythoneda.shared.Event)
        """
        return DockerImageRequested


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
