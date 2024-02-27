function updateFileName(input) {
    var fileName = document.getElementById("fileName");
    if (input.files.length > 0) {
        fileName.innerText = input.files[0].name;
    } else {
        fileName.innerText = "Choose an Image";
    }
}