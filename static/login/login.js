// 1/ getting the error nodes.
// 2/ looping through the error nodes and getting the corresponding input element for each error node.
// 3/ appending the error node to its corresponding input element.

document
  .querySelectorAll("ul.errorlist")
  .forEach((err) => err.nextElementSibling.appendChild(err));


const remember_me = (document.querySelector("#id_remember").parentNode)
remember_me.style.display = "flex";
remember_me.style.flexDirection = "row"
remember_me.style.alignItems = "center"
remember_me.style.justifyContent = "space-between"




document.querySelector("p").querySelector("label").textContent="Username or Email"