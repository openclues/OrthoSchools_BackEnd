"use strict";
console.log("hello");

const profileImg = document.querySelector("#profile-toggele-img");
const profileMenu = document.querySelector("#profile-menu");

profileImg.addEventListener("click", () => {
  if (!profileMenu.classList.contains("show")) {
    profileMenu.classList.add("show");
  } else {
    profileMenu.classList.remove("show");
  }
});
