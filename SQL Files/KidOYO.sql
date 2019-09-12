CREATE TABLE Person (
    PersonID VARCHAR(50),
    Gender CHAR(1),
    PRIMARY KEY (PersonID)
);

#Person Gender
DELIMITER $
CREATE TRIGGER Insert_IsPerson_M_F_O BEFORE INSERT ON Person 
FOR EACH ROW
BEGIN
    IF NEW.Gender NOT IN ('M', 'F', 'O')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Gender must be M or F or N';
    END IF;
END$
DELIMITER ;

INSERT INTO	Person VALUES('Bobby', 'M');

CREATE TABLE Items (
	ItemID INT,
    ItemName VARCHAR(50) NOT NULL,
    ImageName VARCHAR(50),
    ItemDesc VARCHAR(200),
    PersonID VARCHAR(50),
    PRIMARY KEY (ItemID),
    FOREIGN KEY (PersonID)
        REFERENCES Person (PersonID)
);

INSERT INTO Items VALUES('1', 'KIDOYO LOGO', 'oyoyo.png', 'Just for testing', 'Bobby');


SELECT * FROM Person INNER JOIN Items ON Person.PersonID = Items.PersonID;
SELECT * FROM Items INNER JOIN Person ON Items.PersonID = 'Bobby' AND Person.PersonID = 'Bobby';

#create index 
CREATE TABLE Cars (
	CarID INT,
    CarType VARCHAR(30) NOT NULL,
    CarPrice INT NOT NULL,
    PRIMARY KEY (CarID)
);

INSERT INTO Cars VALUES('1', 'BMW', '3000');
INSERT INTO Cars VALUES('2', 'Audi', '5000');
INSERT INTO Cars VALUES('3', 'BMW', '6000');

CREATE INDEX cartype ON Cars (CarType)