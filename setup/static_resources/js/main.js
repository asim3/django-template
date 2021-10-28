String.prototype.clean_digits = function () {
    const arabic_numbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
    return this.replace(/[٠-٩]/g, function (number) {
        return arabic_numbers.indexOf(number)
    });
}


// function is_there_QR_code_canvas() {
//     QR_code_canvas = document.getElementById("QR_code_canvas")
//     if (QR_code_canvas === null) {
//         return false
//     }
//     else {
//         return true
//     }
// }



// function add_QR_code() {
//     QR_code_canvas = document.getElementById("QR_code_canvas")
//     url = window.location.href
//     QR_code_canvas.innerHTML = ""
//     new QRCode(QR_code_canvas, url);
// }



function _main(event) {
    const today = new Date()
    $("#all_rights_reserved").append(today.getFullYear())

    // if (is_there_QR_code_canvas()) {
    //     add_QR_code()
    // }

    // document
    //     .getElementById("id_select")
    //     .addEventListener("change", select_changed)

    // select_changed()
}


window.addEventListener("load", _main)
