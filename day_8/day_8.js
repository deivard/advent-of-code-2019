var fs = require('fs');

function separateLayers(input, width, height) {
  var layers = []

  var pixelsPerLayer = width*height  
  var numLayers = input.length / pixelsPerLayer
  // console.log(numLayers)

  for (var l = 0; l < numLayers; ++l){
    layers.push(input.slice(l*pixelsPerLayer, (l+1)*pixelsPerLayer))
  }

  return layers
}


function countOccurences(layer, char) {
  var re = new RegExp(char, 'g')
  var res = layer.match(re)
  return res ? res.length : 0
}


// var inputData = "123456789012"
var [width, height] = [25,6]
var inputData = fs.readFileSync('input.txt', 'utf8').replace("\n", "")

var leastZeroes = {zeroes: null, layer: null}
for (var l of separateLayers(inputData, width, height)){
  var zeroes = countOccurences(l, "0")
  if (zeroes < leastZeroes.zeroes || leastZeroes.zeroes == null) {
    leastZeroes.zeroes = zeroes
    leastZeroes.layer = l
  }
}

console.log(leastZeroes)
var ones = countOccurences(leastZeroes.layer, "1")
var twos = countOccurences(leastZeroes.layer, "2")
console.log(ones + " * " + twos + " = " + ones*twos)