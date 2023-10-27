




$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('Patient details ' + recipient)
  modal.find('.modal-body input').val(recipient)
})

$('#exampleModal').on('click', 'a', function(event) {
    event.preventDefault();
    window.open($(this).attr('href'), '_blank');
});


setInterval(async function(){

     const response = await fetch("/api/messages", {method: 'get' });

    if (response.ok) {

        const _result = await response.json();
        const result = JSON.parse(_result);

        const table = document.getElementById('messages_list');
        table.innerHTML=""

        document.getElementById('messageCount').innerText =  result.length

        for (let index = 0; index < result.length; index+=1){

            let msg = document.createElement("tr")


            msg.innerHTML =  "<td><div class='widget-26-job-title'>" + result[index].fields.message + "</div></td><td>" +
               " <div class='widget-26-job-info'><p class='type m-0'>Reason</p>" +
                    "<p class='text-muted m-0'>in <span class='location'>" + result[index].fields.reason + "</span>" +
                    "</p> </div> </td> <td> <div class='widget-26-job-salary'>"+ result[index].fields.addAt + "</div>" +
        "</td> <td> <div class='widget-26-job-category bg-soft-danger'>" +
                "<i class='indicator bg-info'></i>" +
                "<span> Critical </span>" +
            "</div> </td> <td> <div class='widget-26-job-starred'>"

            table.appendChild(msg)


        }



    } else {

          console.log("error")

    }


}, 60000)





$('#refresh_patients_list').on('click',  function(event) {
    event.preventDefault();
    refresh_patients_list();

 });


refresh_patients_list = async function(){

   const response = await fetch("/api/patients", {method: 'get' });

    if (response.ok) {


        const _result = await response.json();
        const result = JSON.parse(_result);
        console.log(result)
        const table = document.getElementById('patients_list');
        table.innerHTML = ""

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

$(document).ready(async function(){

     const response = await fetch("/api/messages", {method: 'get' });

    if (response.ok) {

        const _result = await response.json();
        const result = JSON.parse(_result);

        const table = document.getElementById('messages_list');
        table.innerHTML=""

        document.getElementById('messageCount').innerText =  result.length

        for (let index = 0; index < result.length; index+=1){

            let msg = document.createElement("tr")


            msg.innerHTML =  "<td><div class='widget-26-job-title'>" + result[index].fields.message + "</div></td><td>" +
               " <div class='widget-26-job-info'><p class='type m-0'>Reason</p>" +
                    "<p class='text-muted m-0'>in <span class='location'>" + result[index].fields.reason + "</span>" +
                    "</p> </div> </td> <td> <div class='widget-26-job-salary'>"+ result[index].fields.addAt + "</div>" +
        "</td> <td> <div class='widget-26-job-category bg-soft-danger'>" +
                "<i class='indicator bg-info'></i>" +
                "<span> UNREAD </span>" +
            "</div> </td> <td> <div class='widget-26-job-starred'> </div> </td>"

            table.appendChild(msg)
        }

    } else {

          console.log("error")
    }

})




$('#addOnePatient').on('submit', async function(event) {

    event.preventDefault();

    const myForm = document.getElementById('addOnePatient');

    const formData = new FormData(myForm);
    const response = await fetch("/reception/patients/add", {method: 'post', body: formData });

    if (response.ok) {

        const result = await response.json();
        var elt = document.getElementsByClassName("closeAddPatient")
        elt[0].click();
        elt[1].click();

        window.open("/reception/patients/details/" + result.patient_id , '_blank');
        refresh_patients_list()

    } else {

          console.log("error")
    }

});

$('.removeHospitalisation').on('click', async function(event) {

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






