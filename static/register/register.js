// 1/ getting the error nodes.
// 2/ looping through the error nodes and getting the corresponding input element for each error node.
// 3/ appending the error node to its corresponding input element.

document
  .querySelectorAll("ul.errorlist")
  .forEach((err) => err.nextElementSibling.appendChild(err));
