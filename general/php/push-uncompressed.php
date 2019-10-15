<html>
<head></head>
<body>
<?php
$fout = fopen("/tmp/push-data.txt", "a") or die ("unable to open file");
$txt = file_get_contents("php://input");
fwrite($fout, $txt);
fclose($fout);
?>
<p>Thank you!</p>
</body>
</html>

