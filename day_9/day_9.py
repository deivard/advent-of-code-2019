import sys
sys.path.insert(1, 'lib')
import IntCodeComputer

def main():
  f = open("day_9/input.txt", "r")
  input_day9 = f.read().split(",")
  # input_day9 = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split()
  # input_day9 = "1102,34915192,34915192,7,4,7,99,0".split(",")
  # input_day9 = "104,1125899906842624,99".split(",")

  computer = IntCodeComputer.IntCodeComputer("Day9", input_day9)
  value = computer.run()

  print("Return code = {}".format(value))

if __name__ == "__main__":
  main()