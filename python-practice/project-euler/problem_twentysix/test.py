import main


def test_repeating_string():
    input_string = "1234123412341234"
    expected = "1234"
    received = main.repeating_sequence(input_string)
    assert expected == received

    input_string = "1234"
    expected = "1234"
    received = main.repeating_sequence(input_string)
    assert expected == received

    input_string = "0.14285714285714285"
    expected = "142857"
    received = main.repeating_sequence(input_string)
    assert expected == received

    input_string = "zachzachzach"
    expected = "zach"
    received = main.repeating_sequence(input_string)
    assert expected == received

    input_string = "666"
    expected = "6"
    received = main.repeating_sequence(input_string)
    assert expected == received

    input_string = "0.1666666"
    expected = "6"
    received = main.repeating_sequence(input_string)
    assert expected == received

    input_string = "0.11111111111"
    expected = "1"
    received = main.repeating_sequence(input_string)
    assert expected == received
