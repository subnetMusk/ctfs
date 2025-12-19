<?php
    $db_username = "blog";
    $db_password = getenv("MYSQL_BLOG_PASSWORD");
    $db_database = "blog";
    $db_hostname = "db";
    $conn = mysqli_connect($db_hostname, $db_username, $db_password, $db_database);
