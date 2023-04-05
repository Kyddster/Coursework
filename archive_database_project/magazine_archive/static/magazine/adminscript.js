let form = document.getElementById('upload-form');
let fileInput = document.getElementById('file-input');

form.addEventListener('submit', e => {
  let file = fileInput.files[0];
  if (!file || !file.type.includes('pdf')) {
    e.preventDefault();
    alert('Please select a PDF file.');
  }
});

let reset = document.getElementById('reset-admin')

reset.addEventListener('click', function(e) {
    form.reset()
})