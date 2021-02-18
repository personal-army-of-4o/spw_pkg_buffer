from nmigen import *
from nmigen.cli import main
from nmigen.back import verilog


class spw_pkg_guard(Elaboratable):
    def __init__(self):
        self.iHandshake = Signal()
        self.oHandshake = Signal()
        self.iValid = Signal()
        self.iData = Signal(9)
        self.oAck= Signal()
        self.oValid = Signal()
        self.oData = Signal(9)
        self.iAck = Signal()

    def ports(self):
        return [
            self.iHandshake,
            self.oHandshake,
            self.iValid,
            self.iData,
            self.oAck,
            self.oValid,
            self.oData,
            self.iAck
        ]
 
    def elaborate(self, platform):
        m = Module()
        sState = Signal(2)
        with m.Switch(sState):
            with m.Case(0):
                with m.If(self.iHandshake == 1):
                    m.d.sync += sState.eq(1)
            with m.Case(1):
                with m.If((self.iValid == 1) & (self.iAck == 1) & (self.iData[8] == 1)):
                    m.d.sync += sState.eq(2)
            with m.Case(2):
                with m.If(self.iHandshake == 0):
                    m.d.sync += sState.eq(0)
            with m.Default():
                m.d.sync += sState.eq(0)
        with m.Switch(sState):
            with m.Case(0):
                m.d.comb += self.oValid.eq(0)
                m.d.comb += self.oData.eq(0)
                m.d.comb += self.oAck.eq(0)
                m.d.sync += self.oHandshake.eq(0)
            with m.Case(1):
                m.d.comb += self.oValid.eq(self.iValid)
                m.d.comb += self.oData.eq(self.iData)
                m.d.comb += self.oAck.eq(self.iAck)
                m.d.sync += self.oHandshake.eq(1)
            with m.Case(2):
                m.d.comb += self.oValid.eq(0)
                m.d.comb += self.oData.eq(0)
                m.d.comb += self.oAck.eq(0)
                m.d.sync += self.oHandshake.eq(1)
            with m.Default():
                m.d.comb += self.oValid.eq(0)
                m.d.comb += self.oData.eq(0)
                m.d.comb += self.oAck.eq(0)
                m.d.sync += self.oHandshake.eq(0)
                
        return m
 
 
if __name__ == "__main__":
    top = spw_pkg_guard()
    with open("spw_pkg_guard.v", "w") as f:
        f.write(verilog.convert(top, ports=[top.iHandshake, top.oHandshake, top.iValid, top.iData, top.oAck, top.oValid, top.oData, top.iAck], strip_internal_attrs=True))
        #f.write(verilog.convert(top, strip_internal_attrs=False))
