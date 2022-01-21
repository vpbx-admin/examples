<?php
use Firebase\JWT\JWT;
use Firebase\JWT\Key;



$key = "Klucz do podpisu";
// HS256 lub HS512
$method = "HS256";

$authorization_header = $_SERVER["HTTP_AUTHORIZATION"];
$val = explode(" ", $authorization_header);

$jwt = $val[1];

try {
        $decoded = JWT::decode($jwt, new Key($key, $method));
} catch (Exception $e) {
        http_response_code(500);
        echo 'Caught exception: ',  $e->getMessage(), "\n";
        exit;

}

$decoded_array = (array) $decoded;

//check the payload hash (not required if you are using HTTPS)

if (isset($_POST)) {

    $payload = file_get_contents('php://input');
    $hexHash = hash_hmac('sha256', $payload, utf8_encode($key));
    $base64Hash = base64_encode(hex2bin($hexHash));
    if($base64Hash != $decoded_array['hash']){
        http_response_code(500);
        echo 'Payload hash is invalid';
        exit;
    }
    echo 'ok';
}
?>

