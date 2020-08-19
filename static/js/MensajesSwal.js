function MensajeInfo(mensaje) {
    Swal.fire({
        title: 'Información!',
        icon: 'info',
        text: mensaje,
        type: 'success',
        timer: 1500
    });
}

function MensajeError(mensaje) {
    Swal.fire({
        title: 'Información!',
        icon: 'error',
        text: mensaje,
        type: 'error',
        timer: 5000
    });
}

function MensajeAlerta(mensaje) {
    Swal.fire({
        title: 'Información!',
        icon: 'warning',
        text: mensaje,
        type: 'warning',
        timer: 5000
    });
}