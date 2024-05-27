document.getElementById("user-login-form").addEventListener("submit",function(event){
    event.preventDefault(); 
    var loginformData = {
        "username": document.getElementById("username").value,
        "password": document.getElementById("password").value
    }
    let xhr = new XMLHttpRequest()
    let form = JSON.stringify(loginformData)
    xhr.open("POST","/login",true)
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
        // Request was successful, handle response.
        // Redirect the user to the products page
        window.location.href = "/products";
    } else {
        // Request failed, handle errors.
        console.error("Request failed with status:", xhr.status);
    }
};
    xhr.send(form)
})