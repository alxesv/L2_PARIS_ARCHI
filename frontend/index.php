<?php
function getData($apiUrl)  {

$ch = curl_init();

curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_URL,$apiUrl);
   curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization:token' ,
    ]);
$response = curl_exec($ch);
if (curl_errno($ch)) {
    return array("message"=>'Curl error: ' . curl_error($ch));
}

curl_close($ch);
$data = json_decode($response, true);

if ($data === null) {
    return array("message" =>'Error decoding JSON');
} else {
    return($data);
}
}
$env = parse_ini_file('.env');
$api_url = "". $env["BASE_URL"] . "/api/compteur/";
$compteur_data= getData($api_url)["compteur"];
?>
<html>
    <head>
        <title>Welcome to your_domain!</title>
    </head>
    <body>
	  <h1>Success! </h1>

    <?php if ($compteur_data["message"] !== null or $compteur_data["detail"] !== null): ?>
        <div><?=$compteur_data["message"];?></div>
 	<div><?=$compteur_data["detail"];?></div>
	<?php endif; ?>
	<ul>
        <?php foreach ($compteur_data as $compteur): ?>
        <li><?=$compteur["horodatage"];?> : <?=$compteur["methode"];?></li>
	<?php endforeach; ?>
	</ul>
    </body>
</html>
