// Add this script to your HTML file
function clicks(params) {
  // Show the spinner
  document.getElementById("spinner").style.visibility = "visible";

  // Disable the button
  document.getElementById("updateButton").disabled = true;

  // Make the API call to update the database
  // Replace '/update' with the URL of your API endpoint
  fetch("/add_movie")
    .then((response) => {
      // Hide the spinner
      document.getElementById("spinner").style.visibility = "hidden";
      location.reload();

      // Enable the button
      document.getElementById("updateButton").disabled = false;

      // Handle the response from the API endpoint
      if (response.ok) {
      } else {
        alert("Error updating database");
      }
    })
    .catch((error) => {
      // Handle any errors that occur during the API call
      console.error("Error calling API", error);

      // Hide the spinner
      document.getElementById("spinner").style.visibility = "hidden";

      // Enable the button
      document.getElementById("updateButton").disabled = false;

      // Show an error message to the user
      alert("An error occurred while updating the database");
    });
}
