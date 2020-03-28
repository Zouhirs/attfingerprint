<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "attendance_ensaf";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error . "\n");
echo "Connected successfully.<br><br>";

$conn->query("DROP TABLE `weeks`");
$sql = "CREATE TABLE IF NOT EXISTS `weeks`(`number` INT(2) NOT NULL,
                                           `days` VARCHAR(10) NOT NULL,
                                            PRIMARY KEY(number))";
$conn->query($sql);

$stmnt = $conn->prepare("INSERT INTO `weeks`(`number`, `days`) VALUES (?,?)");
$stmnt->bind_param("is", $number, $days);

$datetime = new DateTime(date('d-m-Y'));

for ($i=1; $i <=13 ; $i++) {
  $number = $i;
  $days = $datetime->format('Y-m-d');
  $stmnt->execute();
  $datetime->modify('+1 day');
}

$stmnt->close();
$conn->close();
?>
