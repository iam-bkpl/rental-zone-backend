function validateForm(){

            var fname = document.forms['form']['firstname'].value;
            var lname = document.forms['form']['lastname'].value;
            var uname = document.forms['form']['uname'].value;
            var email = document.forms['form']['email'].value;
            var phone = document.forms['form']['phone'].value;
            var pass1 = document.forms['form']['password'].value;
            var pass2 = document.forms['form']['cpassword'].value;
            var address = document.forms['form']['address'].value;
            const btn = document.getElementById('btn');
           
           

            if (fname == "") {
               
               document.getElementById("result").innerHTML="First Name must be filled out";
               
             return false;
             
         } else if(!isNaN(fname)){
            document.getElementById("result").innerHTML="First Name must be character";
            return false;
         }
         if (lname == "") {

            document.getElementById("result").innerHTML="Last Name must be filled out";
            return false;
         } else if(!isNaN(lname)){
            document.getElementById("result").innerHTML="Last Name must be character";
            return false;
         }
         if (uname == "") {

            document.getElementById("result").innerHTML="User Name must be filled out";
            return false;
         } else if(!isNaN(uname)){
            document.getElementById("result").innerHTML="User Name must be character";
            return false;
         }
         if(email == ""){
            document.getElementById("result").innerHTML="Email must be filled out";
            return false;
         }
               
         if(pass1 == ""){
            document.getElementById("result").innerHTML="Password must be filled";
            return false;
         }
         if(pass2 == ""){
            document.getElementById("result").innerHTML="Confirm your password";
            return false;
         } 
         
         else if(pass1 != pass2){
            document.getElementById("result").innerHTML="Password must be same";
            return false;
         }
         if(phone==""){
            document.getElementById("result").innerHTML="Enter Phone Number";
            return false;
         } else if (phone.length!=10) {
            document.getElementById("result").innerHTML="Phone Number should be of 10 digits";
            return false;
         } 

         if(address==""){
            document.getElementById("result").innerHTML="Address should be filled ";
            return false;

         }

       }

       
      //   const btn = document.getElementById('btn');

      //   btn.addEventListener('click', () => {
      //     setTimeout(() => {
      //       const result = document.getElementById('result');
        
      //       // 👇️ removes element from DOM
      //       result.style.display = 'hidden';
        
      //       // 👇️ hides element (still takes up space on page)
      //       // box.style.visibility = 'hidden';
      //     }, 3000);
      //   });


// function validateForm() {
//     var f_name=document.getElementById('firstname').Value;
//     var l_name=document.getElementById('lastname').Value;
//     var email=document.getElementById('email').Value;
//     var uname=document.getElementById('username').Value;
//     var pwd=document.getElementById('password').Value;
//     var cpwd=document.getElementById('confirm-password').Value;
//     var mobile=document.getElementById('phone').Value;
//     var address=document.getElementById('address').Value;
//     var id_file=document.getElementById('file').Value;

//     var f_nameErr = l_nameErr = unameErr = emailErr = pwdErr = cpwdErr = mobileErr = addressErr = id_fileErr = true;

//     if(f_name == "") {
//         printError("f_nameErr", "Please enter your name");
//         var elem = document.getElementById("firstname");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//     } 
    
//     else {
//         var regex = /^[a-zA-Z\s]+$/;                
//         if(regex.test(f_name) === false) {
//             printError("f_nameErr", "Please enter a valid name");
//             var elem = document.getElementById("firstname");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//         } else {
//             printError("f_nameErr", "");
//             nameErr = false;
//             var elem = document.getElementById("firstname");
//             elem.classList.add("input-1");
//             elem.classList.remove("input-2");

            
//         }
//     }
//     if(l_name == "") {
//         printError("l_nameErr", "Please enter your name");
//         var elem = document.getElementById("lastname");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//     } 
    
//     else {
//         var regex = /^[a-zA-Z\s]+$/;                
//         if(regex.test(l_name) === false) {
//             printError("l_nameErr", "Please enter a valid name");
//             var elem = document.getElementById("lastname");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//         } else {
//             printError("l_nameErr", "");
//             nameErr = false;
//             var elem = document.getElementById("lastname");
//             elem.classList.add("input-1");
//             elem.classList.remove("input-2");

            
//         }
//     }
    
//     if(uname == "") {
//         printError("unameErr", "Please enter your name");
//         var elem = document.getElementById("name");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//     } 
    
//     else {
//         var regex = /^[a-zA-Z\s]+$/;                
//         if(regex.test(uname) === false) {
//             printError("unameErr", "Please enter a valid name");
//             var elem = document.getElementById("name");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//         } else {
//             printError("unameErr", "");
//             nameErr = false;
//             var elem = document.getElementById("name");
//             elem.classList.add("input-1");
//             elem.classList.remove("input-2");

            
//         }
//     }

//     if(email == "") {
//         printError("emailErr", "Please enter your email address");
//          var elem = document.getElementById("email");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//     } else {
        
//         var regex = /^\S+@\S+\.\S+$/;
//         if(regex.test(email) === false) {
//             printError("emailErr", "Please enter a valid email address");
//             var elem = document.getElementById("email");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//         } else{
//             printError("emailErr", "");
//             emailErr = false;
//              var elem = document.getElementById("email");
//             elem.classList.add("input-1");
//             elem.classList.remove("input-2");

//         }
//     }
    
//     if(mobile == "") {
//         printError("mobileErr", "Please enter your mobile number");
//         var elem = document.getElementById("mobile");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//     } else {
//         if(mobile.length<10){
//             printError("mobileErr", "Please enter a valid 10 digit mobile number");
//             var elem = document.getElementById("mobile");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//         }else if(!mobile.startsWith("9")){
//             printError("mobileErr","Enter a mobile number starting from 9");
//             var elem = document.getElementById("mobile");
//             elem.classList.add("input-2");
//             elem.classList.remove("input-1");
//         }else{
//             printError("mobileErr", "");
//             mobileErr = false;
//             var elem = document.getElementById("mobile");
//                 elem.classList.add("input-2");
//                 elem.classList.remove("input-1");
//         }
//     }
    
// }