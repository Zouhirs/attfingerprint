<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "attendance_ensaf";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error . "\n");
echo "Connected successfully.<br><br>";

$conn->query("DROP TABLE `real_weeks`");
$sql = "CREATE TABLE IF NOT EXISTS `real_weeks`(`number` INT(2) NOT NULL,
                                                `first_day` VARCHAR(10) NOT NULL,
                                                `last_day` VARCHAR(10) NOT NULL,
                                                PRIMARY KEY(number))";
$conn->query($sql);

$stmnt = $conn->prepare("INSERT INTO `real_weeks`(`number`, `first_day`, `last_day`) VALUES (?,?,?)");
$stmnt->bind_param("iss", $number, $first_day, $last_day);

$datetime = new DateTime('2020-01-27');

for ($i=1; $i <=13 ; $i++) {
  $number = $i;
  $first_day = $datetime->format('Y-m-d');
  $datetime->modify('+5 day');
  $last_day = $datetime->format('Y-m-d');
  $stmnt->execute();
  if($i==10) $datetime->modify('+9 day');
  else $datetime->modify('+2 day');
}

$stmnt->close();
$conn->close();
?>
