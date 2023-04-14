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
currentPDF = current.split('-')

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

let languagesDict = [
  { code: 'ab', name: 'Abkhazian' },
  { code: 'aa', name: 'Afar' },
  { code: 'af', name: 'Afrikaans' },
  { code: 'ak', name: 'Akan' },
  { code: 'sq', name: 'Albanian' },
  { code: 'am', name: 'Amharic' },
  { code: 'ar', name: 'Arabic' },
  { code: 'an', name: 'Aragonese' },
  { code: 'hy', name: 'Armenian' },
  { code: 'as', name: 'Assamese' },
  { code: 'av', name: 'Avaric' },
  { code: 'ae', name: 'Avestan' },
  { code: 'ay', name: 'Aymara' },
  { code: 'az', name: 'Azerbaijani' },
  { code: 'bm', name: 'Bambara' },
  { code: 'ba', name: 'Bashkir' },
  { code: 'eu', name: 'Basque' },
  { code: 'be', name: 'Belarusian' },
  { code: 'bn', name: 'Bengali (Bangla)' },
  { code: 'bh', name: 'Bihari' },
  { code: 'bi', name: 'Bislama' },
  { code: 'bs', name: 'Bosnian' },
  { code: 'br', name: 'Breton' },
  { code: 'bg', name: 'Bulgarian' },
  { code: 'my', name: 'Burmese' },
  { code: 'ca', name: 'Catalan' },
  { code: 'ch', name: 'Chamorro' },
  { code: 'ce', name: 'Chechen' },
  { code: 'ny', name: 'Chichewa, Chewa, Nyanja' },
  { code: 'zh', name: 'Chinese' },
  { code: 'zh-Hans', name: 'Chinese (Simplified)' },
  { code: 'zh-Hant', name: 'Chinese (Traditional)' },
  { code: 'cv', name: 'Chuvash' },
  { code: 'kw', name: 'Cornish' },
  { code: 'co', name: 'Corsican' },
  { code: 'cr', name: 'Cree' },
  { code: 'hr', name: 'Croatian' },
  { code: 'cs', name: 'Czech' },
  { code: 'da', name: 'Danish' },
  { code: 'dv', name: 'Divehi, Dhivehi, Maldivian' },
  { code: 'nl', name: 'Dutch' },
  { code: 'dz', name: 'Dzongkha' },
  { code: 'en', name: 'English' },
  { code: 'eo', name: 'Esperanto' },
  { code: 'et', name: 'Estonian' },
  { code: 'ee', name: 'Ewe' },
  { code: 'fo', name: 'Faroese' },
  { code: 'fj', name: 'Fijian' },
  { code: 'fi', name: 'Finnish' },
  { code: 'fr', name: 'French' },
  { code: 'ff', name: 'Fula, Fulah, Pulaar, Pular' },
  { code: 'gl', name: 'Galician' },
  { code: 'gd', name: 'Gaelic (Scottish)' },
  { code: 'gv', name: 'Gaelic (Manx)' },
  { code: 'ka', name: 'Georgian' },
  { code: 'de', name: 'German' },
  { code: 'el', name: 'Greek' },
  { code: 'kl', name: 'Greenlandic' },
  { code: 'gn', name: 'Guarani' },
  { code: 'gu', name: 'Gujarati' },
  { code: 'ht', name: 'Haitian Creole' },
  { code: 'ha', name: 'Hausa' },
  { code: 'he', name: 'Hebrew' },
  { code: 'hz', name: 'Herero' },
  { code: 'hi', name: 'Hindi' },
  { code: 'ho', name: 'Hiri Motu' },
  { code: 'hu', name: 'Hungarian' },
  { code: 'is', name: 'Icelandic' },
  { code: 'io', name: 'Ido' },
  { code: 'ig', name: 'Igbo' },
  { code: 'id, in', name: 'Indonesian' },
  { code: 'ia', name: 'Interlingua' },
  { code: 'ie', name: 'Interlingue' },
  { code: 'iu', name: 'Inuktitut' },
  { code: 'ik', name: 'Inupiak' },
  { code: 'ga', name: 'Irish' },
  { code: 'it', name: 'Italian' },
  { code: 'ja', name: 'Japanese' },
  { code: 'jv', name: 'Javanese' },
  { code: 'kl', name: 'Kalaallisut, Greenlandic' },
  { code: 'kn', name: 'Kannada' },
  { code: 'kr', name: 'Kanuri' },
  { code: 'ks', name: 'Kashmiri' },
  { code: 'kk', name: 'Kazakh' },
  { code: 'km', name: 'Khmer' },
  { code: 'ki', name: 'Kikuyu' },
  { code: 'rw', name: 'Kinyarwanda (Rwanda)' },
  { code: 'rn', name: 'Kirundi' },
  { code: 'ky', name: 'Kyrgyz' },
  { code: 'kv', name: 'Komi' },
  { code: 'kg', name: 'Kongo' },
  { code: 'ko', name: 'Korean' },
  { code: 'ku', name: 'Kurdish' },
  { code: 'kj', name: 'Kwanyama' },
  { code: 'lo', name: 'Lao' },
  { code: 'la', name: 'Latin' },
  { code: 'lv', name: 'Latvian (Lettish)' },
  { code: 'li', name: 'Limburgish ( Limburger)' },
  { code: 'ln', name: 'Lingala' },
  { code: 'lt', name: 'Lithuanian' },
  { code: 'lu', name: 'Luga-Katanga' },
  { code: 'lg', name: 'Luganda, Ganda' },
  { code: 'lb', name: 'Luxembourgish' },
  { code: 'gv', name: 'Manx' },
  { code: 'mk', name: 'Macedonian' },
  { code: 'mg', name: 'Malagasy' },
  { code: 'ms', name: 'Malay' },
  { code: 'ml', name: 'Malayalam' },
  { code: 'mt', name: 'Maltese' },
  { code: 'mi', name: 'Maori' },
  { code: 'mr', name: 'Marathi' },
  { code: 'mh', name: 'Marshallese' },
  { code: 'mo', name: 'Moldavian' },
  { code: 'mn', name: 'Mongolian' },
  { code: 'na', name: 'Nauru' },
  { code: 'nv', name: 'Navajo' },
  { code: 'ng', name: 'Ndonga' },
  { code: 'nd', name: 'Northern Ndebele' },
  { code: 'ne', name: 'Nepali' },
  { code: 'no', name: 'Norwegian' },
  { code: 'nb', name: 'Norwegian bokmål' },
  { code: 'nn', name: 'Norwegian nynorsk' },
  { code: 'ii', name: 'Nuosu' },
  { code: 'oc', name: 'Occitan' },
  { code: 'oj', name: 'Ojibwe' },
  { code: 'cu', name: 'Old Church Slavonic, Old Bulgarian' },
  { code: 'or', name: 'Oriya' },
  { code: 'om', name: 'Oromo (Afaan Oromo)' },
  { code: 'os', name: 'Ossetian' },
  { code: 'pi', name: 'Pāli' },
  { code: 'ps', name: 'Pashto, Pushto' },
  { code: 'fa', name: 'Persian (Farsi)' },
  { code: 'pl', name: 'Polish' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'pa', name: 'Punjabi (Eastern)' },
  { code: 'qu', name: 'Quechua' },
  { code: 'rm', name: 'Romansh' },
  { code: 'ro', name: 'Romanian' },
  { code: 'ru', name: 'Russian' },
  { code: 'se', name: 'Sami' },
  { code: 'sm', name: 'Samoan' },
  { code: 'sg', name: 'Sango' },
  { code: 'sa', name: 'Sanskrit' },
  { code: 'sr', name: 'Serbian' },
  { code: 'sh', name: 'Serbo-Croatian' },
  { code: 'st', name: 'Sesotho' },
  { code: 'tn', name: 'Setswana' },
  { code: 'sn', name: 'Shona' },
  { code: 'ii', name: 'Sichuan Yi' },
  { code: 'sd', name: 'Sindhi' },
  { code: 'si', name: 'Sinhalese' },
  { code: 'ss', name: 'Siswati' },
  { code: 'sk', name: 'Slovak' },
  { code: 'sl', name: 'Slovenian' },
  { code: 'so', name: 'Somali' },
  { code: 'nr', name: 'Southern Ndebele' },
  { code: 'es', name: 'Spanish' },
  { code: 'su', name: 'Sundanese' },
  { code: 'sw', name: 'Swahili (Kiswahili)' },
  { code: 'ss', name: 'Swati' },
  { code: 'sv', name: 'Swedish' },
  { code: 'tl', name: 'Tagalog' },
  { code: 'ty', name: 'Tahitian' },
  { code: 'tg', name: 'Tajik' },
  { code: 'ta', name: 'Tamil' },
  { code: 'tt', name: 'Tatar' },
  { code: 'te', name: 'Telugu' },
  { code: 'th', name: 'Thai' },
  { code: 'bo', name: 'Tibetan' },
  { code: 'ti', name: 'Tigrinya' },
  { code: 'to', name: 'Tonga' },
  { code: 'ts', name: 'Tsonga' },
  { code: 'tr', name: 'Turkish' },
  { code: 'tk', name: 'Turkmen' },
  { code: 'tw', name: 'Twi' },
  { code: 'ug', name: 'Uyghur' },
  { code: 'uk', name: 'Ukrainian' },
  { code: 'ur', name: 'Urdu' },
  { code: 'uz', name: 'Uzbek' },
  { code: 've', name: 'Venda' },
  { code: 'vi', name: 'Vietnamese' },
  { code: 'vo', name: 'Volapük' },
  { code: 'wa', name: 'Wallon' },
  { code: 'cy', name: 'Welsh' },
  { code: 'wo', name: 'Wolof' },
  { code: 'fy', name: 'Western Frisian' },
  { code: 'xh', name: 'Xhosa' },
  { code: 'yi, ji', name: 'Yiddish' },
  { code: 'yo', name: 'Yoruba' },
  { code: 'za', name: 'Zhuang, Chuang' },
  { code: 'zu', name: 'Zulu' },
];

let languageSelect = document.getElementById('language-select')

for (language of languagesDict) {
    option = document.createElement("option")
    option.value = language.code
    option.text = language.name
    languageSelect.appendChild(option)
}

let languageButton = document.getElementById('run-language-select')
let form = document.getElementById('language-form')
languageButton.addEventListener('click', function(e) {
    let language = document.getElementById('language-select').value
    if (!(language == '')) {
        form.innerHTML += '<input type="hidden" name="language" value='+language+'>'
        form.innerHTML += '<input type="hidden" name="volume" value='+currentPDF[0]+'>'
        form.innerHTML += '<input type="hidden" name="number" value='+currentPDF[1]+'>'
        
        form.submit()
    }

});