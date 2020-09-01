
// js upload image
document.getElementById('avatar_form').addEventListener('submit', function(event) {
    event.preventDefault();
    let input = document.getElementById('id_avatar');
    let data = new FormData();
    data.append('UserImage', input.files[0]);

    fetch('https://127.0.0.1:8000/connectdata/uploadimage/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: data
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);
    }).catch((error) => {
        console.error('Error:', error);
    });
});