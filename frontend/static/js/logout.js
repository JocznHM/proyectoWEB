$(document).ready(function() {
    $('#logout').click(function() {
        $.ajax({
            url: '/logout',
            type: 'POST',
            success: function(response) {
                if (response == 'success') {
                    window.location.href = '/';
                } else {
                    alert('Error al cerrar sesión');
                }
            }
        });
    });
});