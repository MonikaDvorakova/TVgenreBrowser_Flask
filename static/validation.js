if (document.querySelectorAll('input[type="checkbox"]:checked').length === document.querySelectorAll('input[type="checkbox"]').length) {
    console.log('All checkboxes are checked');
} else {
    console.log('Some checkboxes are not checked');
};

let fieldsetCheckboxes = document.querySelector('#checkboxes');
let submitBtn = document.querySelector('.button');
let checkboxes = document.querySelector('#checkboxes');
let form = document.querySelector('#form');
let warning = document.querySelector('#warning');



checkboxes.addEventListener('change', function (event) {
    //let checkedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    let checkedCheckboxes = [];
    let checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            checkedCheckboxes.push(checkbox);
        }
    });
    if (!checkedCheckboxes.length) {
        checkboxes.forEach(checkbox => {
            checkbox.classList.add('invalid');
        })
        warning.classList.remove('hidden');
    } else {
        checkboxes.forEach(checkbox => {
            checkbox.classList.remove('invalid');
        })
        warning.classList.add('hidden');
    }
});

form.addEventListener('submit', function (event) {
    if (!document.querySelectorAll('input[type="checkbox"]:checked').length) {
        alert("Vyberte alespoň jednu televizní stanici!");
        event.preventDefault();
        warning.classList.remove('hidden');
    }
})

