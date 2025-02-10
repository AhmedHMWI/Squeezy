const passwordPattern = /(?=^.{10,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z\d])/;
const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
const usernamePattern = /^\S+$/;

// Login form validation
function validateLoginForm() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const errorMessage = document.getElementById("error-message");

  errorMessage.style.display = "none";
  errorMessage.innerHTML = "";

  if (!email && !password) {
    errorMessage.style.display = "block";
    errorMessage.innerHTML = "All fields are required.";
    return false;
  }
  if (!email.match(emailPattern)) {
    errorMessage.style.display = "block";
    errorMessage.innerHTML = "Please enter a valid email address.";
    return false;
  }

  if (!password) {
    errorMessage.style.display = "block";
    errorMessage.innerHTML = "Password cannot be empty.";
    return false;
  }

  return true;
}



// register from validation
function validateRegisterForm() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
  
    const nameError = document.getElementById("name-error");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");
    const confirmPasswordError = document.getElementById(
      "confirm_password-error"
    );
    let count = 0;
  
    nameError.innerHTML = "";
    emailError.innerHTML = "";
    passwordError.innerHTML = "";
    confirmPasswordError.innerHTML = "";
  
    if (!name) {
      nameError.innerHTML = "Name cannot be empty.";
      count++;
    }

    if (!email) {
      emailError.innerHTML = "Email cannot be empty.";
      count++;
    } else if (!email.match(emailPattern)) {
      emailError.innerHTML = "Please enter a valid email address.";
      count++;
    }
  
    if (!password) {
      passwordError.innerHTML = "Password cannot be empty.";
      count++;
    } else if (!password.match(passwordPattern)) {
      passwordError.innerHTML =
        "Password must be at least 10 characters, contain one uppercase letter, one lowercase letter, one digit, and one special character.";
      count++;
    }
  
    if (!confirm_password) {
      confirmPasswordError.innerHTML = "Confirm Password cannot be empty.";
      count++;
    }
    if (password != confirm_password) {
      confirmPasswordError.innerHTML = "Passwords do not match.";
      count++;
    }
    // return count < 0
    if (count > 0) {
      return false;
    }
    return true;
  }