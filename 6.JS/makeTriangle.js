// 1. 왼쪽 삼각형
function leftTriangle(n) {
  for (let i = 1; i <= n; i++) {
    console.log("*".repeat(i));
  }
}

// 2. 왼쪽 역삼각형
function leftInvertedTriangle(n) {
  for (let i = n; i > 0; i--) {
    console.log("*".repeat(i));
  }
}

// 3. 오른쪽 삼각형
function rightTriangle(n) {
  for (let i = 1; i <= n; i++) {
    console.log(" ".repeat(n - i) + "*".repeat(i));
  }
}

// 4. 오른쪽 역삼각형
function rightInvertedTriangle(n) {
  for (let i = n; i > 0; i--) {
    console.log(" ".repeat(n - i) + "*".repeat(i));
  }
}

// 5. 이등변 삼각형
function isoscelesTriangle(n) {
  for (let i = 1; i <= n; i++) {
    console.log(" ".repeat(n - i) + "*".repeat(2 * i - 1));
  }
}

// 6. 마름모
function rhombus(n) {
  isoscelesTriangle(n);
  for (let j = n - 1; j >= 1; j--) {
    console.log(" ".repeat(n - j) + "*".repeat(2 * j - 1));
  }
}

function main() {
  console.log("1. 왼쪽 삼각형");
  leftTriangle(5);
  console.log();
  /*
출력 결과:

*
**
***
****
*****

*/

  console.log("2. 왼쪽 역삼각형");
  leftInvertedTriangle(5);
  console.log();
  /*
출력 결과:

*****
****
***
**
* 

*/

  console.log("3. 오른쪽 삼각형");
  rightTriangle(5);
  console.log();
  /*
출력 결과:

    *
   **
  ***
 ****
*****

*/

  console.log("4. 오른쪽 역삼각형");
  rightInvertedTriangle(5);
  console.log();
  /*
출력 결과:

*****
 ****
  ***
   **
    *

*/

  console.log("5. 이등변 삼각형");
  isoscelesTriangle(5);
  console.log();
  /*
출력 결과:

    *
   ***
  *****
 *******
*********

*/

  console.log("6. 마름모");
  rhombus(5);
  /*
출력 결과:

    *
   ***
  *****
 *******
*********
 *******
  *****
   ***
    *

 */
}

main();
