$(document).ready(function() {
    console.log("Perfil cargado");
    var token = localStorage.getItem('token');
    var currentUser = localStorage.getItem('currentUser');
    cargarPerfil();
    function cargarPerfil() {
        var template = '';
        $.ajax({
            url: 'http://'+window.location.hostname+':8000/usuarios/get_user/email='+currentUser,
            type: 'GET',
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function(response) {
                user = response.data_user;
                console.log(user);
                template += `
                    <div class="profile-info">
                        <p><b>Nombre completo:</b></p>
                        <p>${user.nombre_completo}</p>
                        <p><b>Email:</b></p>
                        <p>${user.email}</p>
                    </div>
                `;
                $('#profile-info').html(template);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

});