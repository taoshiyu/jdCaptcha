upstream captcha_api {

    least_conn;

    server captcha:5052;
    server captcha:5053;

}

server {

    listen 5051;

    server_name _;

    client_max_body_size 20m;

    location / {

        proxy_pass http://captcha_api;

        proxy_http_version 1.1;

        proxy_set_header Connection "";

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_connect_timeout 10s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;

    }

}