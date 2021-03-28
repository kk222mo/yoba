function update_data() {
    var labels = document.getElementsByClassName("label-for-checkbox");
    var labels_search = [];
    for (var i = 0; i < labels.length; i++) {
        var checkbox = document.getElementById(labels[i].htmlFor);
        if (checkbox.checked) {
            var classname = labels[i].innerHTML;
            labels_search.push(classname);
        }
    }
    console.log(labels_search);
    if (labels_search.length > 0) {
        var tag_spans = document.getElementsByClassName("tags");
        for (var i = 0; i < tag_spans.length; i++) {
            var del = true;
            var tag_list = tag_spans[i].innerHTML.split(',');
            for (var j = 0; j < labels_search.length; j++) {
                for (var k = 0; k < tag_list.length; k++) {
                    if (tag_list[k] == labels_search[j]) {
                        del = false;
                        break;
                    }
                }
            }
            if (del) {
                tag_spans[i].parentElement.style.display = "none";
            } else {
                tag_spans[i].parentElement.style.display = "block";
            }
        }
    } else {
        var tag_spans = document.getElementsByClassName("tags");
        for (var i = 0; i < tag_spans.length; i++) {
            tag_spans[i].parentElement.style.display = "block";
        }
    }
}

window.onload = function() {
    update_data();
}

function join_unjoin(token) {
    $.post('/courses/join/', {course_token: token})
    .done(function(data){
        document.location.reload();
    });
}