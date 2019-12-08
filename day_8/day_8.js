var fs = require('fs');

class Image {
  constructor(pixels, width, height) {
    this.pixels = pixels
    this.width = width
    this.height = height
  }
  
}

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

// Decode the image by stacking all the layers
function decodeImage(layers) {
  var imgLength = layers[0].length
  var imagePixels = new Array(imgLength)

  for(var i = 0; i < imgLength; ++i){
    // console.log("imagePixels")
    var renderedPixel = 2 // Transparent
    for(var l = 0; l < layers.length; ++l){
      var pixel = layers[l][i]
      if (pixel != 2){
        renderedPixel = pixel
        l = layers.length
      }
    }
    imagePixels[i] = renderedPixel
  }
  return imagePixels.join("")
}

// Render the image object to the screen
function renderImage(img){
  for(var h = 0; h < img.height; ++h) {
    // Replace the 1s (white) and 0s (black) with easier to read characters
    var modifiedPixels = img.pixels.replace(/0/g, " ").replace(/1/g, "\u25CF")
    console.log(modifiedPixels.slice(h*img.width, (h+1)*img.width))
  }
}


// var inputData = "123456789012"
var [width, height] = [25,6]
var inputData = fs.readFileSync('input.txt', 'utf8').replace("\n", "")

var leastZeroes = {zeroes: null, layer: null}
var layers = separateLayers(inputData, width, height)
for (var l of layers){
  var zeroes = countOccurences(l, "0")
  if (zeroes < leastZeroes.zeroes || leastZeroes.zeroes == null) {
    leastZeroes.zeroes = zeroes
    leastZeroes.layer = l
  }
}

// console.log(leastZeroes)
// var ones = countOccurences(leastZeroes.layer, "1")
// var twos = countOccurences(leastZeroes.layer, "2")
// console.log(ones + " * " + twos + " = " + ones*twos)

var decodedPixels = decodeImage(layers)
var img = new Image(decodedPixels, width, height)
renderImage(img)

