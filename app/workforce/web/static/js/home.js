var BASE_URL = ''
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
            this.append(draggedItem);
            this.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
        });
    }
}

function onclick_load_team(elem) {
    console.log($(elem).get(0));
    const id = $(elem).get(0).id;
    const url = BASE_URL + `/api/v1/team/${id}?only=description,id,members.name,members.designation,name,tasks.actual_end_date,tasks.assignee.name,tasks.attachments,tasks.created_at,tasks.description,tasks.expected_end_date,tasks.id,tasks.modified_at,tasks.modified_by,tasks.priority,tasks.reporter.id,tasks.reporter.name,tasks.start_date,tasks.task_status,tasks.title`;
    $.get(url,(data, status) =>{
        $('#team-title').text(data["name"]);
        $('#team-description').text(data["description"]);
        var status=data["tasks"];
        console.log(status);
    });

};

$(document).ready(function(){
    $.get(BASE_URL + '/api/v1/teams?only=id,name', (data, status)=>{
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