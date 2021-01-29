<?php
if(isset($_GET['url'])){
$url = $_GET['url'];
header('Content-Type: application/json');
echo file_get_contents($url);
}
else{ 
echo 'url not provided';
}
?>