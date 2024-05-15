
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





const comments_section = document.querySelector(".comments")

comments_section.addEventListener("htmx:afterSwap", function (event) {
  comments_section.querySelector(".input_box").value = ""
});