<?php
if (session_status()!==PHP_SESSION_ACTIVE)session_start();

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
    return $response;
}
function verify_input($data) {
	$data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
}
$env = parse_ini_file('.env');
if(isset($_POST['url'])) {
    	$uri = verify_input($_POST['url']);
	$uri_split = explode("/", $uri);
	$uri_split = array_filter($uri_split, function($value) { return !is_null($value) && $value !== ''; });
	if(count($uri_split) === 2){
	 	if($uri[strlen($uri)-1] !== "/"){
                	$uri = $uri . "/";
        	}
	}else{
		if($uri[strlen($uri)-1] === "/"){
                	$uri =  substr($uri, 0,-1);
        	}
	}
    	$api_url =  "". $env["BASE_URL"] .$uri;
	$data = getData($api_url);
} else {
    	$api_url_default =  "". $env["BASE_URL"]. "/";
    	$data = getData($api_url_default);
}

$_SESSION['data'] = $data;

header("Location: /index.php");
exit;
?>
