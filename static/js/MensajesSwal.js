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


function MensajeInformativo(mac_bracelet) {
    Swal.fire({
        title: 'Información!',
        icon: 'warning',
        text: mac_bracelet,
        type: 'warning',
        timer: 5000
    });
    Swal.fire({
        position: 'top-end',
        title: '<strong>MAC <u>mac_bracelet</u></strong>',
        icon: 'info',
        html:
            'You can use <b>bold text</b>, ' +
            'and other HTML tags',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText:'<i class="fa fa-thumbs-up"></i> Great!',
        confirmButtonAriaLabel: 'Thumbs up, great!',
        cancelButtonText: '<i class="fa fa-thumbs-down"></i>',
        cancelButtonAriaLabel: 'Thumbs down'
    });
}