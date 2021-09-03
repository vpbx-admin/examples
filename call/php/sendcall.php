<?php
require_once('Vpbx.php');

define ('VPBX_API_URL', 'https://api.vpbx.pl');

// Uźytkownik i hasło wygenerowane w portalu https://ssl.vpbx.pl
define ('VPBX_API_USERNAME', '');
define ('VPBX_API_PASSWORD', '');


#Numer docelowy (E164)
$number = "48500000000";
#Numer dzwoniący (E164)
$from_number = "48224723555";


$call_object = array(
    "from" => $from_number,
    "to"=> $number,
    "ring_timeout" => 30,
    "objects" => array(
        array( "type" => "answer"),
        array( "type" => "wait", "params" => array( "time" => 2 )),
        array( "type" =>  "tts", "params" => array( "text" => "Twój jednorazowy kod to: 1. 2. 3. 4.", "lang" => "pl-PL/Maja")), 
	array( "type" =>  "tts", "params" => array( "text" => "Powtarzam: Twój jednorazowy kod to: 1. 2. 3. 4.", "lang" => "pl-PL/Maja")),
        array( "type" => "hangup"),
    )
);


$vpbx = new Vpbx();

$token_response = $vpbx->Post(VPBX_API_URL . "/api/v1/login", array("username"=> VPBX_API_USERNAME, "password"=> VPBX_API_PASSWORD));
if(isset($token_response['token'])){
	$vpbx->SetAuth($token_response['token']);
	$response = $vpbx->Post(VPBX_API_URL . "/api/v1/callobject" , $call_object);
        print_r($response);
} else {
	echo "Generowanie tokenu nie powiodło się. Przenalizuj błąd:\n";
	print_r($token_response);
}

?>
