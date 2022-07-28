function validate(){
    var username = document.forms['form']['username'].value;
    var password = document.forms['form']['password'].value;
    if (username == "") {

        document.getElementById("result").innerHTML="User Name must be filled out";
        return false;
    }
    else if (password == "") {
        

        document.getElementById("result").innerHTML="Password must be filled out";
        return false;
    }

}    