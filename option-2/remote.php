<?php 

$username = "user";
$password = "pass";
$bigip_ip = "192.168.5.91";
$retrieve = $_GET['retrieve'];


if ($retrieve == "pool")
{
	$data = '{
		"command": "run",
		"utilCmdArgs": "-c /config/pool.sh"
	}';
}
if ($retrieve == "wideip")
{
	$data = '{
		"command": "run",
		"utilCmdArgs": "-c /config/wideip.sh"
		}';
}
if ($retrieve == "servers")
{
	$data = '{
		"command": "run",
		"utilCmdArgs": "-c /config/servers.sh"
		}';
}


$ch = curl_init();

$url = 'https://'.$bigip_ip .'/mgmt/tm/util/bash';
$header = array();
$header[] = 'Content-type: application/json';
$header[] = 'Authorization: Basic '.base64_encode($username.":".$password);

curl_setopt($ch, CURLOPT_URL, $url); 
curl_setopt($ch, CURLOPT_HTTPHEADER,$header);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ch, CURLOPT_POST,true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data); 
curl_setopt($ch, CURLOPT_TIMEOUT_MS, 60000);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$info = curl_getinfo($ch);

if (!curl_errno($ch)) {
	$data = json_decode($response, true);
	$json_output = json_decode($data['commandResult'], true);
}
curl_close($ch);

print (json_encode($json_output, true));

?>

