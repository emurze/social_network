function toggle_elem(elem) {elem.classList.toggle('no_display')}
function show_elem(elem) {elem.classList.remove('no_display')}
function remove_elem(elem) {elem.classList.add('no_display')}

function toggle_elems(...elems) {elems.map(toggle_elem)}
function show_elems (...elems) {elems.map(show_elem)}
function remove_elems (...elems) {elems.map(remove_elem)}

function show_overlay_elem(overlay) {
    document.body.classList.add('no_scroll')
    show_elem(overlay)
}
function remove_overlay_elem(overlay) {
    document.body.classList.remove('no_scroll')
    remove_elem(overlay)
}