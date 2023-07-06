--Get all information for Rental page. Displays Member ID, Item ID, and Transaction ID
SELECT * FROM `rentals`;

--Get all columns for Transaction page. Display Transaction Number, Item Number, Member ID and price
SELECT * FROM `transactions`;

--Get all colums for Movies page.
SELECT * FROM `movies`;

--Get all columns for members page
SELECT * FROM `members`;

--Search function on rentals page. Can search by any column
SELECT * FROM `rentals` WHERE `memberID` = :memberID_selected_from_search_rentals_page;
SELECT * FROM `rentals` WHERE `itemID` = :itemID_selected_from_search_rentals_page;
SELECT * FROM `rentals` WHERE `transactionsID` = :tranasctionID_selected_from_search_rentals_page;

--Search function on members page. Can search by any column
SELECT * FROM `members` WHERE `memberID` = :memberID_selected_from_search_rentals_page;
SELECT * FROM `members` WHERE `member_name` = :member_name_selected_from_search_rentals_page;
SELECT * FROM `members` WHERE `email` = :email_selected_from_search_rentals_page;

--Search function on transactions page. Search by any column
SELECT * FROM `transactions` WHERE `transactionID` = :transactionID_selected_from_search_rentals_page;
SELECT * FROM `transactions` WHERE `itemID` = :itemID_selected_from_search_rentals_page;
SELECT * FROM `transactions` WHERE `memberID` = :transactionID_selected_from_search_rentals_page;

--Search function on movies page. Search by any column
SELECT * FROM `movies` WHERE `itemID` = :itemID_selected_from_search_rentals_page;
SELECT * FROM `movies` WHERE `title` = :title_selected_from_search_rentals_page;
SELECT * FROM `movies` WHERE `release_year` = :release_year_selected_from_search_rentals_page;

--Add new movie
INSERT INTO `movies` (`title`, `release_year`, `in_stock`, `qty`, `rental_price`) VALUES (:title, :release_year, :in_stock, :qty, :rental_price);

--Add new transaction
INSERT INTO `transactions` (`itemID`, `memberID`, `rental_price`) VALUES (:itemID, :memberID, :rental_price);

--Add new member
INSERT INTO `members` ( `member_name`, `email`) VALUES (:fname, :lname, :email);

--Delete Member
DELETE FROM `members` WHERE `memberID` = :memberID_user_selected;

--Delete Movie
DELETE FROM `movies` WHERE `itemID` = :movieID_user_selected;

--Add new rental
INSERT INTO `rentals` (`memberID`, `itemID`, `transactionID`) VALUES (:memberID, itemID, transactionID);