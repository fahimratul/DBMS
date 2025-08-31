SELECT receiver.name AS name,
    (SELECT item.name 
    FROM stock
    JOIN item 
    ON stock.item_id = item.item_id) AS item
FROM donation_receiver
JOIN receiver ON donation_receiver.receiver_id = receiver.receiver_id
JOIN stock ON donation_receiver.stock_id = stock.stock_id;

SELECT item.name FROM stock
JOIN ITEM ON stock.item_id = item.item_id;

SELECT receiver.name AS receiver_name, item.name AS item_name
FROM donation_receiver
JOIN receiver ON donation_receiver.receiver_id = receiver.receiver_id
JOIN stock ON donation_receiver.stock_id = stock.stock_id
JOIN item ON stock.item_id = item.item_id
WHERE donation_receiver.date = (
    SELECT MAX(donation_receiver2.date)
    FROM donation_receiver donation_receiver2
    WHERE donation_receiver2.receiver_id = donation_receiver.receiver_id
);

SELECT r.name AS receiver_name, i.name AS item_name
FROM donation_receiver dr
JOIN receiver r ON dr.receiver_id = r.receiver_id
JOIN stock s ON dr.stock_id = s.stock_id
JOIN item i ON s.item_id = i.item_id
WHERE dr.request_date = (
    SELECT MAX(dr2.request_date)
    FROM donation_receiver dr2
    WHERE dr2.receiver_id = dr.receiver_id
);


SELECT name, profile_picture FROM volunteer;

-- Simple error handling with CASE
SELECT 
    volunteer_id,
    name,
    CASE 
        WHEN profile_picture IS NULL THEN 'No profile picture'
        WHEN LENGTH(profile_picture) = 0 THEN 'Empty profile picture'
        ELSE CONCAT('Profile picture available (', LENGTH(profile_picture), ' bytes)')
    END AS picture_status
FROM volunteer;