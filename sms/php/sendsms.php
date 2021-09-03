<?php
require_once('Vpbx.php');

define ('VPBX_API_URL', 'https://api.vpbx.pl');

// Uźytkownik i hasło wygenerowane w portalu https://ssl.vpbx.pl
define ('VPBX_API_USERNAME', '');
define ('VPBX_API_PASSWORD', '');

//Numer, na jaki wysyłany jest SMS w formacie E164  https://en.wikipedia.org/wiki/E.164
$number = "48500000000";

//Tekst wiadomości SMS. Jeśli używane są polskie znaki, maksymalna długość pierwszej wiadomości to 70 znaków
$text   = "To jest wiadomość testowa z VPBX.PL";


$vpbx = new Vpbx();

$token_response = $vpbx->Post(VPBX_API_URL . "/api/v1/login", array("username"=> VPBX_API_USERNAME, "password"=> VPBX_API_PASSWORD));
if(isset($token_response['token'])){
	$vpbx->SetAuth($token_response['token']);
	$response = $vpbx->Post(VPBX_API_URL . "/api/v1/sms" , array("from" => "callapi.pl","to" => $number,"text" => $text));
        print_r($response);
} else {
	echo "Generowanie tokenu nie powiodło się. Przenalizuj błąd:\n";
	print_r($token_response);
}

?>
