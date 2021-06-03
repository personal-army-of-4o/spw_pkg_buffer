import itertools
from spw_pkg_guard import spw_pkg_guard
from nMigen_test import mytest, runtests, helper as h, uut_iface


DEBUG = 1 == 1
VERBOSE = DEBUG

addr_width = 8
cnt_width = 32

class helper(h):
    def __init__(self):
        self.uut = uut = spw_pkg_guard()
        cfg = {
            'r': [None, uut.oValid, uut.oData, uut.iAck],
            'w': [None, uut.iValid, uut.iData, uut.oAck],
        }
        self.ui = ui = uut_iface(cfg, VERBOSE)
        super().__init__()

@mytest
class handshake_test(helper):
    def get_test_processes(self):
        uut = self.uut
        pkg0 = self.gen(20)
        pkg1 = self.gen(20)
        def rd():
            yield uut.iHandshake.eq(1)
            while (yield uut.oHandshake) == 0:
                yield from self.ticks(1)
        return [self.uut, [rd]]

@mytest
class one_pkg_test(helper):
    def get_test_processes(self):
        uut = self.uut
        pkg0 = self.gen(20)
        pkg1 = self.gen(20)
        def wr():
            yield from self.wr(pkg0)
        def rd():
            yield uut.iHandshake.eq(1)
            while (yield uut.oHandshake) == 0:
                yield from self.ticks(1)
            yield from self.rd(pkg1)
            yield uut.iHandshake.eq(0)
            while (yield uut.oHandshake) == 1:
                yield from self.ticks(1)
            yield uut.iHandshake.eq(0)
        return [self.uut, [wr, rd]]

@mytest
class two_pkg_test(helper):
    def get_test_processes(self):
        uut = self.uut
        pkg0 = self.gen(20)
        pkg1 = self.gen(20)
        pkg2 = self.gen(20)
        pkg3 = self.gen(20)
        def wr():
            yield from self.wr(pkg0)
            yield from self.wr(pkg2)
        def rd():
            yield uut.iHandshake.eq(1)
            while (yield uut.oHandshake) == 0:
                yield from self.ticks(1)
            yield from self.rd(pkg1)
            yield uut.iHandshake.eq(0)
            while (yield uut.oHandshake) == 1:
                yield from self.ticks(1)
            yield uut.iHandshake.eq(1)
            while (yield uut.oHandshake) == 0:
                yield from self.ticks(1)
            yield from self.rd(pkg3)
            yield uut.iHandshake.eq(0)
            while (yield uut.oHandshake) == 1:
                yield from self.ticks(1)
        return [self.uut, [wr, rd]]

if __name__ == "__main__":
    print("start")
    runtests(debug = DEBUG)
    print("done")

