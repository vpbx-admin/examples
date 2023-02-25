<?php
require_once('Vpbx.php');

define ('VPBX_API_URL', 'https://api.vpbx.pl');

// Uźytkownik i hasło wygenerowane w portalu https://ssl.vpbx.pl
define ('VPBX_API_USERNAME', '');
define ('VPBX_API_PASSWORD', '');

//SMS ID
$sms_id = "";


$vpbx = new Vpbx();

$token_response = $vpbx->Post(VPBX_API_URL . "/api/v1/login", array("username"=> VPBX_API_USERNAME, "password"=> VPBX_API_PASSWORD));
if(isset($token_response['token'])){
	$vpbx->SetAuth($token_response['token']);
	$response = $vpbx->Get(VPBX_API_URL . "/api/v1/sms/" . $sms_id);
        print_r($response);
} else {
	echo "Generowanie tokenu nie powiodło się. Przenalizuj błąd:\n";
	print_r($token_response);
}

?>
