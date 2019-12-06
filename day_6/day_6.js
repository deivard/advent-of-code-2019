var fs = require('fs');


class Planet {
  constructor(name, orbits) {
    this.name = name
    // this.orbits = orbits
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


// Recursive function that traverse all planets to find orbittedPlanet and then add orbitterName to that planet's orbittingPlanets array
// Always start from COM to traverse all the planets
function addOrbitter(currentPlanet, planetToOrbit, orbitterName){
  // console.log("addOrbitter called with parameters: " + currentPlanet + ", " + planetToOrbit + ", " + orbitterName)
  if (currentPlanet.name == planetToOrbit){
    // Add the planet to the orbitting array
    currentPlanet.orbittingPlanets.push(new Planet(orbitterName))
    console.log("Added orbitter: " + orbitterName + " to planet: " + planetToOrbit)
    // Return true to break out of the for loop below
    return true
  }
  else {
    for (let p of currentPlanet.orbittingPlanets){
      if (addOrbitter(p, planetToOrbit, orbitterName) == true) break
    }
  }
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

var inputData 
var planetPairs = new Array()
inputData = fs.readFileSync('input.txt', 'utf8').split("\n")
// inputData = fs.readFileSync('testData.txt', 'utf8').split(/\r?\n\r?/)

// Create the planetPairs array that is filled with planet-orbitter objects
inputData.forEach(element => {
  var [planet, orbitter] = element.split(")")
  // console.log(planet + " orbitted by " + orbitter)
  planetPairs.push({planet: planet, orbitter: orbitter})
});

// To find the planet orbitting "COM" we do a search with the findPlanetPairs function.
// If we leave the orbitterName parameter empty (empty string) we will get all pairs that have "COM" as the planetToOrbit
// var pairs = findPlanetPairs(planetPairs, "COM", "")
// console.log(findPlanetPairs(planetPairs, "COM", ""))
// var COM = new Planet("COM")
// pairs.forEach( pair => {
//   COM.orbittingPlanets.push(new Planet(pair.orbitter))
// })
// console.log(COM)

// Create the planet with planet name, a planet is created when all orbitting plannets have been added to the planet's orbittingPlanets array,
// so this function is recursive.
// NOTE: This function is based on the planetPairs array, which is based on the input from input.txt
function createPlanet(planetName) {
  // To find the planet orbitting planetName we do a search with the findPlanetPairs function.
  // If we leave the orbitterName parameter empty (empty string) we will get all pairs that have planetName as the planetToOrbit
  pairs = findPlanetPairs(planetPairs, planetName, "")
  var planet =  new Planet(planetName)
  pairs.forEach(pair => {
    // Add all the orbitting planet, after the planets orbitting that planet have been added, after the planets orbitting that planet have been added, after the ... 
    planet.orbittingPlanets.push(createPlanet(pair.orbitter))
  })
  return planet
}

var com = createPlanet("COM")
// printOrbitterMap(com)
console.log("Direct and indirect orbits: " + countDirectAndIndirectOrbits(com, 0))
// console.log(addPlanet("COM"))

// console.log(COM)
// printOrbitterMap(COM)



