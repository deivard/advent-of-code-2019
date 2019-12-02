def startIntcodeProgram(input):
    i = 0
    while (i < len(input)):
        if int(input[i]) == 1:
            input[int(input[i+3])] = int(input[int(input[i+1])]) + int(input[int(input[i+2])])
        if int(input[i]) == 2:
            input[int(input[i+3])] = int(input[int(input[i+1])]) * int(input[int(input[i+2])])
        if int(input[i]) == 99:
            break
        i += 4
    return input[0]



if __name__ == "__main__":

    # print(startIntcodeProgram(f.read().split(",")))
    for verb in range(100):
        for noun in range(100):
            # Open every time cuz wtf when and why do f go out of scope?!
            f = open("input.txt", "r")
            # Read from the file to reset the input
            input_day2 = f.read().split(",")
            input_day2[1] = noun
            input_day2[2] = verb

            # print("Verb: " + str(verb) + " and noun: " + str(noun))
            result = startIntcodeProgram(input_day2)
            if(int(result) == 19690720):
                print("Verb: " + str(verb) + " and noun: " + str(noun) + " produces " + "19690720")
                print("Answer: 100 * noun + verb = " + str((100*int(noun))+int(verb)))
                break






