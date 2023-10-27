



/*
$(document).ready( async function(){

   const response = await fetch("/api/patients", {method: 'get' });

    if (response.ok) {

        const _result = await response.json();
        const result = JSON.parse(_result);
        console.log(result)
        const table = document.getElementById('patients_list');

        for (let index = 0; index < result.length; index+=1){

           const condition = result[index].fields.condition
           isCritical = condition == "Critical"
           console.log(isCritical)

            let patient = document.createElement("tr")
            if(isCritical){

            patient.innerHTML =  "<td><div class='widget-26-job-title'>" +
                "<a href='#' class='text-uppercase'>" + result[index].fields.firstName + " " + result[index].fields.lastName + "</a> </div></td><td>" +
               " <div class='widget-26-job-info'><p class='type m-0'>Full-Time</p>" +
                    "<p class='text-muted m-0'>in <span class='location'>" + result[index].fields.address + "</span>" +
                    "</p> </div> </td> <td> <div class='widget-26-job-salary'>"+ result[index].fields.gender + "</div>" +
        "</td> <td> <div class='widget-26-job-category bg-soft-danger'>" +
                "<i class='indicator bg-danger'></i>" +
                "<span> Critical </span>" +
            "</div> </td> <td> <div class='widget-26-job-starred'>" +
            "<button data-target='#exampleModal' data-toggle='modal' data-whatever=" + result[index].pk + "> Add param</button> </div></td>"




            }
            else{


                        patient.innerHTML =  "<td><div class='widget-26-job-title'>" +
                "<a href='#' class='text-uppercase'>" + result[index].fields.firstName + " " + result[index].fields.lastName + "</a> </div></td><td>" +
               " <div class='widget-26-job-info'><p class='type m-0'>Full-Time</p>" +
                    "<p class='text-muted m-0'>in <span class='location'>" + result[index].fields.address + "</span>" +
                    "</p> </div> </td> <td> <div class='widget-26-job-salary'>"+ result[index].fields.gender + "</div>" +
        "</td> <td> <div class='widget-26-job-category bg-soft-base'>" +
                "<i class='indicator bg-primary'></i>" +
                "<span> No Critical </span>" +
            "</div> </td> <td> <div class='widget-26-job-starred'>" +
            "<button data-target='#exampleModal' data-toggle='modal' data-whatever=" + result[index].pk + "> Add param</button> </div></td>"


            }


            table.appendChild(patient)


        }



    } else {

          console.log("error")

    }



}


)
*/



/*
$('#makeConsultation').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('makeConsultation');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    const response = await fetch("/api/patients/make-consultation", {method: 'post', body: formData });

    if (response.ok) {

        document.location.reload();



    } else {

          console.log("error")
    }

});

*/



$('#add_access').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('add_access');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    "hjhjdvsd ".replace("^.['].$","\"")

    const response = await fetch("/api/patients/add-access", {method: 'post', body: formData });

    if (response.ok) {

        document.location.reload();



    } else {

          console.log("error")
    }

});

$('.removeAccess').on('click', async function(event) {

    event.preventDefault();

    var idAccess = $(this).attr('data-whatever')

     if(confirm('Are you sure you want to Remove access to this member?') == true ){

        const response = await fetch("/api/patients/remove-access/" + idAccess);

        if (response.ok) {

            document.location.reload();

        } else {

              console.log("error")
        }



     }

});

$('#makeConsultation').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('makeConsultation');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    const response = await fetch("/api/patients/add-consultation", {method: 'post', body: formData });

    if (response.ok) {

        document.location.reload();

    } else {

          console.log("error")
    }

});

$('.toggleCondition').on('click', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    if (confirm("Change condition ?") == true) {

        const response = await fetch("/api/patients/toggle-condition/" + idPatient);

        if (response.ok) {

            document.location.reload();
        }
        else {

              console.log("error")
        }
    }

});

$('#addAppointment').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('addAppointment');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    const response = await fetch("/api/patients/add-appointment", {method: 'post', body: formData });

    if (response.ok) {

        document.location.reload();

    } else {

          console.log("error")
    }

});

$('#addParam').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('addParam');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    const response = await fetch("/api/patients/add-param", {method: 'post', body: formData });

    if (response.ok) {


        document.location.reload();

    } else {

          console.log("error")
    }

});

$('#addPrescription').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('addPrescription');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    const response = await fetch("/api/patients/add-prescription", {method: 'post', body: formData });

    if (response.ok) {


        document.location.reload();


    } else {

          console.log("error")
    }

});

$('#addExamRequest').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('addExamRequest');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    const response = await fetch("/api/patients/add-exam-request", {method: 'post', body: formData });

    if (response.ok) {


        document.location.reload();

    } else {

          console.log("error")
    }

});

$('#addHospitalisationRequest').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('addHospitalisationRequest');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)
    formData.append('reason', "Hospitalisation")

    const response = await fetch("/api/patients/add-message", {method: 'post', body: formData });

    if (response.ok) {


        document.location.reload();

    } else {

          console.log("error")
    }

});

$('#removeHospitalisation').on('click', async function(event) {

    event.preventDefault();

    let id = $(this).attr('data-whatever')

    if (confirm("Leave Hospitalisation ?") == true) {

        const response = await fetch("/api/patients/remove-hospitalisation/" + id);

        if (response.ok) {

            document.location.reload();
        }
        else {

              console.log("error")
        }
    }

});

$('#makeHospitalisation').on('submit', async function(event) {

    event.preventDefault();

    var idPatient = $(this).attr('data-whatever')

    const myForm = document.getElementById('makeHospitalisation');

    const formData = new FormData(myForm);
    formData.append('idPatient', idPatient)

    const response = await fetch("/api/patients/add-hospitalisation", {method: 'post', body: formData });

    if (response.ok) {


        document.location.reload();

    } else {

          console.log("error")
    }

});


