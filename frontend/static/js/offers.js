$(document).ready(function () {
    console.log("Ofertas cargado");
    var token = localStorage.getItem('token');
    var currentUser = localStorage.getItem('currentUser');

    cargarOfertas();
    function cargarOfertas() {
        var template = '';
        $.ajax({
            url: 'http://'+window.location.hostname+':8000/cursos/cursos_oferta',
            type: 'GET',
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function(response) {
                courses = response.cursos;
                courses.forEach(course => {
                    template += `
                        <div class="course-card" courseid="${course._id}">
                            <img src="${course.imagen}" alt="HTML and CSS">
                            <div class="course-info">
                                <div class="dropdown-container">
                                    <button class="options-button">⋮</button>
                                </div>
                                <h3>${course.titulo}</h3>
                                <p class="course-language">Lenguaje: ${course.lenguaje}</p>
                                <p class="course-duration">Duración: ${course.duracion}</p>
                                <a class="btn btn-primary" id="inscribirCurso">Inscribirme</a>
                                <a class="btn btn-primary" id="agregarCarrito"><img src="/static/img/compras.png"></a>
                            </div>
                        </div>
                    `;
                });
                $('#offers-list').html(template);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    $(document).on('click', '#inscribirCurso', function() {
        console.log('Inscribirme');
        // Obtener el id del curso al que se quiere inscribir del course-card padre
        var curso = $(this).parent().parent().attr('courseid');
        var email = localStorage.getItem('currentUser');
        var data = {
            course_id: curso,
            email: email
        };

        $.ajax({
            url: 'http://'+window.location.hostname+':8000/cursos/inscribir',
            type: 'POST',
            headers: {
                "Authorization": "Bearer " + token
            },
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json',
            success: function(response) {
                console.log(response);
                toastr.success('Inscripción exitosa', '¡Felicidades!');
                window.location.href = '/myCourses';
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('error: ', jqXHR);
                console.log('error: ', jqXHR.responseJSON["msg"]);
                toastr.error(jqXHR.responseJSON["msg"], 'Error al inscribirse');
            }
        });
    });


    $(document).on('click', '#agregarCarrito', function() {
        console.log('Agregar al carrito');
        // Obtener el id del curso al que se quiere inscribir del course-card padre
        var curso = $(this).parent().parent().attr('courseid');
        var email = localStorage.getItem('currentUser');
        var data = {
            course_id: curso,
            email: email
        };
        $.ajax({
            url: 'http://'+window.location.hostname+':5000/agregar_carrito',
            type: 'POST',
            headers: {
                "Authorization": "Bearer " + token
            },
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json',
            success: function(response) {
                console.log(response);
                toastr.success('Curso agregado al carrito', '¡Felicidades!');
                window.location.href = '/offers';
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('error: ', jqXHR);
                console.log('error: ', jqXHR.responseJSON["msg"]);
                toastr.error(jqXHR.responseJSON["msg"], 'Error al agregar al carrito');
            }
        });
    });
});