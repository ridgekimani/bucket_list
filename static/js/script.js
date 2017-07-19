function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}


function signUp() {
    var email = $("#email").val();
    var password = $("#password").val();
    var confirm_password = $("#confirm_password").val();

    if (!email){
        swal('Error!', 'Please enter your email address', 'error');
        return 0;
    }

    if (!validateEmail(email)){
        swal("Error!", "Please enter a valid email address", 'error');
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
        data: {email:email, password: password, confirm_password: confirm_password},
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
    var email = $("#email").val();
    var password = $("#password").val();

    if(!email){
        swal("Error!", "Please enter your email", "error");
        return 0;
    }
    if (!validateEmail(email)){
        swal("Error!", "Please enter a valid email address", 'error');
        return 0;
    }
    if(!password){
        swal("Error!","Please enter your password", 'error');
        return 0;
    }

    var data = {
        password:password,
        email:email
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

function updateBucketUrl(key){
 window.location.href = '/update_bucket/?key=' + key;
}

function updateBucket(key){
    var bucket_name = $("#bucket_name").val();
    var description = $("#description").val();
    var category = $("#category").val();

    if (!bucket_name){
        swal("Error!", 'Please enter your bucket name', 'error');
        return 0;
    }
    if (!description){
        swal('Error!', 'Please enter a short description', 'error');
        return 0
    }

    $.ajax({
        url: '/update_bucket/',
        data: {bucket_name:bucket_name, description:description, category:category, key:key},
        type: 'POST',
        dataType: 'text',
        success: function (response) {
            var json = JSON.parse(response);
            swal("Success", json.success, 'success');
            window.location.href = '/view_buckets/'
        },
        error: function (xhr) {
            var json = JSON.parse(xhr.responseText);
            swal("Error!", json.error, 'error');
            return 0;
        }
    })
}

function deleteBucket(key){
    if (! key){
        swal("Please select a specific bucket to delete");
        return 0;
    }

    $.ajax({
        url: '/delete/',
        data: {key:key, bucket:true},
        type: 'POST',
        dataType: 'text',
        success: function (response) {
            var json = JSON.parse(response);
            swal('Success!', json.success, 'success');
            window.location.href = '/view_buckets/'
        },
        error: function (xhr) {
            var json = JSON.parse(xhr.responseText);
            swal("Error!", json.error, 'error');
            return 0;
        }
    });
}

function addActivity(key){
    swal({
        title: 'Add Activity',
        input: 'textarea',
        showCancelButton: true,
        inputValidator: function (value){
            return new Promise(function (resolve, reject){
                if (value){
                    resolve()
                }
                else{
                    reject('Please add your activities!')
                }
            })
        }
    }).then(function (text) {
        if (!text){
            swal('Error!', 'Please enter your activities');
            return 0;
        }
        $.ajax({
            data: {text:text, key:key},
            url: '/add_activity/',
            type: 'POST',
            dataType: 'text',
            success: function(response){
                var json = JSON.parse(response);
                swal('Success!', json.success, 'success');
                return 0;
            }
        })

    })
}

function viewActivitiesUrl(key){
    window.location.href = '/view_activities/?key=' + key;
}

function updateActivityUrl(activity_key){
    var key = $("#key").val();
    window.location.href = '/update_activity/?key=' + key + activity_key;

}

function deleteActivity(activity_key){
    var key = $("#key").val();

    if (! activity_key){
        swal("Please select a specific activity to delete");
        return 0;
    }

    $.ajax({
        url: '/delete/',
        data: {key:key, activity:true, activity_key:activity_key},
        type: 'POST',
        dataType: 'text',
        success: function (response) {
            var json = JSON.parse(response);
            swal('Success!', json.success, 'success');
            window.location.reload();
        },
        error: function (xhr) {
            var json = JSON.parse(xhr.responseText);
            swal("Error!", json.error, 'error');
            return 0;
        }
    });

}

function updateActivity(){
    var activity_key = $("#activity_key").val();
    var key = $("#key").val();
    var description = $("#div_description").text();

    if (!description){
        swal('Error!', 'Please enter the activities', 'error');
        return 0;
    }
        $.ajax({
        url: '/update_activity/',
        data: {description:description, activity_key:activity_key, key:key},
        type: 'POST',
        dataType: 'text',
        success: function (response) {
            var json = JSON.parse(response);
            swal("Success", json.success, 'success');
            window.location.href = '/view_activities/?key=' + key;
        },
        error: function (xhr) {
            var json = JSON.parse(xhr.responseText);
            swal("Error!", json.error, 'error');
            return 0;
        }
    })



}