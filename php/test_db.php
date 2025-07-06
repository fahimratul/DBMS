<?php
require_once '../configure.php';

if ($conn) {
    echo "Database connection successful\n";
    
    // Check if table exists
    $sql = "SELECT table_name FROM user_tables WHERE table_name = 'DONATION_REQUESTS'";
    $stmt = oci_parse($conn, $sql);
    oci_execute($stmt);
    $row = oci_fetch_array($stmt);
    
    if ($row) {
        echo "Table DONATION_REQUESTS exists\n";
        
        // Show table structure
        $sql2 = "SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'DONATION_REQUESTS' ORDER BY column_id";
        $stmt2 = oci_parse($conn, $sql2);
        oci_execute($stmt2);
        
        echo "Table structure:\n";
        while ($row2 = oci_fetch_array($stmt2)) {
            echo "- " . $row2['COLUMN_NAME'] . " (" . $row2['DATA_TYPE'] . ")\n";
        }
        oci_free_statement($stmt2);
    } else {
        echo "Table DONATION_REQUESTS does not exist\n";
        echo "Creating table...\n";
        
        $create_sql = "CREATE TABLE donation_requests (
            id NUMBER PRIMARY KEY,
            name VARCHAR2(100) NOT NULL,
            phone VARCHAR2(20) NOT NULL,
            emergency_phone VARCHAR2(20),
            district VARCHAR2(50) NOT NULL,
            postal_code VARCHAR2(10) NOT NULL,
            address CLOB NOT NULL,
            message CLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )";
        
        $sequence_sql = "CREATE SEQUENCE donation_requests_seq START WITH 1 INCREMENT BY 1";
        $trigger_sql = "CREATE OR REPLACE TRIGGER donation_requests_trigger 
            BEFORE INSERT ON donation_requests
            FOR EACH ROW
            BEGIN
                :NEW.id := donation_requests_seq.NEXTVAL;
            END;";
        
        $create_stmt = oci_parse($conn, $create_sql);
        if (oci_execute($create_stmt)) {
            echo "Table created successfully\n";
            
            // Create sequence
            $seq_stmt = oci_parse($conn, $sequence_sql);
            if (oci_execute($seq_stmt)) {
                echo "Sequence created successfully\n";
                
                // Create trigger
                $trigger_stmt = oci_parse($conn, $trigger_sql);
                if (oci_execute($trigger_stmt)) {
                    echo "Trigger created successfully\n";
                } else {
                    $e = oci_error($trigger_stmt);
                    echo "Error creating trigger: " . $e['message'] . "\n";
                }
                oci_free_statement($trigger_stmt);
            } else {
                $e = oci_error($seq_stmt);
                echo "Error creating sequence: " . $e['message'] . "\n";
            }
            oci_free_statement($seq_stmt);
        } else {
            $e = oci_error($create_stmt);
            echo "Error creating table: " . $e['message'] . "\n";
        }
        oci_free_statement($create_stmt);
    }
    
    oci_free_statement($stmt);
    oci_close($conn);
} else {
    $e = oci_error();
    echo "Database connection failed: " . $e['message'] . "\n";
}
?>
