# cuz global variables mane
shortest_steps_intersection = 999999

def transformToCoordinates(wire_data):
  coords = list(tuple())
  # Starting position
  coords.append((0, 0)) # (x, y), accessed via coords[i][0|1]
  # Next position is at index 1
  index = 1
  for w in wire_data:
    # Get the direction
    direction = w[0]
    value = int(w[1:])
    # "U" changes the Y coordinate by adding the value to the previous Y
    if direction == "U":
      # The position at "index" is dependant on the previous position
      coords.append((coords[index-1][0], coords[index-1][1] + value))
    # "D" = current Y - value
    if direction == "D":
      coords.append((coords[index-1][0], coords[index-1][1] - value))
    # "R" = current X + value
    if direction == "R":
      coords.append((coords[index-1][0] + value, coords[index-1][1]))
    # "L" = current X - value
    if direction == "L":
      coords.append((coords[index-1][0] - value, coords[index-1][1]))

    index += 1

  return coords


# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
def seg_intersect(a1,a2, b1,b2):
  denomX = (((a1[0] - a2[0]) * (b1[1] - b2[1])) - ((a1[1] - a2[1])*(b1[0] - b2[0])))
  denomY = (((a1[0] - a2[0]) * (b1[1] - b2[1])) - ((a1[1] - a2[1])*(b1[0] - b2[0])))
  if denomX is 0 or denomY is 0:
    return (False, False)
  px = (((a1[0]*a2[1] - a1[1]*a2[0])*(b1[0] - b2[0])) - ((a1[0] - a2[0])*(b1[0]*b2[1] - b1[1]*b2[0]))) / denomX
  py = (((a1[0]*a2[1] - a1[1]*a2[0])*(b1[1] - b2[1])) - ((a1[1] - a2[1])*(b1[0]*b2[1] - b1[1]*b2[0]))) / denomY
  if (px >= min(a1[0], a2[0]) and px <= max(a1[0], a2[0]) ) and (py >= min(a1[1], a2[1]) and py <= max(a1[1], a2[1]) ) and \
    (px >= min(b1[0], b2[0]) and px <= max(b1[0], b2[0]) ) and (py >= min(b1[1], b2[1]) and py <= max(b1[1], b2[1]) ):
    return (px,py)
  return (False, False)

def findIntersections(fst_coords, snd_coords):
  global shortest_steps_intersection
  intersections = list(tuple())

  for i in range(len(fst_coords)-1):
    for j in range(len(snd_coords)-1):
      intersect = seg_intersect(fst_coords[i], fst_coords[i+1], snd_coords[j], snd_coords[j+1])
      # print (intersect)
      if intersect[0] is not False and (intersect[0] != 0 and intersect[1] != 0):
        intersections.append((intersect[0], intersect[1]))

        fst_steps_needed = 0
        fst_steps_i = 0
        while (fst_steps_i < i-1):
          # Calculate steps to intersection
          fst_steps_needed += (abs(fst_coords[fst_steps_i][0] - fst_coords[fst_steps_i+1][0]) +  abs(fst_coords[fst_steps_i][1] - fst_coords[fst_steps_i+1][1]))
          fst_steps_i += 1
        # Handle steps from last coord before intersection point, to the intersection
        fst_steps_needed += (abs(fst_coords[fst_steps_i][0] - intersect[0]) +  abs(fst_coords[fst_steps_i][1] - intersect[1]))

        snd_steps_needed = 0
        snd_steps_j = 0
        while (snd_steps_j < j-1):
          # Calculate steps to intersection
          snd_steps_needed += (abs(snd_coords[snd_steps_j][0] - snd_coords[snd_steps_j+1][0]) +  abs(snd_coords[snd_steps_j][1] - snd_coords[snd_steps_j+1][1]))
          snd_steps_j += 1
        # Handle steps from last coord before intersection point, to the intersection
        snd_steps_needed += (abs(snd_coords[snd_steps_j][0] - intersect[0]) +  abs(snd_coords[snd_steps_j][1] - intersect[1]))

        steps_needed = fst_steps_needed + snd_steps_needed
        if steps_needed < shortest_steps_intersection:
          shortest_steps_intersection = steps_needed


  return intersections


def getManhattanDistance(coords):
  central_port = (0,0)
  return abs(coords[0] - central_port[0]) + abs(coords[1] - central_port[1])


if __name__ == "__main__":
  f = open("input.txt", "r")
  input_data = f.read().splitlines()

  # TEST CASE
  # test0 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
  # test1 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
  # test0 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
  # test1 = "U62,R66,U55,R34,D71,R55,D58,R83"
  # test0_coords = transformToCoordinates(test0.split(","))
  # test1_coords = transformToCoordinates(test1.split(","))
  # test_intersect = findIntersections(test0_coords, test1_coords)
  # print("STEPS: " + str(shortest_steps_intersection))
  # print(test_intersect)
  # END TEST CASE
  # print((transformToCoordinates(test.split(","))[-1]))
  # fst_wire = test_data0.split(",")
  # snd_wire = test_data1.split(",")


  fst_wire = input_data[0].split(",")
  snd_wire = input_data[1].split(",")

  fst_coords = transformToCoordinates(fst_wire)
  snd_coords = transformToCoordinates(snd_wire)
  # print (fst_coords)
  # print(fst_wire)
  # print(snd_wire)

  intersections = findIntersections(fst_coords, snd_coords)
  print(intersections)

  # First distance
  shortest_distance = getManhattanDistance(intersections[0])
  for i in intersections:
    dist = getManhattanDistance(i)
    if dist < shortest_distance:
      shortest_distance = dist

  print(int(shortest_distance))

  print(shortest_steps_intersection)


