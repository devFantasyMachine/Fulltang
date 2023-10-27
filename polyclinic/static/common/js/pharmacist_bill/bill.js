var bill = "";
var row_price;

function open_form(){
    document.getElementById("myForm").style.display = "block";
}

function close_form(){
    document.getElementById("myForm").style.display = "none";
}

function add(reference,price,qty) {
    var tableRef = document.getElementById("bill").getElementsByTagName('tbody')[0];
    let i = String(reference);
    let qtyRef = i+"qty";
    let btnRef = i+"btn";
    tableRef.insertRow().innerHTML = 
    '<td></td>'+
    '<td>' + reference +'</td>'+
    `<td id="${qtyRef}" class= "quantity"> 1 </td>`+
    `<td class = ${i}>` + price +'</td>'+
    `<td id =${i}>`+  '<b>'+ price + '</b>'  +'</td>'+
    '<td>' + '<button style ="background-color : red" onclick ="remove(this)">x</button>' +'</td>'+
    '<td>' + `<button name="${i}" onclick ="inc(${reference},op='dec')" style ="background-color : yellow"> - </button>` +'</td>'+
    '<td>' + `<button name="${i}" onclick ="inc(${reference},op='inc',${qty})" style ="background-color : blue"> + </button>` +'</td>'; 
    total_amount();
    document.getElementById(btnRef).disabled = true;
    

}

function inc(reference,op,qty){
    let i = String(reference);
    let qtyRef = i+"qty";
    qtyTag = document.getElementById(`${qtyRef}`);
    let number = parseInt(qtyTag.textContent);
   
    if (op=='inc'){
        if (qty==number) window.alert("the quantity is exceding the available value");
        else qtyTag.innerText = number +1;
    }
    else qtyTag.innerText = number -1;
    quantity = qtyTag.textContent;
    unitTag = document.getElementsByClassName(`${i}`)[0];
    unit =  unitTag.textContent;

    total= document.getElementById(`${i}`);
    total.innerHTML = '<b>'+ unit*quantity +'</b>' ;
    total_amount()
}

function remove(r){
    var i = r.parentNode.parentNode.rowIndex;
    document.getElementById("bill").deleteRow(i);
    total_amount()
}

function total_amount(){
    /*Sum all the totals in each row of the Total's Column  */
row_price = document.getElementsByTagName('b');
var total_bill = 0; var items = 0;

for (let i = 0; i < row_price.length; i++) {
    total_bill += parseInt(row_price[i].textContent);
    
}
/*Sum all the quantities in each row of the Quantity's Column  */
document.getElementById('amount').value= total_bill;
itemsTag = document.getElementsByClassName("quantity");
for (let i = 0; i < itemsTag.length; i++) {
    items += parseInt(itemsTag[i].textContent);
    
}
document.getElementById('items').value = items;
}

function save(){
    item = "";
    bill_items = document.querySelectorAll("#bill tbody tr");
    /* cleaning stage 1 */
    /* cleaning stage 2 is performed at the server side */
    for (let index = 0; index < bill_items.length-1; index++) {
        item = item + bill_items[index].outerText + ">";
        item = item.replaceAll("x","");
        item = item.replaceAll("+","");
        item = item.replaceAll("-","");
    }
    item = item + bill_items[bill_items.length-1].outerText
    item = item.replaceAll("x","");
    item = item.replaceAll("+","");
    item = item.replaceAll("-","");
    item = item.replaceAll("\t"," ");
    document.getElementById("send").value = item;
    table = item.split('>');
    window.confirm("all your actions have been saved successfully")
    

}
function print(){
    pageContent = document.body.innerHTML;
    actionTag = document.getElementById("print");
    actionTag.remove();
    window.print();
    docTag = document.getElementById("document").innerHTML;
    document.body.innerHTML = docTag;
    
    document.body.innerHTML = pageContent;
}
tag = document.querySelectorAll(".line:nth-child(2)")
line = document.querySelectorAll(".line")
var val = 0;
for (let index = 0; index < tag.length; index++) {
    val = parseInt(tag[index].textContent);
    if(val<5){
        line.style.backgroundColor = "red"
    }
    
}

