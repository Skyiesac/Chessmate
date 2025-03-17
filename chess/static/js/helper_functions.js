
function post_request(url, csrf) {
    fetch(url, {
        method: "POST",
        headers: { "X-CSRFTOKEN": csrf },
        mode: "same-origin",
        credentials: "same-origin",
        redirect: 'follow',
    })
    .then(response => {
        console.log(response);
        window.location.href = response["url"];
    })
    .catch((error) => {
        console.error('Error', error);
    });
}

/*
function get_request_fetch(url, ID, callback) {
    fetch(url + ID, {
        method: "GET",
        headers: {
            "Accept": "application/json",
        },
    })
    .then(response => callback)
    .catch((error) => {
        console.error('Error', error);
    });
}

function post_request_fetch(url, send_data, csrf) {
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=UTF-8",
            "X-CSRF-TOKEN": csrf,
        },
        body: send_data,
        redirect: 'follow',
    })
    .then(response => {
        console.log(response);
        console.log(response);
        window.location.href = response["url"];
    })
    .catch((error) => {
        console.error('Error', error);
    });
}
*/

export { post_request } ;
