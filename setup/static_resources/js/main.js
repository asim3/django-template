String.prototype.clean_digits = function () {
    const arabic_numbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
    return this.replace(/[٠-٩]/g, function (number) {
        return arabic_numbers.indexOf(number)
    });
}


function _main(event) {
    const today = new Date()
    $("#all_rights_reserved").append(today.getFullYear())


    document
        .getElementById("id_select")
        .addEventListener("change", select_changed)

    select_changed()
}


window.addEventListener("load", _main)
