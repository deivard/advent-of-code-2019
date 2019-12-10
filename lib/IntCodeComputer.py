from enum import Enum
import time

class OPCODE(Enum): 
  HALT = 99
  ADD = 1
  MUL = 2
  INPUT = 3
  OUTPUT = 4
  JIT = 5
  JIF = 6
  LT = 7
  EQ = 8
  ADD_REL = 9

  def __eq__(self, other):
    if other.__class__ is int:
      return self.value == other
    elif other.__class__ is str:
      return str(self.value) == other
    return NotImplemented

class PARAM_MODE(Enum):
  POS = "0" # Positional
  IMM = "1" # Immediate
  REL = "2" # Relative

  def __eq__(self, other):
    if other.__class__ is str:
      return self.value == other
    elif other.__class__ is int:
      return int(self.value) == other
    return NotImplemented

class INPUT_MODE(Enum):
  MANUAL = 0
  BUFFER = 1

  def __eq__(self, other):
    if other.__class__ is int:
      return self.value == other
    return NotImplemented
  

class IntCodeComputer:
  def __init__(self, name, intCodeProgram, inputMode = INPUT_MODE.MANUAL):
    self.name = name
    self.intCodeProgram = intCodeProgram

    # Extremely intricate implementation to support large adresses
    for veryImportantVarible in range(10000):
      intCodeProgram.append(0)

    self.inputMode = inputMode
    self.inputBuffer = None
    self.latestOutput = None
    self.outputBuffer = []
    self.outputDestination = None
    self.returnCode = None
    # Program counter
    self.PC = 0
    self.relativeBase = 0
    
  def setOutputDestination(self, destination):
    self.outputDestination = destination

  def writeOutput(self):
    if self.outputDestination is None:
      self.latestOutput = self.outputBuffer[0]
      print(self.outputBuffer.pop(0))
    # else:
    #   # TODO

  def sendToInputBuffer(self, message):
    self.inputBuffer.append(message)

  # Read input from buffer or the command line (depending on the input mode)
  def readInput(self):
    if self.inputMode == INPUT_MODE.MANUAL:
      x = input()
    else: 
      # print(self.name + " is waiting for input")
      # Busy wait until there is a message in the receive buffer
      while len(self.inputBuffer) == 0:
        time.sleep(1/1000)
      # print("Buffer before read: {}".format(self.inputBuffer))
      x = self.inputBuffer.pop(0)
      # print(self.name + " read input " + str(x))
    return x

  # Read memory based on the param mode and the adress of the parameter
  def readMem(self, address, mode):
    if mode == PARAM_MODE.POS:
      return int(self.intCodeProgram[int(self.intCodeProgram[address])])
    elif mode == PARAM_MODE.IMM:
      return int(self.intCodeProgram[address])
    elif mode == PARAM_MODE.REL:
      return int(self.intCodeProgram[int(self.intCodeProgram[address]) + self.relativeBase])

  # Get the memory write position based on the param mode and the adress of the parameter
  def getWritePos(self, address, mode):
    if mode == PARAM_MODE.POS:
      return int(self.intCodeProgram[address])
    elif mode == PARAM_MODE.IMM:
      raise Exception("Invalid param mode for write position")
    elif mode == PARAM_MODE.REL:
      return int(self.intCodeProgram[address]) + self.relativeBase

  def run(self):
    while (self.PC < len(self.intCodeProgram)):
      # time.sleep(1/10) 
      opcode = int(str(self.intCodeProgram[self.PC]).replace("\n","")[-2:])
      param_modes = str(self.intCodeProgram[self.PC])[:-2]

      # Immediately check if it is a break opcode
      if opcode == OPCODE.HALT:
        break
      # print("---")
      # print("PC: {}".format(self.PC))
      # print("Param modes: " + param_modes)
      # print("Opcode: " + str(opcode) + " Parameters: " + str(self.intCodeProgram[self.PC+1]) + ", "+ str(self.intCodeProgram[self.PC+2]) + ", "+ str(self.intCodeProgram[self.PC+3]))

      param_1_mode = param_modes[-1:] or "0"
      param_2_mode = param_modes[-2:-1] or "0"
      param_3_mode = param_modes[-3:-2] or "0"

      # Add
      if opcode == OPCODE.ADD:
        self.intCodeProgram[self.getWritePos(self.PC+3, param_3_mode)] = self.readMem(self.PC+1, param_1_mode) + self.readMem(self.PC+2, param_2_mode)
        self.PC += 4
      # Multiply
      elif opcode == OPCODE.MUL:
        self.intCodeProgram[self.getWritePos(self.PC+3, param_3_mode)] = self.readMem(self.PC+1, param_1_mode) * self.readMem(self.PC+2, param_2_mode)
        self.PC += 4
        # print(self.PC)
      # Read input
      elif opcode == OPCODE.INPUT:
        self.intCodeProgram[self.getWritePos(self.PC+1, param_1_mode)] = self.readInput()
        self.PC += 2
      # Output
      elif opcode == OPCODE.OUTPUT:
        value = self.readMem(self.PC+1, param_1_mode)
        self.outputBuffer.append(value) 
        self.returnCode = value # Probably shouldnt do this here...
        self.writeOutput()
        self.PC += 2
      # Jump-if-true
      elif opcode == OPCODE.JIT:
        # If first param is non zero
        if self.readMem(self.PC+1, param_1_mode) != 0:
          # Set instruction pointer to value of param_2
          self.PC = self.readMem(self.PC+2, param_2_mode)
        else:
          # Increment normally
          self.PC += 3
      # Jump-if-false
      elif opcode == OPCODE.JIF:
        # If first param is zero
        if self.readMem(self.PC+1, param_1_mode) == 0:
          # Set instruction pointer to value of param_2
          self.PC = self.readMem(self.PC+2, param_2_mode)
        else:
          # Increment normally
          self.PC += 3
      # Less than
      elif opcode == OPCODE.LT:
        if self.readMem(self.PC+1, param_1_mode) < self.readMem(self.PC+2, param_2_mode):
          self.intCodeProgram[self.getWritePos(self.PC+3, param_3_mode)] = 1
          # self.intCodeProgram[int(self.intCodeProgram[self.PC+3])] = 1
        else:
          self.intCodeProgram[self.getWritePos(self.PC+3, param_3_mode)] = 0
          # self.intCodeProgram[int(self.intCodeProgram[self.PC+3])] = 0
        self.PC += 4
      # Equals
      elif opcode == OPCODE.EQ:
        if self.readMem(self.PC+1, param_1_mode) == self.readMem(self.PC+2, param_2_mode):
          self.intCodeProgram[self.getWritePos(self.PC+3, param_3_mode)] = 1
          # self.intCodeProgram[int(self.intCodeProgram[self.PC+3])] = 1
        else:
          self.intCodeProgram[self.getWritePos(self.PC+3, param_3_mode)] = 0
          # self.intCodeProgram[int(self.intCodeProgram[self.PC+3])] = 0
        self.PC += 4
      elif opcode == OPCODE.ADD_REL:
        self.relativeBase += self.readMem(self.PC+1, param_1_mode)
        self.PC += 2  
      else:
        raise Exception("Invalid OPCODE: {}".format(opcode))

    return self.intCodeProgram[0]