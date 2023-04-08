const loginSelect = document.querySelector(".pill-login");
const registerSelect = document.querySelector(".pill-register");

loginSelect.addEventListener("click", () => {
  registerSelect.classList.remove("active");
  loginSelect.classList.add("active");
  document.querySelector(".register-content").style.display = "none";
  document.querySelector(".login-content").style.display = "block";
});

registerSelect.addEventListener("click", () => {
  loginSelect.classList.remove("active");
  registerSelect.classList.add("active");
  document.querySelector(".register-content").style.display = "block";
  document.querySelector(".login-content").style.display = "none";
});