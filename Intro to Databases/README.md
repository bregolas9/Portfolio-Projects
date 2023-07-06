Specifications

    - Your database should be pre-populated with sample data. At least three rows per table is 
        expected. The sample data should illustrate a table's functionality, e.g. if the table is part of a many-to-many relationship, the sample data should depict M:M.
    - Your database should have at least 4 entities and at least 4 relationships, one of which 
        must be a many-to-many relationship.  The entities and relationships should implement the operational requirements of your project.
    - You are creating a web interface for data tables, so the primary user is the administrator 
        of this database.
         - It is NOT a customer facing website; thus there is no need for login page; sessions; 
            register/password; shopping cart; check-out; etc.  While having those pages would be helpful in many customer facing applications, the purpose of this project is to provide a UI for your tables. 
        - Put another way, if you had 4 entities that were implemented as 5 tables in a 
            database, then we expect roughly 5 web app pages as a front end for each of the 5 tables in your database.
        - The one exception is oftentimes it works better for the end-user to have a single web 
            page for a Many-to-Many relationship between 2 tables (so the user doesn't have to view two pages to complete a transaction in both tables). So in that case if you had 4 entities that were implemented as 5 tables, with 1 many-to-many relationship between 2 of those tables, and the 2 tables in that m:m were managed on a single web page, then we expect 4 web pages in the project. 
    - It should be possible to INSERT entries into every table individually.
    - Every table should be used in at least one SELECT query. For the SELECT queries, it is 
        fine to just display the content of the tables, but your website needs to also have the ability to search using text or filter using a dynamically populated list of properties. This search/filter functionality should be present for at least one entity. It is generally not appropriate to have only a single query that joins all tables and displays them.
    - You need to include one DELETE and one UPDATE function in your website, for any one of the 
        entities. In addition, it should be possible to add and remove things from at least one many-to-many relationship and it should be possible to add things to all relationships. This means you need INSERT functionality for all relationships as well as entities. And DELETE for at least one many-to-many relationship.
    - In a one-to-many relationship (like bsg_people to bsg_planets), you should be able to set 
        the foreign key value to NULL (such as on a person in bsg_people), that removes the relationship. In case none of the one-to-many relationships in your database has partial participation, you would need to change that to make sure at least one relation can have NULL values. For example in a sales_invoice table for example, having a customer relation (e.g. customer_id FK) could be mandatory, but having an employee relation (e.g. sales_employee_id FK) could be optional and nullable. 
    - In a many-to-many relationship, to remove a relationship one would need to delete a row 
        from a table. That would be the case with bsg_people and bsg_certifications. One should be able to add and remove certifications for a person without deleting either bsg_people rows or bsg_certification rows. If you implement DELETE functionality on at least (1) many-to-many relationship table, such that the rows in the relevant entity tables are not impacted, that is sufficient.
