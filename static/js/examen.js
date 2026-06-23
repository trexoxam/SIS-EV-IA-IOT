const video = document.getElementById("webcam");
const estado = document.getElementById("estadoRostro");

let stream = null;
let tiempoSinRostro = null;
// BOTÓN ENCENDER

document.getElementById("btnEncender").addEventListener("click", async () => {

    stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });

    video.srcObject = stream;

});

// BOTÓN APAGAR

document.getElementById("btnApagar").addEventListener("click", () => {

    if(stream){

        stream.getTracks().forEach(track => track.stop());

        video.srcObject = null;

        estado.className = "alert warning";
        estado.innerHTML = "🔴 Cámara apagada";

    }

});

// MEDIAPIPE

const faceDetection = new FaceDetection({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/${file}`;
    }
});


faceDetection.setOptions({
    model: "short",
    minDetectionConfidence: 0.5
});

faceDetection.onResults((results) => {

const cantidadRostros = results.detections ? results.detections.length : 0;

if(cantidadRostros > 1){

    estado.className = "alert danger";
    estado.innerHTML = `🚨 Se detectaron ${cantidadRostros} personas`;

    return;
}

    if (!results.detections || results.detections.length === 0) {

    if(!tiempoSinRostro){
        tiempoSinRostro = Date.now();
    }

    const segundosAusente =
        (Date.now() - tiempoSinRostro) / 1000;

    if(segundosAusente >= 5){

        estado.className = "alert danger";
        estado.innerHTML =
        "🚨 Usuario ausente por más de 5 segundos";

    }else{

        estado.className = "alert danger";
        estado.innerHTML =
        "🔴 Rostro no detectado";

    }

    return;
}

    const rostro = results.detections[0];

    tiempoSinRostro = null;

    const x = rostro.boundingBox.xCenter;
    const y = rostro.boundingBox.yCenter;

    // Zona segura
    if (
        x > 0.35 &&
        x < 0.65 &&
        y > 0.30 &&
        y < 0.70
    ) {

        estado.className = "alert success";
        estado.innerHTML = "🟢 Rostro correctamente visible";

    }

    // Zona de advertencia
    else {

        estado.className = "alert info";
        estado.innerHTML = "🟡 Rostro fuera de posición";

    }

});

// ANALIZAR VIDEO

setInterval(async () => {

    if(video.readyState === 4){

        await faceDetection.send({
            image: video
        });

    }

}, 500);