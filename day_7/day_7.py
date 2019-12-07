import itertools
import time
import threading

class Amplifier:
  def __init__(self, name, initialReceiveBuffer, intCodeProgram):
    self.name = name
    self.intCodeProgram = intCodeProgram
    # Send the phasesignal to the buffed so the first input that is read is the phase signal
    # Copy the initial buffer to the receive buffer (The initial buffer will contain the phase signal, and possibly a 0 if it is the first amplifier)
    self.receiveBuffer = initialReceiveBuffer.copy()
    
    self.nextAmplifier = None
    self.thruster = None
    self.latestOutput = None
    

  def connectToNextAmplifier(self, nextAmplifier):
    self.nextAmplifier = nextAmplifier

  # The thruster is just a variable that stores the output
  def connectToThruster(self, thruster):
    self.thruster = thruster

  def receive(self, message):
    self.receiveBuffer.append(message)

  def sendOutput(self, output, target):
    if isinstance(target, Amplifier):
      # print(self.name + " sending output to " + target.name)
      target.receive(output)
    else:
      print(self.name + " sending output ({}) to thruster".format(output))
      target[0] = output

  # Continiously check if the receiveBuffer contains any data and then returns the first data
  def awaitInput(self):
    # print(self.name + " is waiting for input")
    while len(self.receiveBuffer) == 0:
      # Busy wait until there is a message in the receive buffer
      time.sleep(1/1000)
    # print("Buffer before read: {}".format(self.receiveBuffer))
    x = self.receiveBuffer.pop(0)
    # print(self.name + " read input " + str(x))
    return x


  def startModifiedIntcodeProgram(self):
    if self.nextAmplifier == None:
      raise Exception("Cannot start amplifier until it is connected to the next amplifier")

    # (Same structure as R-value instructions)
    # 5,6,7,8 aren't actually the same structure as R-value isntructions but cba to change...
    r_value_instructions = [1,2,5,6,7,8]
    i = 0
    while (i < len(self.intCodeProgram)):
      # time.sleep(1/100)
      # print("Adress: " + str(i))
      opcode = int(str(self.intCodeProgram[i]).replace("\n","")[-2:])
      param_modes = str(self.intCodeProgram[i])[:-2]
      # print("Amplifier {}, opcode: {}".format(self.name, opcode))
      # Immediately check if it is a break opcode
      if opcode == 99:
        # If a thruster is connected
        if (self.thruster is not None):
          # Send the last output to the thruster
          self.sendOutput(self.latestOutput, self.thruster)
        break
      # print("Param modes: " + param_modes)
      # print("Parameters: " + str(self.intCodeProgram[i+1]) + ", "+ str(self.intCodeProgram[i+2]) + ", "+ str(self.intCodeProgram[i+3]))
      # print("---")

      # Param mode 1 is immediate mode, grab the value directly
      if param_modes[-1:] == "1" :
        # Grab the immediate value
        param_1 = int(self.intCodeProgram[i+1])
      # Param mode 0 is position mode, so we load the data from the location given
      # if param_modes[-1:] returns '', we default to position mode
      else:
        # Grab the value on the given position
        param_1 = int(self.intCodeProgram[int(self.intCodeProgram[i+1])])

      # NOTE: Not all opcodes use all parameters, so we must be mindfull when trying to load the second parameter
      # Check if it is safe to handle the second parameter
      if opcode in r_value_instructions:
        # Same principle for param_2
        if param_modes[-2:-1] == "1":
          # Grab the immediate value
          param_2 = int(self.intCodeProgram[i+2])
        # Param mode 0 is position mode, so we load the data from the location given
        # if param_modes[-1:] returns '', we default to position mode
        else:
          # Grab the value on the given position
          param_2 = int(self.intCodeProgram[int(self.intCodeProgram[i+2])])

      # Param 3 will always be position mode so we dont need to handle that param.

      # Add
      if opcode == 1:
        self.intCodeProgram[int(self.intCodeProgram[i+3])] = param_1 + param_2
        i += 4
      # Multiply
      elif opcode == 2:
        self.intCodeProgram[int(self.intCodeProgram[i+3])] = param_1 * param_2
        i += 4
      # Read input
      elif opcode == 3:
        self.intCodeProgram[int(self.intCodeProgram[i+1])] = self.awaitInput()
        i += 2
      # Print
      elif opcode == 4:
        self.latestOutput = param_1 # Store the latest output so we can forward it to the thruster (if we are connected to one) when the program halts
        self.sendOutput(param_1, self.nextAmplifier)
        i += 2
      # Jump-if-true
      elif opcode == 5:
        # If first param is non zero
        if param_1 != 0:
          # Set instruction pointer to value of param_2
          i = param_2
        else:
          # Increment normally
          i += 3
      # Jump-if-false
      elif opcode == 6:
        # If first param is zero
        if param_1 == 0:
          # Set instruction pointer to value of param_2
          i = param_2
        else:
          # Increment normally
          i += 3
      # Less than
      elif opcode == 7:
        if param_1 < param_2:
          self.intCodeProgram[int(self.intCodeProgram[i+3])] = 1
        else:
          self.intCodeProgram[int(self.intCodeProgram[i+3])] = 0
        i += 4
      # Equals
      elif opcode == 8:
        if param_1 == param_2:
          self.intCodeProgram[int(self.intCodeProgram[i+3])] = 1
        else:
          self.intCodeProgram[int(self.intCodeProgram[i+3])] = 0
        i += 4

    return self.intCodeProgram[0]


if __name__ == "__main__":
  # Test input
  # input_day6 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(",")
  # permutations = [[9,8,7,6,5],[8,9,7,6,5]]

  originalSequence = [0,1,2,3,4]
  partTwoSequence = [5,6,7,8,9]

  permutations = itertools.permutations(partTwoSequence)

  f = open("input.txt", "r")
  input_day6 = f.read().split(",")

  highestSignal = 0
  # For all permutations
  for p in permutations:
    # Reset the data every time we try a new permutation
    data = [input_day6.copy(),input_day6.copy(),input_day6.copy(),input_day6.copy(),input_day6.copy()]
    # The output variable represent the thruster input
    output = [0] # Hacky solution to send mutable object 
    # For each amp (one dataset represents an amp)
    # Performs the amp sequence
    AmpA = Amplifier("A", [p[0],0], data[0])
    AmpB = Amplifier("B", [p[1]], data[1])
    AmpC = Amplifier("C", [p[2]], data[2])
    AmpD = Amplifier("D", [p[3]], data[3])
    AmpE = Amplifier("E", [p[4]], data[4])
    AmpA.connectToNextAmplifier(AmpB)
    AmpB.connectToNextAmplifier(AmpC)
    AmpC.connectToNextAmplifier(AmpD)
    AmpD.connectToNextAmplifier(AmpE)
    AmpE.connectToNextAmplifier(AmpA)

    AmpE.connectToThruster(output)

    threads = []
    for amp in [AmpA, AmpB, AmpC, AmpD, AmpE]:
      t = threading.Thread(target=amp.startModifiedIntcodeProgram, args=())
      threads.append(t)
      t.start()
    
    for t in threads:
      t.join()

    # print(output)
    if output[0] > highestSignal:
      highestSignal = output[0]

  print("Highest signal: " + str(highestSignal))


    









