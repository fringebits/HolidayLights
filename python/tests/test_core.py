from holidaylights.core import NuTimer, House, HOA, HouseMode


def test_nutimer_expiration():
    t = NuTimer(0)
    t.reset(0)  # immediate expiration
    assert t.is_expired() is True


def test_house_modes():
    h = House(0, 2)
    assert h.m_mode == HouseMode.NormalMode
    h.set_mode(HouseMode.PartyMode)
    assert h.m_mode == HouseMode.PartyMode
    h.set_mode(HouseMode.NormalMode)
    assert h.m_mode == HouseMode.NormalMode


def test_hoa_basic():
    houses = [House(0,1) for _ in range(3)]
    hoa = HOA(houses, 3, 0)
    # one update should not crash
    class Dummy:
        def set_pixel(self, i, c):
            pass
    hoa.update(Dummy())
