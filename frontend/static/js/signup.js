$(document).ready(function () {
    console.log("signup.js ready");
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