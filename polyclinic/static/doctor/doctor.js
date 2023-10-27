




refresh_patients_list = async function(){

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
            "<button class='btn moreDetails' data-whatever=" + result[index].pk + "> More Details</button> </div></td>"




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
            "<button class='btn moreDetails'  data-whatever=" + result[index].pk + "> More Details</button> </div></td>"


            }


            table.appendChild(patient)

        }


        $('.moreDetails').on('click', function(event) {
            event.preventDefault();

           var button = $(event.relatedTarget) // Button that triggered the modal
           var recipient = $(this).attr('data-whatever')

            window.open("/reception/patients/details/" + recipient , '_blank');
        });


    } else {

          console.log("error")

    }

}


$(document).ready(refresh_patients_list)







$('#addAppointments').on('submit', async function(event) {

    event.preventDefault();

    const myForm = document.getElementById('addAppointments');

    const formData = new FormData(myForm);
    const response = await fetch("/api/appointments/add", {method: 'post', body: formData });

    if (response.ok) {

        const result = await response.json();

    } else {

          console.log("error")

    }

});








