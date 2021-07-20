function _main(event) {
    document
        .getElementById("id_select")
        .addEventListener("change", select_changed)

    select_changed()
}



window.addEventListener("load", _main)
