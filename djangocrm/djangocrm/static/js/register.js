const usernameField = document.getElementById("idUsername");

usernameField.addEventListener("focusout", (event) => {
  let usernameValue = event.target.value;
  if (usernameValue.length > 0) {
    fetch("/authentication/username-validation", {
      body: JSON.stringify({ username: usernameValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
        } else {
          usernameField.classList.remove("is-invalid");
        }
      });
  }
});
