var start = 278384
var end = 824795

var validPasswords = []


function checkAdjacency(num){
  var numString = String(num)
  // For the first two numbers we only need to check the next number if it breaks the criteria (critera from part two)
  if (numString[0] == numString[1] && numString[1] != numString [2])
    return true
  // For the last two numbers we only need to check the previous number if it breaks the criteria 
  if (numString[numString.length-1] == numString[numString.length-2] && numString[numString.length-2] != numString [numString.length-3])
    return true

  for (var i = 1; i < numString.length-2; ++i){
    // Critera from part one
    if (numString[i] == numString[i+1]){
      // Criteria from part two: "the two adjacent matching digits are not part of a larger group of matching digits"
      if(numString[i+1] != numString[i+2] && numString[i] != numString[i-1])
        return true
    }
  }
  return false
}

function checkIncreasing(num){
  numString = String(num)
  for (var i = 0; i < numString.length-1; ++i){
    if (parseInt(numString[i]) > parseInt(numString[i+1]))
      return false
  }
  return true
}

console.log(checkAdjacency(112233))
console.log(checkAdjacency(123444))
console.log(checkAdjacency(111122))

console.log(checkIncreasing(1223))
console.log(checkIncreasing(12323))
console.log(checkIncreasing(111211))

for (var i = start; i <= end; ++i) {
  if (checkAdjacency(i) && checkIncreasing(i))
    validPasswords.push(i)
  
}
console.log(validPasswords.length)

