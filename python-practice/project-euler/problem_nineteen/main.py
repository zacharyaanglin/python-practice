"""Solve Euler problem nineteen."""

import copy

months = {
  0: 31,
  1: 28,
  2: 31,
  3: 30,
  4: 31,
  5: 30,
  6: 31,
  7: 31,
  8: 30,
  9: 31,
  10: 30,
  11: 31,
}

months_leap = copy.deepcopy(months)
months_leap[1] = 29

def is_leap_year(year: int) -> bool:
  """Determine if a year is a leap year."""
  if year % 4 != 0:
    return False
  if year % 400 == 0:
    return True
  if year % 100 == 0:
    return False
  if year % 4 == 0:
    return True
  raise AssertionError("Unreachable condition reached!")

if __name__ == '__main__':

  day = 6
  first_sunday_count = 0

  for year in range(1901, 2001):

    months_in_year = months_leap if is_leap_year(year) else months
    for month in months_in_year.keys():
      if day == 1:
        first_sunday_count += 1
        print(year, month + 1, first_sunday_count)
      while day // months_in_year[month] == 0:
        day += 7
      day = day % months_in_year[month]
      # if day == 1 and month + 1 < 12:
      #   first_sunday_count += 1
      #   print(year, month + 1)
  
  print('There are {} month-leading Sundays!'.format(first_sunday_count))

