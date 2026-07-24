let preguntaActual = 0;

const preguntas =
    document.querySelectorAll(".pregunta");

const totalPreguntas =
    preguntas.length;


function mostrarPregunta(){

    preguntas.forEach(function(pregunta, indice){

        pregunta.style.display =
            indice === preguntaActual
            ? "block"
            : "none";

    });


    document.getElementById("numeroActual")
        .textContent = preguntaActual + 1;


    const porcentaje =
        Math.round(
            ((preguntaActual + 1) / totalPreguntas) * 100
        );


    document.getElementById("porcentaje")
        .textContent = porcentaje + "%";


    document.getElementById("barraProgreso")
        .style.width = porcentaje + "%";

}


function siguiente(){

    const pregunta =
        preguntas[preguntaActual];


    const respuesta =
        pregunta.querySelector(
            'input[type="radio"]:checked'
        );


    if(!respuesta){

        alert(
            "Selecciona una respuesta antes de continuar."
        );

        return;

    }


    if(preguntaActual < totalPreguntas - 1){

        preguntaActual++;

        mostrarPregunta();

    }

}


function anterior(){

    if(preguntaActual > 0){

        preguntaActual--;

        mostrarPregunta();

    }

}


function finalizar(){

    const pregunta =
        preguntas[preguntaActual];


    const respuesta =
        pregunta.querySelector(
            'input[type="radio"]:checked'
        );


    if(!respuesta){

        alert(
            "Selecciona una respuesta antes de finalizar."
        );

        return;

    }


    const confirmar =
        confirm(
            "¿Estás seguro de finalizar el examen?"
        );


    if(confirmar){

        document
            .getElementById("formularioExamen")
            .submit();

    }

}


mostrarPregunta();