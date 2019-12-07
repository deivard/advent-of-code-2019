import itertools


def startModifiedIntcodeProgram(inputIntCode, simulatedInputs):
    # Modifications for day_7
    inputIterator = 0
    numOfInputs = len(simulatedInputs)
    # End of mods

    # (Same structure as R-value instructions)
    # 5,6,7,8 aren't actually the same structure as R-value isntructions but cba to change...
    r_value_instructions = [1,2,5,6,7,8]
    i = 0
    while (i < len(inputIntCode)):
      # print("Adress: " + str(i))
      opcode = int(str(inputIntCode[i])[-2:])
      param_modes = str(inputIntCode[i])[:-2]
      # print("Opcode: " + str(opcode))
      # Immediately check if it is a break opcode
      if opcode == 99:
          break
      # print("Param modes: " + param_modes)
      # print("Parameters: " + str(inputIntCode[i+1]) + ", "+ str(inputIntCode[i+2]) + ", "+ str(inputIntCode[i+3]))
      # print("---")

      # Param mode 1 is immediate mode, grab the value directly
      if param_modes[-1:] == "1" :
        # Grab the immediate value
        param_1 = int(inputIntCode[i+1])
      # Param mode 0 is position mode, so we load the data from the location given
      # if param_modes[-1:] returns '', we default to position mode
      else:
        # Grab the value on the given position
        param_1 = int(inputIntCode[int(inputIntCode[i+1])])

      # NOTE: Not all opcodes use all parameters, so we must be mindfull when trying to load the second parameter
      # Check if it is safe to handle the second parameter
      if opcode in r_value_instructions:
        # Same principle for param_2
        if param_modes[-2:-1] == "1":
          # Grab the immediate value
          param_2 = int(inputIntCode[i+2])
        # Param mode 0 is position mode, so we load the data from the location given
        # if param_modes[-1:] returns '', we default to position mode
        else:
          # Grab the value on the given position
          param_2 = int(inputIntCode[int(inputIntCode[i+2])])

      # Param 3 will always be position mode so we dont need to handle that param.

      # Add
      if opcode == 1:
        inputIntCode[int(inputIntCode[i+3])] = param_1 + param_2
        i += 4
      # Multiply
      elif opcode == 2:
        inputIntCode[int(inputIntCode[i+3])] = param_1 * param_2
        i += 4
      # Read input
      elif opcode == 3:
        if numOfInputs > 0 and inputIterator < numOfInputs:
          # print("Using simulated input: " + str(simulatedInputs[inputIterator]))
          inputIntCode[int(inputIntCode[i+1])]  = simulatedInputs[inputIterator] # str(input("Input: "))
          inputIterator += 1
        else:
          inputIntCode[int(inputIntCode[i+1])]  =  str(input("Input: "))
        i += 2
      # Print
      elif opcode == 4:
        return param_1 # Modified for day_7
        print(param_1) 
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
          inputIntCode[int(inputIntCode[i+3])] = 1
        else:
          inputIntCode[int(inputIntCode[i+3])] = 0
        i += 4
      # Equals
      elif opcode == 8:
        if param_1 == param_2:
          inputIntCode[int(inputIntCode[i+3])] = 1
        else:
          inputIntCode[int(inputIntCode[i+3])] = 0
        i += 4

    return inputIntCode[0]


def startAmp(intcode, simulatedInputs):
  # print("Starting amp: " + str(simulatedInputs[0]) + "(phase setting), " + str(simulatedInputs[1]))
  result = int(startModifiedIntcodeProgram(intcode, simulatedInputs))
  # print("Returning result: " + str(result))
  return result



if __name__ == "__main__":
  # Test input
  # input_day6 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(",")

  originalSequence = [0,1,2,3,4]
  permutations = itertools.permutations(originalSequence)


  f = open("input.txt", "r")
  input_day6 = f.read().split(",")
  data = [input_day6.copy(),input_day6.copy(),input_day6.copy(),input_day6.copy(),input_day6.copy()]

  # output = startAmp(data[4], [0, startAmp(data[3], [1, startAmp(data[2], [2, startAmp(data[1], [3, startAmp(data[0], [4, 0])])])])])

  # print (output)
  highestSignal = 0
  # For all permutations
  for p in permutations:
    phaseSettingIterator = 0
    output = 0
    # For each amp (one dataset represents an amp)
    # Performs the amp sequence
    for d in data:
      output = startAmp(d, [p[phaseSettingIterator], output])
      phaseSettingIterator += 1

    if output > highestSignal:
      highestSignal = output

  print("Highest signal: " + str(highestSignal))


    









