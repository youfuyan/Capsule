const fileInput = document.getElementById('file-upload');
const preview = document.getElementById('image-preview');

fileInput.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.addEventListener('load', function() {
    preview.style.backgroundImage = `url(${reader.result})`;
  });

  reader.readAsDataURL(file);
});
