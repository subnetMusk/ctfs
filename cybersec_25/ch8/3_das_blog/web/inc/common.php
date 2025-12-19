<?php
// Database configuration via environment variables (with sane defaults)
session_start();
include_once('db_init.php');
function cleanData($str) {
    return htmlspecialchars(urldecode($str), ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}
?>
