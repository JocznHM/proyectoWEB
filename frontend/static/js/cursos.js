$(document).ready(function() {
    console.log("Cursos cargado");
    token = localStorage.getItem('token');
    console.log(token);
    cargarCursos();

    // Función para cargar los cursos
    function cargarCursos() {
        $.ajax({
            url: 'http://'+window.location.hostname+':8000/cursos/all_cursos',
            type: 'GET',
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function(response) {
                console.log(response);
                let cursos = response.cursos;
                let template = '';
                cursos.forEach(curso => {
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
                                <a class="btn btn-primary" id="inscribirCurso">Inscribirme</a>
                                <a class="btn btn-primary" id="agregarCarrito"><img src="/static/img/compras.png"></a>
                            </div>
                        </div>

                    `;
                });
                $('#cursos').html(template);
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
                window.location.href = '/allCourses';
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('error: ', jqXHR);
                console.log('error: ', jqXHR.responseJSON["msg"]);
                toastr.error(jqXHR.responseJSON["msg"], 'Error al agregar al carrito');
            }
        });
    });
});