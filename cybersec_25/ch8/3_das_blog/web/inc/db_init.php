<?php
$db_hostname  = getenv('DB_HOST') ?: 'db';
$db_username = getenv('DB_USER') ?: 'web';
$db_password = getenv('DB_PASSWORD') ?: 'db';
$db_database = getenv('DB_NAME') ?: 'dasblog';

$conn = mysqli_connect($db_hostname, $db_username, $db_password, $db_database);
?>