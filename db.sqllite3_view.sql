BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Order" (
	"UserID"	INTEGER NOT NULL,
	"Date Ordered"	DATE NOT NULL,
	"Ordered Items"	INTEGER NOT NULL,
	FOREIGN KEY("UserID") REFERENCES "User"("UserId"),
	FOREIGN KEY("Ordered Items") REFERENCES "Product"("ProductID")
);
CREATE TABLE IF NOT EXISTS "Product" (
	"ProductID"	INTEGER NOT NULL,
	"ProductName"	TEXT NOT NULL,
	"Price"	FLOAT(10, 2) NOT NULL,
	"Stock"	INTEGER,
	PRIMARY KEY("ProductID")
);
CREATE TABLE IF NOT EXISTS "User" (
	"UserId"	INTEGER NOT NULL,
	"Username"	varchar(10) NOT NULL UNIQUE,
	"Password"	varchar(10) NOT NULL UNIQUE,
	"Email"	varchar(45) NOT NULL,
	"AccountBalance"	FLOAT (10,2),
	PRIMARY KEY("UserId")
);
INSERT INTO "Product" ("ProductID","ProductName","Price","Stock") VALUES (1544,'GI Joe Action Figure',26.1,9),
 (2662,'Lego Set',87.26,4),
 (3215,'Chips',2.69,20),
 (5986,'Bottled Water',1.17,45),
 (7412,'Graphic Tee',32.99,5),
 (7845,'Dog Collar',3.45,15);
INSERT INTO "User" ("UserId","Username","Password","Email","AccountBalance") VALUES (1,'Pat_15','IlUv_Refs','3peat@gmail.com',2500.0),
 (2,'RL_52','Mans_Game','ravensLB@yahoo.com',2500.0),
 (3,'DAK_4','Romo=Dak','wedemboys@hotmail.com',2500.0),
 (4,'RG_3','@Gone2Soon','newknees@bing.com',2500.0);
COMMIT;
