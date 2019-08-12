import main


def test_can_be_sum_of_two_nums():
    num_list = [12, 18, 20, 24, 30, 36, 40, 42, 48, 54, 56]
    num = 82
    expected = True
    received = main.can_be_sum_of_two_nums(num, num_list)

    num = 80
    expected = False
    received = main.can_be_sum_of_two_nums(num, num_list)
