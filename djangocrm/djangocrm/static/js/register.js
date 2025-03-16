const usernameField = document.getElementById("idUsername");
const useremailField = document.getElementById("idEmail");
const usernameFeedback = document.querySelector(".usernameFeedback");
const useremailFeedback = document.querySelector(".useremailFeedback");

// Validate Username
usernameField.addEventListener("focusout", (event) => {
  let usernameValue = event.target.value;

  usernameField.classList.remove("is-invalid");
  usernameFeedback.style.display = "none";

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
          usernameFeedback.innerHTML = `<p>${data.username_error}<p>`;
          usernameFeedback.style.display = "block";
        }
      });
  }
});

//Validate email
useremailField.addEventListener("focusout", (event) => {
  let useremailValue = event.target.value;

  useremailField.classList.remove("is-invalid");
  useremailFeedback.style.display = "none";

  if (useremailValue.length > 0) {
    fetch("/authentication/email-validation", {
      body: JSON.stringify({ email: useremailValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.useremail_error) {
          useremailField.classList.add("is-invalid");
          useremailFeedback.innerHTML = `<p>${data.useremail_error}<p>`;
          useremailFeedback.style.display = "block";
        }
      });
  }
});
