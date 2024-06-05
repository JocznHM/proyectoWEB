$(document).ready(function () {
    console.log("Mis cursos cargado");

    token = localStorage.getItem('token');
    currentUser = localStorage.getItem('currentUser');
    cargarMisCursos();
    function cargarMisCursos() {
        $.ajax({
            url: 'http://'+window.location.hostname+':8000/cursos/mis_cursos/'+currentUser,
            type: 'GET',
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function(response) {
                console.log(response);
                let cursos = response.cursos;
                var template1 = '';
                var template = '';
                var aux = 0;
                cursos.forEach(curso => {
                    if (aux == 0){
                        template1 += `
                            <div class="course-card large" courseid="${curso._id}">
                                <img src="${curso.imagen}" alt="Python Essentials">
                                <div class="course-info">
                                    <button class="options-button">⋮</button>
                                    <h3>${curso.titulo}</h3>
                                    <p>Lenguaje: ${curso.lenguaje}</p>
                                    <div class="progress-bar">
                                        <div class="progress" style="width: 100%;"></div>
                                    </div>
                                    <p class="time-left">Duración: ${curso.duracion}</p>
                                    <a class="btn btn-primary" id="verCurso">Ver curso</a>
                                </div>
                            </div>
                        `;
                        $('#continue-learning').html(template1);
                        aux = 1;
                    }
                    else{
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
                                    <a class="btn btn-primary" id="verCurso">Ver curso</a>
                                </div>
                            </div>
                        `;
                    }
                });
                $('#myCourses-list').html(template);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    // Ver curso
    $("#verCurso").on('click', function() {
        console.log("Ver curso");
        window.location.href = "/curso";
    });

    $(document).on('click', '#verCurso', function() {
        console.log("Ver curso");
        window.location.href = "/curso";
    });
});