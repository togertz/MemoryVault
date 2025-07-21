document.addEventListener("DOMContentLoaded", async function () {
    const imageUpload = document.getElementById("imageUpload");
    const imagePreview = document.getElementById("imagePreview");
    const imageLabel = document.getElementById("image-label");

    const convert_to_base64 = file => new Promise((response) => {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);
        fileReader.onload = () => response(fileReader.result);
    });

    imageUpload.addEventListener('change', async function () {
        const file = imageUpload.files;
        const img = await convert_to_base64(file[0]);
        imageLabel.style.backgroundImage = `url(${img})`;
    });
});