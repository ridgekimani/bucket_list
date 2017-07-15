function signUp() {
    var username = $("#username").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var confirm_password = $("#confirm_password").val();

    if (!username){
        swal("Error!", "Please enter your username", 'error');
        return 0;
    }
    if (!password){
        swal("Error!", "Please enter your password", 'error');
        return 0;
    }
    if (!confirm_password){
        swal("Error!", "Please confirm your password", 'error');
        return 0;
    }
    if (confirm_password !== password){
        swal("Error!", "Passwords don't match", 'error');
        return 0;
    }

    $.ajax({
        url:'/register/',
        data: {username: username, password: password, confirm_password: confirm_password},
        type: 'POST',
        dataType: 'text',
        success: function(response){
            var json = JSON.parse(response);
            swal('Success!', json.success, 'success');
            window.location.href = '/create_bucket/';
        },
        error: function (xhr){
            var json = JSON.parse(xhr.responseText);
            swal('Error', json.error, 'error');
            return 0;
        }
    })
}

function login(){
    var username = $("#username").val();
    var password = $("#password").val();

    if(!username){
        swal("Error!", "Please enter your username", "error");
        return 0;
    }
    if(!password){
        swal("Error!","Please enter your password", 'error');
        return 0;
    }

    var data = {
        password:password,
        username:username
    };

    $.ajax({
        url: '/login/',
        data: data,
        type: 'POST',
        success: function(){
            window.location.href = '/create_bucket/';
        },
        error: function(xhr){
            var json = JSON.parse(xhr.responseText);
            swal('Error!', json.error, 'error');
            return 0;
        }
    })
}

function createBucket(value){
    var bucket_name = $("#bucket_name").val();
    var description = $("#description").val();
    var category = $("#category").val();

    if (!bucket_name){
        swal("Error!", "Please enter the bucket name", 'error');
        return 0;
    }

    if (!description){
        swal("Error!", "Please enter the description", 'error');
        return 0;
    }

    $.ajax({
        url: '/create_bucket/',
        data: {bucket_name:bucket_name, description:description, category:category},
        type: 'POST',
        success: function(){
            swal('Success!','Bucket created successfully', 'success');
            if (value === 1){
                window.location.href = '/view_buckets/';
            }
            else if (value === 2){
                window.location.href = '/create_bucket/';
            }
            else{
                window.location.href = '/view_buckets/'
            }
        },
        error: function (xhr){
            var json = JSON.parse(xhr.responseText);
            swal('Error!', json.error, 'error');
            return 0;
        }
    })
}

function addActivity(key){
    swal("Info", 'In progress', 'info');
    return 0;
}

function viewActivities(key){
    swal("Info", 'In progress', 'info');
    return 0;
}

function updateBucket(key){
    swal("Info", 'In progress', 'info');
    return 0;
}

function deleteBucket(key){
    swal("Info", 'In progress', 'info');
    return 0;
}
