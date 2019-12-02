import math

def calcFuel(mass):
  fuel = math.floor((mass / 3)) - 2
  return 0 if fuel <= 0 else fuel + calcFuel(fuel)


with open('day1_input.txt') as f:
  read_data = f.read().splitlines()

total_fuel_req = 0
for m in read_data:
  total_fuel_req += calcFuel(int(m))

print(total_fuel_req)