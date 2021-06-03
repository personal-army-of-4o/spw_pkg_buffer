from nyanMigen import nyanify


@nyanify
def spw_pkg_guard():
    iHandshake = Signal()
    oHandshake = Signal(domain = 'sync')
    iValid = Signal()
    iData = Signal(9)
    oAck= Signal()
    oValid = Signal()
    oData = Signal(9)
    iAck = Signal()

    sState = Fsm(init = 'idle')
    with switch(sState):
        with case('idle'):
            if(iHandshake):
                sState = 'pumping'
        with case('pumping'):
            if((iValid == 1) & (iAck == 1) & (iData[8] == 1)):
                sState = 'done'
        with case('done'):
            if(iHandshake == 0):
                sState = 'idle'
        with default:
            sState = 'idle'

    with m.Switch(sState):
        with case('idle'):
            oValid = 0
            oData = 0
            oAck = 0
            oHandshake = 0
        with case('pumping'):
            oValid = iValid
            oData = iData
            oAck = iAck
            oHandshake = 1
        with case('done'):
            oValid = 0
            oData = 0
            oAck = 0
            oHandshake = 1
        with default:
            oValid = 0
            oData = 0
            oAck = 0
            oHandshake = 0
