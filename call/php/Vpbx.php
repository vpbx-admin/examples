<?php


class Vpbx {
        public function __construct(){
        }

        public function Post($url, $input)
        {
                return $this->makeRequest($url, "POST", $input);
        }

        public function Get($url)
        {
                return $this->makeRequest($url, "GET");
        }

        public function SetAuth($token){
                $this->auth = $token;
        }


        private function makeRequest($url, $method, $input=null)
        {
                if($input){
                        $body = json_encode($input);
                }
                $headers = array('Content-Type: application/json');
                if(isset($this->auth) && (strlen($this->auth)>10)){
                        array_push($headers, 'Authorization: Bearer '. $this->auth);
                }
                $ch = curl_init();
                curl_setopt($ch, CURLOPT_URL, $url);
                curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
                curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                if(isset($body)){
                        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
                }
                curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
                $result = curl_exec($ch);
                curl_close($ch);
                return  json_decode($result, true);
        }

}

