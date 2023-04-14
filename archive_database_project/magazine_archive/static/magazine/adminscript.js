let form = document.getElementById('upload-form');
let fileInput = document.getElementById('file-input');

form.addEventListener('submit', e => {
  let file = fileInput.files[0]
  if (!file || !file.type.includes('pdf')) {
    e.preventDefault()
    alert('Please select a PDF file.')
  }
});

let dateInput = document.getElementById('date-input')
let datePattern = /^\d{4}-\d{2}-\d{2}$/

document.querySelector('form').addEventListener('submit', function(e) {
  e.preventDefault()
  let dateValue = dateInput.value
  if (!datePattern.test(dateValue)) {
    alert('Please enter a valid date in the format YYYY-MM-DD')
    return
  }

  this.submit()
})

let reset = document.getElementById('reset-admin')

reset.addEventListener('click', function(e) {
    form.reset()
})