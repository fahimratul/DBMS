<?php

$username = 'rapid';
$password = '1972';
$connection_string = 'localhost/XE';  // Or whatever service you're using


// Establish a connection to the Oracle database

$conn = oci_connect($username, $password, $connection_string);

if (!$conn) {
    $e = oci_error();
    echo "Connection failed: " . $e['message'];
    exit;
} else {
    echo "✅ Connected to Oracle Database successfully!";
}

// Close the connection when done

?>
