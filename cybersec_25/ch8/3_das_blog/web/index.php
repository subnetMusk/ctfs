<?php
include_once('inc/common.php');
?>
<!DOCTYPE html>
<html>
<head>
    <link rel="style.css" type="text/css"/>
    <title>Das Blog</title>
    <style>
        body {
            text-align: center;
            font-family: sans-serif;
            margin: 30px;
        }
        .post {
            border: 1px solid black;
            background-color: #555;
            color: white;
            padding: 10px;
            margin: 10px auto;
            width: 60%;
            border-radius: 6px;
        }
        .post_title {
            text-decoration: underline;
        }
        .welcome {
            margin-bottom: 10px;
        }
        a {
            color: #00bfff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>You have stumbled upon Das Blog</h1>
    </header>
    <div class="container">
    <?php
    if (isset($_COOKIE['permissions']) && isset($_COOKIE['user'])) {

        $username = cleanData($_COOKIE['user']);
        $permissions = $_COOKIE['permissions'];

        echo "<h3 class='welcome'>Welcome $username</h3>";
        echo "<p><a href='login.php?logout=1'>(Logout)</a></p>";

        if (preg_match('/\badmin\b/i', $permissions)) {
            echo "<h4 class='welcome'>You have ADMIN permissions</h4><hr>";

            $query = "SELECT * FROM `posts`;";
            $data = mysqli_query($conn, $query);
            while ($result = mysqli_fetch_assoc($data)) {
                echo "
                <div class='post'>
                    <h3 class='post_title'>{$result['title']}</h3>
                    <div class='post_body'>
                        {$result['content']}
                    </div>
                </div>";
            }
        } else {
            echo "<h4 class='welcome'>You have DEFAULT permissions</h4><hr>";
            $query = "SELECT * FROM `posts` WHERE `permissions`='OPEN';";
            $data = mysqli_query($conn, $query);
            while ($result = mysqli_fetch_assoc($data)) {
                echo "
                <div class='post'>
                    <h3 class='post_title'>{$result['title']}</h3>
                    <div class='post_body'>
                        {$result['content']}
                    </div>
                </div>";
            }
        }
    } else {
        echo "<h4 class='welcome'>You must <a href='login.php'>login</a> to view posts</h4>";
    }
    ?>
    </div>
</body>
</html>
