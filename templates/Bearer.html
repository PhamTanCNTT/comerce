<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Bearer Token Authentication</title>
    <style>
        html {
            font-size: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.7;
        }
    </style>
</head>

<body>
    <h1>Bearer Token Authentication</h1>
    <p>When working with tokens, like JWT, you need to send the token to the web server along with each HTTP Request.
    </p>
    <p><button id="btnFetch">Click to send a Request</button></p>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('btnFetch').addEventListener('click', sendReq);
            //pretend to get a token after logging in
            sessionStorage.setItem('MyUniqueUserToken',
                JSON.stringify(
                    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
                    )
            );
        });

        let sendReq = (ev) => {
            let url = 'https://jsonplaceholder.typicode.com/posts';
            let token = JSON.parse(sessionStorage.getItem('MyUniqueUserToken'));

            let h = new Headers();
            h.append('Authentication', `Bearer ${token}`);

            let req = new Request(url, {
                method: 'GET',
                mode: 'cors',
                headers: h
            });
            fetch(req)
                .then(resp => resp.json())
                .then(data => {
                    console.log(data[0]);
                })
                .catch(err => {
                    console.error(err.message);
                })
        }
    </script>
</body>

</html>