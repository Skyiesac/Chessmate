
function rem_all(class_name) {
    let els = document.getElementsByClassName(class_name);
    while (els.length >= 1) {
        els[0].classList.remove(class_name);
    }
}

function func_redirect(response) {
    window.location.href = response["url"];
}

function log_error(error) {
    console.error('Error', error);
}

function post_request(url, csrf, body=null, succ=func_redirect, err=log_error, redirect='follow') {
    if (succ == null) { let succ = redirect; }
    if (err  == null) { err  = basicerr; }
    console.log("HI");
    fetch(url,
    {
        method: "POST",
        headers: { "X-CSRFTOKEN": csrf },
        mode: "same-origin",
        credentials: "same-origin",
        redirect: redirect,
        body: JSON.stringify(body),
    }).then(succ).catch(err);
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

export { post_request, rem_all } ;
