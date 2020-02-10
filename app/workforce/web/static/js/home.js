var BASE_URL = ''
team_data = null;
var Item = ({ id, name }) => {
    $.get(BASE_URL+`/api/v1/team/${id}/banner`,(data, status)=>{
        const link = data["link"];
        const color = data["color"];
        console.log(link);
        $('.each-item').append(`
<div id="${id}" onclick="onclick_load_team(this);">
  <a href="#">
    <img class="team-img" src="${link}" alt=""/>
    <h5>${name}</h5>
  </a>
</div>`);
    })
}

var set_drag_on_all = () => {    const listItems = document.querySelectorAll('.list-item');
    const lists = document.querySelectorAll('.list');

    let draggedItem = null;

    for (let i=0; i < listItems.length; i++) {
        const item = listItems[i];

        item.addEventListener('dragstart', function () {
            draggedItem = item;
            setTimeout(function () {
                item.style.display = 'none';
            }, 0)
        });

        item.addEventListener('dragend', function () {
            setTimeout(function () {
                draggedItem.style.display = 'block';
                draggedItem = null;
            }, 0);
        })
    };

    for (let j = 0; j < lists.length; j ++) {
        const list = lists[j];

        list.addEventListener('dragover', function (e) {
            e.preventDefault();
        });
        
        list.addEventListener('dragenter', function (e) {
            e.preventDefault();
            this.style.backgroundColor = 'rgba(0, 0, 0, 0.2)';
        });

        list.addEventListener('dragleave', function (e) {
            this.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
        });

        list.addEventListener('drop', function (e) {
            console.log('drop');
            if (draggedItem !== null){
                this.append(draggedItem);
            }
            this.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
        });
    }
}

function onclick_load_team(elem) {
    console.log($(elem).get(0));
    const id = $(elem).get(0).id;
    const url = BASE_URL + `/api/v1/team/${id}?only=description,id,members.name,members.designation,name,tasks.actual_end_date,tasks.assignee.name,tasks.attachments,tasks.created_at,tasks.description,tasks.expected_end_date,tasks.id,tasks.modified_at,tasks.modified_by,tasks.priority,tasks.reporter.id,tasks.reporter.name,tasks.start_date,tasks.task_status,tasks.title`;
    $.get(url,(data, status) =>{
        team_data = data;
        $('#team-title').text(data["name"]);
        $('#team-description').text(data["description"]);
        $('#TODO').empty();
        $('#DOING').empty();
        $('#DONE').empty();
        $.each(data["tasks"], (index, task) => {
            $(`#${task["task_status"]}`).append(`
            <div class="list-item" draggable="true" onclick="on(this);" data-id="${index}">${task["id"]}</div>
            `);
            console.log("Adding task...")

        });
        set_drag_on_all();
    });
}
     
function off() 
{
    document.getElementById("overlay").style.display = "none";
}

function on(task)
{
    if(task==="new")
    {
        console.log(task);
      $('#details').hide();
      $("#includedContent").show();
      $("#includedContent").load("/addtask"); 

    }
    else
    {
        $('#includedContent').hide();
        $('#details').show();
    index = $(task).attr("data-id");
    console.log("IN ON");
    task_obj = team_data["tasks"][index];
    console.log(task_obj);
    $('#id1').html(task_obj["title"]);
    $('#id2').html(task_obj["description"]);
    $('#id3').text(task_obj["task_status"]);
    $('#id4').text(task_obj["reporter"]["name"]);
    $('#id5').text(task_obj["assignee"]["name"]);
    $('#id6').text(task_obj["start_date"]);
    $('#id7').text(task_obj["expected_end_date"]);
    $('#id8').text(task_obj["priority"]);
    $('#id9').text(task_obj["actual_end_date"]);
    }
    $("#overlay").toggle();

};

$(document).ready(function(){
    $.get(BASE_URL + '/api/v1/teams?only=id,name', (data, status)=>{
        data.map(Item);
    });
    $.get(BASE_URL + '/api/v1/reporterTasks/', (data, status)=>{
        data.map(Item);
    });

    set_drag_on_all();
});

function search()
{
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x=document.getElementsByClassName('animals');

    for(let i=0;i<x.length;i++)
    {
        if(!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else{
            x[i].style.display="list-item";
        }
    }

}