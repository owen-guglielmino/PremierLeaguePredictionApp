// Get the pop-up
var popup = document.getElementById("infoPopup");

// Get the button that opens the pop-up
var infoButton = document.getElementById("infoButton");

// Get the <span> element that closes the pop-up
var closeBtn = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the pop-up
infoButton.onclick = function() {
  popup.style.display = "block";
}

// When the user clicks on <span> (x), close the pop-up
function closePopup() {
  popup.style.display = "none";
}

// When the user clicks anywhere outside of the pop-up, close it
window.onclick = function(event) {
  if (event.target == popup) {
    popup.style.display = "none";
  }
}
