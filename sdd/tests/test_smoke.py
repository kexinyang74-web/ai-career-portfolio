"""工具链冒烟测试：证明 pytest/pyright 环境可用。"""


def test_toolchain_ready() -> None:
    assert 1 + 1 == 2
