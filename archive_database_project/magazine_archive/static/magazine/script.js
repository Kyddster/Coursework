var years = document.getElementById("years-var").value;
var months = document.getElementById("months-var").value;
var days = document.getElementById("days-var").value;
var volumes = document.getElementById("volumes-var").value;
var numbers = document.getElementById("numbers-var").value;


yearElements = document.getElementsByClassName('year');
monthElements = document.getElementsByClassName('month');
dayElements = document.getElementsByClassName('day');
volumeElements = document.getElementsByClassName('volume');
numberElements = document.getElementsByClassName('number');

let yearInput = document.getElementById('years');
let monthInput = document.getElementById('months');
let dayInput = document.getElementById('days');

let volumeInput = document.getElementById('volumes');
let numberInput = document.getElementById('numbers');

let selectBox = document.getElementsByClassName('download-check')
let selectAll = document.getElementById('select-all')
let downloadError = document.getElementById('error-msg-download')



function checkResults() {

    var results = []

    let yearContent = document.getElementsByClassName('year-column')
    let monthContent = document.getElementsByClassName('month-column')
    let dayContent = document.getElementsByClassName('day-column')
    let volumeContent = document.getElementsByClassName('volume-column')
    let numberContent = document.getElementsByClassName('number-column')

    let searchOptions = document.getElementsByClassName('search-option')

    for (j = 0; j < searchOptions.length; j++) {
        searchOptions[j].style.display = 'none'
    }

    let currentSearch = []
    for (i = 0; i < yearContent.length; i++) {

        var yearBool = false
        var monthBool = false
        var dayBool = false
        var volumeBool = false
        var numberBool = false

        let year = yearContent[i].textContent
        let month = monthContent[i].textContent
        let day = dayContent[i].textContent

        let volume = volumeContent[i].textContent
        let number = numberContent[i].textContent

        if (yearInput.value != 'all') {
            if (year != yearInput.value) {
                yearBool = false
            } else {
                yearBool = true
            }
        } else {
            yearBool = true
        }

        if (monthInput.value != 'all') {
            if (month != monthInput.value) {
                monthBool = false
            } else {
                monthBool = true
            }
        } else {
            monthBool = true
        }

        if (dayInput.value != 'all') {
            if (day != dayInput.value) {
                dayBool = false
            } else {
                dayBool = true
            }
        } else {
            dayBool = true
        }

        if (volumeInput.value != 'all') {
            if (volume != volumeInput.value) {
                volumeBool = false
            } else {
                volumeBool = true
            }
        } else {
            volumeBool = true
        }

        if (numberInput.value != 'all') {
            if (number != numberInput.value) {
                numberBool = false
            } else {
                numberBool = true
            }
        } else {
            numberBool = true
        }

        if (yearBool && monthBool && dayBool && volumeBool && numberBool) {
            yearContent[i].parentElement.style.display = 'table-row'


            result = [year, month, day, volume, number]

            document.getElementById('year-'+result[0]).style.display = 'block'
            document.getElementById('month-'+result[1]).style.display = 'block'
            document.getElementById('day-'+result[2]).style.display = 'block'
            document.getElementById('volume-'+result[3]).style.display = 'block'
            document.getElementById('number-'+result[4]).style.display = 'block'
            
            let temp = [volume, number]
            currentSearch.push([temp])

        } else {
            yearContent[i].parentElement.style.display = 'none'
        }
    }
    window.currentSearch = currentSearch
}

checkResults()

yearInput.addEventListener('input', checkResults);
monthInput.addEventListener('input', checkResults);
dayInput.addEventListener('input', checkResults);
volumeInput.addEventListener('input', checkResults);
numberInput.addEventListener('input', checkResults);

selectors = document.getElementsByClassName('select-search')

function reset_selectors() {
    for (i = 0; i < selectors.length; i++) {
        selectors[i].value = 'all'
    }
    checkResults()
    localStorage.clear()
}

reset = document.getElementById('reset-search')
reset.addEventListener('click', function (e) {
    reset_selectors()
    window.location.href = '/magazine'
})



let current = window.location.href.split('/').slice(-1)[0]

if (current != '') {
    let currentRow = document.getElementById('row-' + current)
    currentRow.style.backgroundColor = '#ffff00'

    currentArr = current.split('-')
    currentVol = currentArr[0]
    currentNum = currentArr[1]

    currentDisplay = document.getElementById('current-display')
    currentDisplay.innerHTML = 'Current edition of \'The Gresham\' selected: Vol ' + currentVol + ', number ' + currentNum
}



selectAll.addEventListener('click', function(e) {
    if (selectAll.checked == true) {
        for (const box of selectBox) {
            if (box.parentElement.parentElement.style.display != 'none') {
                box.checked = true
            }
        }
    } else {
        for (const box of selectBox) {
            box.checked = false
        }
    }
})


let download = document.getElementById('download-files')
download.addEventListener('click', function(e) {
    
    let selected = []
    for (const box of selectBox) {
        if (box.parentElement.parentElement.style.display != 'none') {
            if (box.checked && box.parentElement.parentElement.style.display != 'none') {
                selected.push(box)
            }
        } else {
            box.checked = false
        }

    }
    if (selected.length == 1) {
        dirID = selected[0].parentElement.parentElement.id.slice(4)
        downloadError.style.display = 'none'
        window.location.href = '/magazine/download/'+dirID
    } else if (selected.length > 1) {
        let downloadArr = []
        for (const box of selected) {
            downloadArr.push(box.name)
        }
        let downloadForm = document.getElementById("download-arr-form")
        downloadForm.innerHTML += '<input type="hidden" name="downloadArr" value='+downloadArr+'>'
        downloadForm.submit()
        downloadError.style.display = 'none'
    } else if (current != '') {
        dirID = current
        downloadError.style.display = 'none'
        window.location.href = '/magazine/download/'+dirID
    } else {
        downloadError.style.display = 'block'
    }
})

let keywordsearch = document.getElementById('run-key-word-search')
let keywordsbox = document.getElementById('keywords')
let keywordForm = document.getElementById('keyword-form')

let savedKeywords = localStorage.getItem('keywords')
if (savedKeywords) {
  keywordsbox.value = savedKeywords
}

keywordsearch.addEventListener('click', function(e) {

    if (keywordsbox.value == '') {
        return
    }


    reset_selectors()
    const keywords = keywordsbox.value.trim()
    localStorage.setItem('keywords', keywords)

    keywordArr = keywordsbox.value.split(' ')
    console.log(keywordArr)

    keywordArr = [...new Set(keywordArr.filter(f => f !== ''))]

    const formData = new FormData(keywordForm);
    formData.set('keywordArr', keywordArr);
    formData.set('pdfArr', window.currentSearch);
    formData.set('current', current);

    fetch('/magazine/keywords', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        localStorage.setItem('results', JSON.stringify(data))

        keywordPages(data.result)

    })
    .catch(error => console.error(error));
    
    
    e.preventDefault();
});

window.pages = document.getElementById('pages')

temp = localStorage.getItem('results')
if (temp) {
    keywordResults = JSON.parse(temp).result
    keywordPages(keywordResults)
}



function keywordPages(keywordResults) {
    console.log(keywordResults)
    tableRowArr = document.getElementsByClassName('table-row')
    for (item of tableRowArr) {
        if (getComputedStyle(item).backgroundColor == 'rgb(0, 255, 255)') {
            item.style.backgroundColor = '#ffffff'
        }
    }
    window.pages.innerHTML = ''
    let executed = false
    for (item of keywordResults) {
        let volume = item[0]
        let number = item[1]
        let page = item[2]

        let tableRow = document.getElementById('row-'+volume+'-'+number)
        tableRow.style.backgroundColor = '#00ffff'
        if (current != '') {
            temp = current.split('-')
            tempVolume = parseInt(temp[0])
            tempNumber = parseInt(temp[1])

            if (volume == tempVolume && number == tempNumber) {
                if (!executed) {
                    window.pages.innerHTML += '<div>Pages the keywords are in:</div>'
                    executed = true
                }
                window.pages.innerHTML += '<div>'+page+'</div>'
            }
        }
    }
}

adminButton = document.getElementById('admin-link')
adminButton.addEventListener('click', function(e) {
    window.location.href = 'login'
})

