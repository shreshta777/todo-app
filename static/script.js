function addTask(){
fetch("/add",{
method:"POST",
headers:{"Content-Type":"application/x-www-form-urlencoded"},
body:`task=${task.value}&deadline=${date.value}`
}).then(()=>location.reload());
}

function deleteTask(id){
fetch(`/delete/${id}`).then(()=>location.reload());
}

function toggleTask(id){
fetch(`/complete/${id}`).then(()=>location.reload());
}
