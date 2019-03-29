#
# This file is part of the PyRDP project.
# Copyright (C) 2019 GoSecure Inc.
# Licensed under the GPLv3 or later.
#

from pyrdp.layer import FastPathLayer
from pyrdp.mitm.state import RDPMITMState
from pyrdp.pdu import FastPathPDU


class FastPathMITM:
    """
    MITM component for the fast-path layer.
    """

    def __init__(self, client: FastPathLayer, server: FastPathLayer, state: RDPMITMState):
        """
        :param client: fast-path layer for the client side
        :param server: fast-path layer for the server side
        """

        self.client = client
        self.server = server
        self.state = state

        self.client.createObserver(
            onPDUReceived = self.onClientPDUReceived,
        )

        self.server.createObserver(
            onPDUReceived = self.onServerPDUReceived,
        )

    def onClientPDUReceived(self, pdu: FastPathPDU):
        if self.state.forwardInput:
            self.server.sendPDU(pdu)

    def onServerPDUReceived(self, pdu: FastPathPDU):
        if self.state.forwardOutput:
            self.client.sendPDU(pdu)