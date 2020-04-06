<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "attendance_ensaf";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error . "\n");
echo "Connected successfully.<br><br>";

$value = $_GET['real'];

$conn->query("DROP TABLE `weeks`");

if($value==0){
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
}
elseif ($value==1) {
  $sql = "CREATE TABLE IF NOT EXISTS `weeks`(`number` INT(2) NOT NULL,
                                                  `first_day` VARCHAR(10) NOT NULL,
                                                  `last_day` VARCHAR(10) NOT NULL,
                                                  PRIMARY KEY(number))";
  $conn->query($sql);

  $stmnt = $conn->prepare("INSERT INTO `weeks`(`number`, `first_day`, `last_day`) VALUES (?,?,?)");
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
}



$stmnt->close();
$conn->close();
?>
