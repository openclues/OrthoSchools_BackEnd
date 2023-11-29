"use strict";
console.log("hello");

const profileImg = document.querySelector("#profile-toggele-img");
const profileMenu = document.querySelector("#profile-menu");
// body.addEventListener("click", function () {
//   // dropDown.classList.remove("show");
// });
profileImg.addEventListener("click", () => {
  if (!profileMenu.classList.contains("show")) {
    profileMenu.classList.add("show");
  } else {
    profileMenu.classList.remove("show");
  }
});
console.log("hello");