function haveExperience(obj){
    years = document.getElementById('employee_have_experience_years')
    if (obj.value == '1'){
        document.getElementById('have_experience_box').style.display = 'block';
        years.required = true
        
    } else {
        document.getElementById('have_experience_box').style.display = 'none';
        years.required = false
        years.value = ''
    }
}

function haveExperienceOnSave(){
    passing = false
    years = document.getElementById('employee_have_experience_years')
    if (years.value < 46 && years.value > 0) {
        passing = true
    } else {
        alert("يرجى اختيار رقم من 1 الى 45")
        years.value = ''
    }
    // if (passing === true) {
    //     $('#exampleModal').modal('hide');
    // }
}



function MainFormBox(obj){
    years = document.getElementById('main-form-box')
    if (obj.value == '1'){
        years.style.display = 'block';

    } else {
        years.style.display = 'none';

    }
}


function employee_ageOnSave(){
    passing = false
    years = document.getElementById('employee_age')
    if ( years.value > 16) {
        document.getElementById('employee-age-feedback').style.display = 'none'
    } else {
        years.value = ''
        document.getElementById('employee-age-feedback').style.display = 'block'
        
    }
    // if (passing === true) {
    //     $('#exampleModal').modal('hide');
    // }
}




function onChangeDisplayHowHear(obj){
    if (obj.value == '0' ) {
        document.getElementById('employee_how_hear_other1').style.display = 'block'
    } else {
        document.getElementById('employee_how_hear_other1').style.display = 'none'
    }

}

function onChangeDisplayCetType(obj){
    if (obj.value != '1' ) {
        document.getElementById('employee_learning_domain1').style.display = 'block'
    } else {
        document.getElementById('employee_learning_domain1').style.display = 'none'
    }

}

function onChangeDisplayAmputation(obj){
    employee_disability_type = document.getElementById('employee_disability_type')
    if (obj.value == '5' &&  employee_disability_type.value == '1') {
        document.getElementById('employee_disability_amputation_type1').style.display = 'block'
        document.getElementById('employee_disability_idntify_amputation1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_amputation_type1').style.display = 'none'
        document.getElementById('employee_disability_idntify_amputation1').style.display = 'none'
    }

}

function onChangeDisplayDisabilityOthers(obj){
    employee_disability_type = document.getElementById('employee_disability_type')
    if (obj.value == '0' &&  employee_disability_type.value == '0') {
        document.getElementById('employee_disability_others_identy1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_others_identy1').style.display = 'none'
    }

}


function onChangeDisplayDisabilityType(obj){
    if (obj.value == '1' ) {
        document.getElementById('employee_disability_movement1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_movement1').style.display = 'none'
    }

    if (obj.value == '2' ) {
        document.getElementById('employee_disability_mind1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_mind1').style.display = 'none'
    }

    if (obj.value == '3' ) {
        document.getElementById('employee_disability_Disturbances1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_Disturbances1').style.display = 'none'
    }
    
    if (obj.value == '4' ) {
        document.getElementById('employee_disability_hear1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_hear1').style.display = 'none'
    }

    if (obj.value == '5' ) {
        document.getElementById('employee_disability_eays1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_eays1').style.display = 'none'
    }

    if (obj.value == '7' ) {
        document.getElementById('employee_disability_body1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_body1').style.display = 'none'
    }

    if (obj.value == '8' ) {
        document.getElementById('employee_disability_alone1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_alone1').style.display = 'none'
    }

    if (obj.value == '9' ) {
        document.getElementById('employee_disability_learn1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_learn1').style.display = 'none'
    }

    if (obj.value == '10' ) {
        document.getElementById('employee_disability_atrabat1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_atrabat1').style.display = 'none'
    }

    if (obj.value == '11' ) {
        document.getElementById('employee_disability_speak1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_speak1').style.display = 'none'
    }

    if (obj.value == '0' ) {
        document.getElementById('employee_disability_others_identy1').style.display = 'block'
    } else {
        document.getElementById('employee_disability_others_identy1').style.display = 'none'
    }



    
}