from analyzer.utils.permissions import (
    generate_full_write_combination,
    generate_single_write_combination,
)


def test_generate_single_write_combination():
    result = generate_single_write_combination()
    assert len(result) == 4
    assert "-w-" in result
    assert "rwx" in result
    assert "-wx" in result
    assert "rw-" in result


def test_generate_full_write_combination():
    result = generate_full_write_combination()
    assert len(result) == 64  # 4 * 4 * 4 for the combinations (owner, group, others)
    assert "r--r--r--" not in result
    assert "-w--w--w-" in result
    assert "--x--x--x" not in result
    assert "rwxrwxrwx" in result
    assert "-wx-wx-wx" in result
