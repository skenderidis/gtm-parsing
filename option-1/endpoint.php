<?php 

$retrieve = $_GET['retrieve'];

header('Content-Type: application/json');

exec("python get_file.py $retrieve  2>&1");

if ($retrieve == "server" )
{
	$result = file_get_contents("server.json");
}
if ($retrieve == "pool" )
{
	$result = file_get_contents("pool.json");
}
if ($retrieve == "wideip" )
{
	$result = file_get_contents("wideip.json");
}

print($result);

?>

