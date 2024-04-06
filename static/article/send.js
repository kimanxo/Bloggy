
const send = document.querySelector("#send");
const input = document.querySelector(".input_box");
if (send && input){
  send.style.display = "none";
  input.addEventListener("input", (x) =>
    x.target.value
      ? (send.style.display = "block")
      : (send.style.display = "none")
  );
}