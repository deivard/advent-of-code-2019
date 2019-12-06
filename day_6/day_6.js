var fs = require('fs');


class Planet {
  constructor(name, orbits) {
    this.name = name
    this.orbits = orbits // Planet
    this.orbittingPlanets = new Array()
  }
}

function findPlanetPairs(planetPairs, planetToOrbit, orbitterName){
  var matches = new Array()
  for (let pair of planetPairs){
    if ((planetToOrbit == '' || planetToOrbit == pair.planet) && (orbitterName == '' || orbitterName == pair.orbitter))
      matches.push(pair)
  }
  return matches
}

// Create the planet with planet name, a planet is created when all orbitting plannets have been added to the planet's orbittingPlanets array,
// so this function is recursive.
// NOTE: This function is based on the planetPairs array, which is based on the input from input.txt
function createPlanet(planetName, orbits) {
  // To find the planet orbitting planetName we do a search with the findPlanetPairs function.
  // If we leave the orbitterName parameter empty (empty string) we will get all pairs that have planetName as the planetToOrbit
  pairs = findPlanetPairs(planetPairs, planetName, "")
  var planet =  new Planet(planetName)
  planet.orbits = orbits
  pairs.forEach(pair => {
    // Add all the orbitting planet, after the planets orbitting that planet have been added, after the planets orbitting that planet have been added, after the ... 
    planet.orbittingPlanets.push(createPlanet(pair.orbitter, planet))
  })
  return planet
}


// Recursive function that prints the planet, and then goes in to all the orbitting planets and prints them and their orbitting planets etc etc
function printOrbitterMap(startPlanet){
  console.log(startPlanet)
  startPlanet.orbittingPlanets.forEach(planet => {
    printOrbitterMap(planet)
  })
}

// Recursion wtf super cool
function countDirectAndIndirectOrbits(startPlanet, stepsTaken){
  var sum = stepsTaken
  startPlanet.orbittingPlanets.forEach(planet => {
    sum += countDirectAndIndirectOrbits(planet, stepsTaken+1)
  })
  return sum
}

function findYOU(planet) {
  // console.log(planet)
  if (planet.name == "YOU")
    return planet
  for (let p of planet.orbittingPlanets){
    var result = findYOU(p)
    if (result != undefined)
      return result
  }
}

// Start at the planet YOU orbits, with prevPlanet = YOU, 
function stepToSAN(planet, path, numTransfers, pathToSAN){
  // console.log(path)
  // We moved to new planet, so add it to the path
  path.push(planet.name)
  // and add 1 to the steps counter
  numTransfers += 1

  var validMoves = new Array()
  // Find all possible moves from current planet (moving back to the previous planet is not a valid move)
  for (var orbitter of planet.orbittingPlanets) {
    // First we check if we are at the planet that SAN orbits
    if (orbitter.name == "SAN")
      // 
      return {transfers: numTransfers, path: path}
  
    // All orbitting planets around this planet is a valid move (except the planets you have visited)
    if (path.includes(orbitter.name) == false)
      validMoves.push(orbitter)
  }
  // The planet that this planet orbits is also a valid move (unless it is undefined, which it will be when the planet is COM)
  // or if we have visited it already
  if (planet.orbits != undefined && path.includes(planet.orbits.name) == false)
    validMoves.push(planet.orbits)
  
  // console.log(validMoves)
  // Explore all valid moves 
  for (let targetPlanet of validMoves){
    var result = stepToSAN(targetPlanet, path, numTransfers)
    // console.log(result)
    if (result)
      return result
  }
}







var planetPairs = new Array()
var inputData = fs.readFileSync('input.txt', 'utf8').split("\n")
// inputData = fs.readFileSync('testData.txt', 'utf8').split(/\r?\n\r?/)

// Create the planetPairs array that is filled with planet-orbitter objects
inputData.forEach(element => {
  var [planet, orbitter] = element.split(")")
  // console.log(planet + " orbitted by " + orbitter)
  planetPairs.push({planet: planet, orbitter: orbitter})
});

var COM = createPlanet("COM", null)
// printOrbitterMap(COM)
// console.log("Direct and indirect orbits: " + countDirectAndIndirectOrbits(COM, 0))

var YOU = findYOU(COM)
// Start at -1 steps since the recursive function counts the steps from YOU to the planet that SAN is orbitting
console.log(stepToSAN(YOU.orbits, ["YOU"], -1))

// console.log(addPlanet("COM"))




