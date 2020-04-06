let {PythonShell} = require('python-shell')
let path = require("path");
const fs = require('fs');


function isEmpty(str) {
    return (!str || 0 === str.length);
}

function forwardHome(){
    window.location.href = "home.html";
}

function validateLogin(){
//    check if all fields are filled out
    let url = document.getElementById("URL");
    let userName = document.getElementById("username");
    let password = document.getElementById("password");
    let a = [];

    if(isEmpty(url.value)){
        document.getElementById('urlLabel').style.color = 'red';
    }
    else{
        document.getElementById('urlLabel').style.color = 'grey';
    }
    if(isEmpty(userName.value)){
        document.getElementById('usernameLabel').style.color = 'red';
    }
    else{
        document.getElementById('usernameLabel').style.color = 'grey';
    }
    if(isEmpty(password.value)){
        document.getElementById('passwordLabel').style.color = 'red';
    }
    else{
        document.getElementById('passwordLabel').style.color = 'grey';
    }

    let options = {
        scriptPath : 'PyEngine/',
        pythonOptions: ['-u'], // get print results in real-time
        args : [url.value, userName.value, password.value]
    };

    let pyshell = new PythonShell('login.py', options);
    let answer = "";
    pyshell.on('message', function(message) {
        //receive true or value if login is validated
        answer = message

        if(answer === "true"){
            // login validated, go to login page
            console.log("forwarding to home page")
            forwardHome()
        }
        else{
            // notify that the login was not validated

        }
    });
}