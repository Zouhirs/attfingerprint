<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "attendance_ensaf";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error . "\n");
echo "Connected successfully.<br><br>";

$sql = "SELECT `id` FROM subjects";

$result = $conn->query($sql);

while($row = $result->fetch_assoc()) {
    $sql = "DROP TABLE `".$row['id']."`";
    $conn->query($sql);
}

$conn->close();
?>
