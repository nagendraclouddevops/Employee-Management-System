if (!localStorage.getItem("loggedIn")) {
    window.location.href = "login.html";
}

function logout() {
    localStorage.removeItem("loggedIn");
    window.location.href = "login.html";
}

function saveEmployee(){

fetch("http://localhost:5001/add",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

name:document.getElementById("name").value,
email:document.getElementById("email").value,
department:document.getElementById("department").value,
salary:document.getElementById("salary").value

})

}).then(()=>loadEmployees());

}

function loadEmployees(){

fetch("http://localhost:5001/employees")

.then(response=>response.json())

.then(data=>{

let html="<table>";

html+="<tr><th>Name</th><th>Email</th><th>Department</th><th>Salary</th></tr>";

data.forEach(emp=>{

html+=`<tr>
<td>${emp.Name}</td>
<td>${emp.Email}</td>
<td>${emp.Department}</td>
<td>${emp.Salary}</td>
</tr>`;

});

html+="</table>";

document.getElementById("employees").innerHTML=html;

});

}

loadEmployees();