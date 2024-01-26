<?php

if (session_status()!==PHP_SESSION_ACTIVE)session_start();
if (isset($_SESSION['data'])){
    $data = $_SESSION['data'];
    unset($_SESSION['data']);
}
?>
<html>
    <head>
        <title>Welcome to your_domain!</title>
    </head>
    <body>
    <h1>Home </h1>
    <form method="POST" action="index_submit.php"><input type="text" name="url"/><button type="submit">Envoyer</button></form>
<div><?= $data ?></div>
</body>
</html>
