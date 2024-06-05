$(document).ready(function () {
    console.log("Carrito cargado");

    token = localStorage.getItem('token');
    currentUser = localStorage.getItem('currentUser');
    cargarCarrito();
    function cargarCarrito() {
        var template = '';
        $.ajax({
            url: 'http://'+window.location.hostname+':5000/get_carrito',
            type: 'GET',
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function(response) {
                courses = response.cart;
                if (courses.length == 0){
                    template += `
                        <div class="empty-cart">
                            <h2>Carrito vacío</h2>
                            <p>¡Agrega cursos a tu carrito para comenzar a aprender!</p>
                        </div>
                    `;
                    $('#carrito-list').html(template);
                    return;
                }
                else{
                    courses.forEach(course => {
                        $.ajax({
                            url: 'http://'+window.location.hostname+':8000/cursos/get_curso/'+course,
                            type: 'GET',
                            headers: {
                                "Authorization": "Bearer " + token
                            },
                            success: function(response) {
                                let curso = response.curso;
                                console.log(curso);
                                template += `
                                    <div class="course-card" courseid="${curso._id}">
                                        <img src="${curso.imagen}" alt="HTML and CSS">
                                        <div class="course-info">
                                            <div class="dropdown-container">
                                                <button class="options-button">⋮</button>
                                            </div>
                                            <h3>${curso.titulo}</h3>
                                            <p class="course-language">Lenguaje: ${curso.lenguaje}</p>
                                            <p class="course-duration">Duración: ${curso.duracion}</p>
                                        </div>
                                    </div>
                                `;
                            },
                            error: function(error) {
                                console.log(error);
                            }
                        });
                    });
                }
                //se espera a que se carguen todos los cursos
                setTimeout(function(){
                    $('#carrito-list').html(template);
                }, 500);
            }
        });
    }

    $(document).on('click', '#pay', function() {
        $.ajax({
            url: 'http://'+window.location.hostname+':5000/limpiar_carrito',
            type: 'GET',
            success: function(response) {
                console.log(response);
                toastr.success('Compra realizada con éxito');
                setTimeout(function(){
                    window.location.href = "/carrito";
                }
                , 2000);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

});