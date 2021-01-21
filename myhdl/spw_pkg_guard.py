from myhdl import *

@block
def spw_pkg_guard(iClk, iReset, iHandshake, oHandshake, iValid, iData, oAck, oValid, oData, iAck):

    states = enum('idle', 'fopen', 'pump', 'fclose')
    state = Signal(states.idle)
    state_next = Signal(states.idle)

    @always(iClk.posedge, iReset.negedge)
    def state_current_logic():
        if iReset == 0 :
            state.next = states.idle
        else :
            state.next = state_next

    @always_comb
    def state_next_logic():
        state_next.next = state
        if state == states.idle:
            if iValid == 1 and iData[8] == 0:
                state_next.next = states.fopen
        elif state == states.fopen:
            if iHandshake == 1:
                state_next.next = states.pump
        elif state == states.pump:
            if iValid == 1 and iData[8] == 1 and iAck == 1:
                state_next.next = states.fclose
        elif state == states.fclose:
            if iHandshake == 0:
                state_next.next = states.idle

    @always_comb
    def output_logic():
        if state == states.idle:
            oHandshake.next = 0
            oValid.next = 0
            oData.next = 0
            if iValid == 1 and iData[8] == 1:
                oAck.next = 1
            else:
                oAck.next = 0
        elif state == states.fopen:
            oHandshake.next = 1
            oValid.next = 0
            oData.next = 0
            oAck.next = 0
        elif state == states.pump:
            oHandshake.next = 1
            oValid.next = iValid
            oData.next = iData
            oAck.next = iAck
        elif state == states.fclose:
            oHandshake.next = 0
            oValid.next = 0
            oData.next = 0
            oAck.next = 0

    return state_current_logic, state_next_logic, output_logic
  
def main():
    iClk = Signal(bool(0))
    iReset = Signal(bool(0))
    iHandshake = Signal(bool(0))
    oHandshake = Signal(bool(0))
    iValid = Signal(bool(0))
    iData = Signal(intbv(0)[9:])
    oAck = Signal(bool(0))
    oValid = Signal(bool(0))
    oData = Signal(intbv(0)[9:])
    iAck = Signal(bool(0))

    uut= spw_pkg_guard(iClk, iReset, iHandshake, oHandshake, iValid, iData, oAck, oValid, oData, iAck)
    uut.convert(hdl="VHDL", initial_values=False)

if __name__ == '__main__':
    main()
