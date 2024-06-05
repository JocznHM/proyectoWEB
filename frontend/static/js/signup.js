$(document).ready(function () {
    console.log("signup.js ready");
    function validarPassword(password){
        var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&])[A-Za-z\d@$!%*?#&]{8,}$/;
        return regex.test(password);
    }
    function validarEmail(email){
        var regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return regex.test(email);
    }

    $('#password').keyup(function(){
        if(validarPassword($('#password').val())){
            $('#password').css('border-color', 'green');
            $('#sign-up').prop('disabled', false);
        }else{
            $('#password').css('border-color', 'red');
            $('#sign-up').prop('disabled', true);
            $('#validateText').text('La contraseña no cumple la validación!');
        }
    });

    $('#username').keyup(function(){
        if(validarEmail($('#username').val())){
            $('#username').css('border-color', 'green');
            $('#sign-up').prop('disabled', false);
        }else{
            $('#username').css('border-color', 'red');
            $('#sign-up').prop('disabled', true);
            $('#validateText').text('El correo no cumple la validación!');
        }
    });

    $('#sign-up').click(function(){
        console.log("sign-up clicked");
        data ={
            nombre_completo: $('#fullname').val(),
            email: $('#username').val(),
            password: $('#password').val(),
            cumpleanios: $('#date').val(),
            courses:{}
        }
        $.ajax({
            url: 'http://'+window.location.hostname+':8000/usuarios/sign_up',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response){
                $('#fullname').modal('hide');
                $('#username').val('');
                $('#password').val('');
                $('#date').val('');
                toastr.success('Usuario creado correctamente', 'Exito');
                setTimeout(function() {
                window.location.href = "http://" + window.location.hostname + ":5000/login";
                }, 3000); // 3000 milisegundos = 3 segundos
            },
            error: function(error){
                $('#fullname').modal('hide');
                $('#username').val('');
                $('#password').val('');
                $('#date').val('');
                toastr.error(error.responseJSON.error, 'Error');
            }
        });
    });
});