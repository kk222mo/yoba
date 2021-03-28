function getCourses() {
    $.ajax({
        url: "/courses/get/",
        success: function (data) {
            console.log(data);
        }
    })
}

function joinCourse(token) {
    $.post('/courses/join/', {course_token: token})
    .done(function(data){
        console.log(data)
    });
}