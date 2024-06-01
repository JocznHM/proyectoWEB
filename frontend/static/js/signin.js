$(document).ready(function () {
/*------------------------------------ Codigo para recordar usuario y contraseña ---------------------------------------*/
    var emailInput = $("#email");
    var passwordInput = $("#passwd");
    var recordarCheckbox = $("#recordarCheckbox");

    // Restaurar usuario y contraseña almacenados, si están disponibles
    var storedEmail = localStorage.getItem("storedEmail");
    var storedPassword = localStorage.getItem("storedPassword");
    if (storedEmail && storedPassword) {
        emailInput.val(storedEmail);
        passwordInput.val(storedPassword);
        recordarCheckbox.prop("checked", true);
    }

    // Agregar un event listener para detectar cambios en el estado del checkbox de "Recordar"
    recordarCheckbox.change(function() {
        if (recordarCheckbox.prop("checked")) {
            // Si se marca la casilla de "Recordar", almacenar el usuario y la contraseña en localStorage
            localStorage.setItem("storedEmail", emailInput.val());
            localStorage.setItem("storedPassword", passwordInput.val());
        } else {
            // Si se desmarca la casilla de "Recordar", eliminar el usuario y la contraseña almacenados de localStorage
            localStorage.removeItem("storedEmail");
            localStorage.removeItem("storedPassword");
        }
    });

    // Agregar un event listener para el envío del formulario
    $("#loginForm").submit(function(event) {
         event.preventDefault(); // Evitar que se envíe el formulario de inmediato
    });

/*------------------------------- Evento que detecta el click en el botón de login ----------------------------*/
    $("#loginButton").click(function () {
        var data = {
            email:  $("#email").val(),
            password: $("#passwd").val(),
        };
        console.log(data);
        $.ajax({
            url: "http://" + window.location.hostname + ":8000/usuarios/sign_in",
            type: "POST",
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json",
            success: function (res, textStatus, jqXHR) {
                if(jqXHR.status==200){
                    toastr.success('Bienvenido', 'Autenticación exitosa');
                    // Se almacena el token de autenticación en el local storage
                    localStorage.setItem('token', res.token);
                    // Se llama al servidor front para guardar el usuario y el valor de session
                    var dataSession = {
                        email: data.email, 
                        logged_in: true, 
                        token: res.token
                    }
                    $.ajax({
                        url: "http://" + window.location.hostname + ":5000/signin",
                        type: "POST",
                        data: JSON.stringify(dataSession),
                        dataType: "json",
                        contentType: "application/json",
                        success: function (res, textStatus, jqXHR) {
                            if (jqXHR.status == 200) {
                                window.location.href = "http://" + window.location.hostname + ":5000/";
                            }
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            console.log('error: ', jqXHR);
                            toastr.error(jqXHR.responseJSON.error, 'Error al iniciar sesión');
                        }
                    });

                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                toastr.error(jqXHR.responseJSON.error, 'Error al iniciar sesión');
            }
        });
    });


});