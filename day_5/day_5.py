def startIntcodeProgram(inputIntCode):
    # (Same structure as R-value instructions)
    # 5,6,7,8 aren't actually the same structure as R-value isntructions but cba to change...
    r_value_instructions = [1,2,5,6,7,8]
    i = 0
    while (i < len(inputIntCode)):
      print("Adress: " + str(i))
      opcode = int(str(inputIntCode[i])[-2:])
      param_modes = str(inputIntCode[i])[:-2]
      print("Opcode: " + str(opcode))
      # Immediately check if it is a break opcode
      if opcode == 99:
          break
      print("Param modes: " + param_modes)
      print("Parameters: " + str(inputIntCode[i+1]) + ", "+ str(inputIntCode[i+2]) + ", "+ str(inputIntCode[i+3]))
      print("---")

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
        inputIntCode[int(inputIntCode[i+1])]  = str(input("Input: "))
        i += 2
      # Print
      elif opcode == 4:
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



if __name__ == "__main__":

  # test_input1 = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")
  # startIntcodeProgram(test_input1)
  f = open("input.txt", "r")
  input_day5 = f.read().split(",")
  startIntcodeProgram(input_day5)






