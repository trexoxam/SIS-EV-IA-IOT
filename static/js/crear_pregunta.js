

document.getElementById("btnIA").addEventListener("click", async () => {

    const nombreExamen = document.getElementById("nombre_examen").value;
    const tema = document.getElementById("tema").value;

    if(nombreExamen === "" || tema === ""){

        alert("Escribe el nombre del examen y el tema.");

        return;

    }

    try{

        const respuesta = await fetch("/generar_pregunta_ia",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                nombre_examen:nombreExamen,
                tema:tema

            })

        });

        const datos = await respuesta.json();

        if(datos.error){

            alert(datos.error);

            return;

        }

        document.getElementById("pregunta").value = datos.pregunta;
        document.getElementById("opcion_a").value = datos.opcion_a;
        document.getElementById("opcion_b").value = datos.opcion_b;
        document.getElementById("opcion_c").value = datos.opcion_c;
        document.getElementById("opcion_d").value = datos.opcion_d;
        document.getElementById("respuesta_correcta").value = datos.respuesta_correcta;

    }

    catch(error){

        console.log(error);

        alert("Error al generar la pregunta.");

    }

});

