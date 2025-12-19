<?php
require_once('inc/common.php');
$output = '';
$show_form = true;

// Logout
if (isset($_GET['logout'])) {
    setcookie('user', '', time() - 3600, '/');
    setcookie('permissions', '', time() - 3600, '/');
    $output = 'You have been logged out successfully. Please login again.';
    $show_form = true;
}

// Se già loggato e non in logout
elseif (isset($_COOKIE['user']) && isset($_COOKIE['permissions'])) {
    $username = cleanData($_COOKIE['user']);
    $output = "You are already logged in as <strong>$username</strong>. "
            . '<a href="?logout=1">Logout</a>';
    $show_form = false;
}

// Tentativo di login
elseif (isset($_POST['Username']) && isset($_POST['Password'])) {
    $name = mysqli_real_escape_string($conn, $_POST['Username']);
    $pass = mysqli_real_escape_string($conn, $_POST['Password']);

    $sql = "SELECT `name`, `permissions` FROM `users` 
            WHERE `name`='$name' AND `password`='$pass' LIMIT 1;";
    $data = mysqli_query($conn, $sql);

    if ($data && mysqli_num_rows($data) > 0) {
        $result = mysqli_fetch_assoc($data);
        $name = $result['name'];
        $perm = $result['permissions'];

        // Imposta cookie e reindirizza
        setcookie('user', $name, 0, "/");
        setcookie('permissions', $perm, 0, "/");
        header('Location: index.php');
        exit();
    } else {
        $output = 'Sorry, that username or password is incorrect.';
        $show_form = true;
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Das Blog Login</title>
    <style>
        body { text-align: center; font-family: sans-serif; margin-top: 50px; }
        form { display: inline-block; text-align: left; margin-top: 20px; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h2>Login Page</h2>
    <p><?php echo $output ? $output : 'Please login below:'; ?></p>

    <?php if ($show_form): ?>
    <form action="?" method="post">
        <label for="Username">Username</label>
        <input type="text" name="Username" required>
        <br><br>
        <label for="Password">Password</label>
        <input type="password" name="Password" required>
        <br><br>
        <input type="submit" name="submit" value="Login">
    </form>
    <?php endif; ?>
</body>
</html>
