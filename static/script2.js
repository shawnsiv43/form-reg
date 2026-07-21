const Form=document.getElementById('register');
const usernameCheck=document.getElementById('username');
const emailCheck=document.getElementById('email');
const passwordCheck=document.getElementById('password');
const conPassword=document.getElementById('confirm-password');
const resultDiv=document.getElementById('endResult')
const ageCheck=document.getElementById('age')
const searchBtn=document.getElementById('search_btn')
usernameCheck.removeAttribute('readonly')
if (localStorage.getItem('readonlyFlag')==="true"){
    usernameCheck.setAttribute('readonly','')
} else{
    usernameCheck.removeAttribute('readonly')
}
Form.addEventListener('submit',validator);
function showError(input,msg){
    const formElement=input.parentElement;
    formElement.className="form-element error";
    const small=formElement.querySelector("small");
    small.innerText=msg
}
function showsuccess(input){
    const formElement=input.parentElement
    formElement.className="form-element success"
}


function validator(e){
    e.preventDefault();
    resultDiv.textContent=""
    let con=false
    let em=false
    let pass=false
    let user=false
    let ageFlag=false
    let isUpdate=localStorage.getItem("updateTrue")
    user=usernameValid((usernameCheck),3,25)
    em=emailCheckings(emailCheck)
    pass=passwordValid(passwordCheck,6,25)
    con=cValid((conPassword))
    ageFlag=validAge(ageCheck,10,80)

    if (user && em && pass && con && ageFlag && localStorage.getItem("readonlyFlag")!=="true"){
    username=usernameCheck.value;
    eName=emailCheck.value
    passName=passwordCheck.value
    cpassName=conPassword.value
    ageName=ageCheck.value
        fetch("/api/reg?uName="+encodeURIComponent(username)+"&eName="+encodeURIComponent(eName)+"&passName="+encodeURIComponent(passName)+"&ageName="+encodeURIComponent(ageName))
            .then(function(response){
                return response.json()
            })
            .then(function(data){
                resultDiv.textContent=data.regMsg;
                if (data.regMsg===`Your Registration has been ${username}, ${eName}, ${passName}, ${ageName}` & !data.error){
                    let isSuccess="Successfully registered. Saved to the database"
                    // fetch("/success?isSuccess="+encodeURIComponent(isSuccess))
                    //     .then(function(response){
                    //         return response
                    //     })
                    window.location.href="/allusers"
                }
                else{
                    let isSuccess=`Regestration has failed on Primary Key constraint on the username:  ${username} `
                    // fetch("/success?isSuccess="+encodeURIComponent(isSuccess))
                    //     .then(function(response){
                    //         return response
                    //     })
                    //showError(usernameCheck,"Primary key constraint")
                    window.location.href="/success?isSuccess="+encodeURIComponent(isSuccess)

                }
            })
    }
    else if(user && em && pass && con && ageFlag && localStorage.getItem("readonlyFlag")==="true"){
        // 1. Package the data you want to send in the POST request body
    const payload = {
        email: emailCheck.value,
        age: ageCheck.value,
        password: passwordCheck.value,
        // Add any other variables you need to send to the backend here
    };

    // 2. Make the POST request to your Flask route
    fetch(`/update/${username.value}`, {
        method: 'POST', // Explicitly setting the method to POST
        headers: {
            'Content-Type': 'application/json' // Telling Flask to expect JSON data
        },
        body: JSON.stringify(payload) // Converting the JS object to a JSON string
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); 
    })
    .then(data=>{
        if (data.happy==="success"){
            window.location.href="/allusers"
        }
    })
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error during POST request:', error);
    });
    }
    // else if(user && em && pass && con && ageFlag && isUpdate==="true"){
    //     uName=usernameCheck.value;
    //     eName=emailCheck.value
    //     passName=passwordCheck.value
    //     cpassName=conPassword.value
    //     ageName=ageCheck.value
    //     exUsername=localStorage.getItem("usernameHappy")
    //     fetch("/update?uName="+encodeURIComponent(uName)+"&eName="+encodeURIComponent(eName)+"&ageName="+encodeURIComponent(ageName)+"&passName="+encodeURIComponent(passName)+"&cpassName="+encodeURIComponent(cpassName)+"&ex_username="+encodeURIComponent(exUsername))
    //         .then(function(response){
    //             return response.json()
    //         })
    //         .then(function(data){
    //             resultDiv.textContent=data.msg
    //         })
    //     isUpdate=false
    //     localStorage.setItem("updateTrue","false")
    // }
}
function emailCheckings(emailVal){
    emailVal=emailVal.value
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if(emailVal===""){
        showError(emailCheck,'Email can\' be balnk')
        return false
    }
    else if (emailRegex.test(emailVal)){
        showsuccess(emailCheck)
        return true
    }
    
}
function validAge(input,min,max){
    if(parseInt(input.value)<min){
        showError(input,'Age must 10 or greater')
        return false
    }else if (parseInt(input.value)>max){
        showError(input,'Bro you know that you\'re a Grandpa/Grandma. Enjoy your life')
        return false
    }else{
        showsuccess(input)
        return true
    }
}
function usernameValid(input,min,max){
    if(input.value===""){
        showError(input,'Username can\' be blank')
        return false
    }
    else if(input.value.length<min){
        showError(input,'Username must be at least 3')
        return false
    }
    else if(input.value.length>max){
        showError(input,'Username is at most 25')
        return false
}
else{
    showsuccess(input)
    return true
}
}
function passwordValid(input,min,max){
    if(input.value===""){
        showError(input,'Password can\' be blank')
        return false
    }
    else if(input.value.length<min){
        showError(input,'Password must be at least 6 characters')
        return false
    }
    else if(input.value.length>max){
        showError(input,'Password can\'t is at most 25 characters ')
        return false
    }
    else{
        showsuccess(input)
        return true
    }
}
function cValid(input){
    if(input.value===""){
        showError(input,'Confirm password can\' be blank')
        return false  
    }
    else if(input.value!==passwordCheck.value.trim()){
        showError(input,'Confirm password must be the same as password')
        return false
    }
    else{
        showsuccess(input)
        return true
    }
}