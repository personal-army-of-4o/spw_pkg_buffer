import itertools
from spw_pkg_guard import spw_pkg_guard
from nMigen_test import mytest, runtests, helper, uut_iface


DEBUG = False
VERBOSE = DEBUG

addr_width = 8
cnt_width = 32

@mytest
class handshake_test(helper):
    def get_test_processes(self):
        self.ui = ui = uut_iface(spw_pkg_guard(), VERBOSE)
        pkg0 = self.gen(20)
        pkg1 = self.gen(20)
        def rd():
            yield ui.uut.iHandshake.eq(1)
            while (yield ui.uut.oHandshake) == 0:
                yield from self.ticks(1)
        return (ui.uut, [rd])

@mytest
class one_pkg_test(helper):
    def get_test_processes(self):
        self.ui = ui = uut_iface(spw_pkg_guard(), VERBOSE)
        pkg0 = self.gen(20)
        pkg1 = self.gen(20)
        def wr():
            yield from self.wr_pkg(pkg0)
        def rd():
            yield ui.uut.iHandshake.eq(1)
            while (yield ui.uut.oHandshake) == 0:
                yield from self.ticks(1)
            yield from ui.di_rd.Read(pkg1)
            yield ui.uut.iHandshake.eq(0)
            while (yield ui.uut.oHandshake) == 1:
                yield from self.ticks(1)
            yield ui.uut.iHandshake.eq(0)
        return (ui.uut, [wr, rd])

@mytest
class two_pkg_test(helper):
    def get_test_processes(self):
        self.ui = ui = uut_iface(spw_pkg_guard(), VERBOSE)
        pkg0 = self.gen(20)
        pkg1 = self.gen(20)
        pkg2 = self.gen(20)
        pkg3 = self.gen(20)
        def wr():
            yield from self.wr_pkg(pkg0)
            yield from self.wr_pkg(pkg2)
        def rd():
            yield ui.uut.iHandshake.eq(1)
            while (yield ui.uut.oHandshake) == 0:
                yield from self.ticks(1)
            yield from ui.di_rd.Read(pkg1)
            yield ui.uut.iHandshake.eq(0)
            while (yield ui.uut.oHandshake) == 1:
                yield from self.ticks(1)
            yield ui.uut.iHandshake.eq(1)
            while (yield ui.uut.oHandshake) == 0:
                yield from self.ticks(1)
            yield from ui.di_rd.Read(pkg3)
            yield ui.uut.iHandshake.eq(0)
            while (yield ui.uut.oHandshake) == 1:
                yield from self.ticks(1)
        return (ui.uut, [wr, rd])

if __name__ == "__main__":
    print("start")
    runtests(debug = DEBUG)
    print("done")

