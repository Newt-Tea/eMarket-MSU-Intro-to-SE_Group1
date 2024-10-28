BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Order" (
	"UserID"	INTEGER NOT NULL,
	"Date Ordered"	DATE NOT NULL,
	"Ordered Items"	INTEGER NOT NULL,
	FOREIGN KEY("UserID") REFERENCES "User"("id"),
	FOREIGN KEY("Ordered Items") REFERENCES "Product"("id")
);
CREATE TABLE IF NOT EXISTS "Product" (
	"id"	INTEGER NOT NULL,
	"ProductName"	TEXT NOT NULL,
	"Price"	FLOAT(10, 2) NOT NULL,
	"Stock"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "User" (
	"id"	INTEGER NOT NULL,
	"Username"	varchar(10) NOT NULL UNIQUE,
	"Password"	varchar(10) NOT NULL UNIQUE,
	PRIMARY KEY("id")
);
INSERT INTO "Product" ("ProductID","ProductName","Price","Stock") VALUES 
 (1544,'GI Joe Action Figure',26.1,9),
 (2662,'Lego Set',87.26,4),
 (3215,'Chips',2.69,20),
 (5986,'Bottled Water',1.17,45),
 (7412,'Graphic Tee',32.99,5),
 (7845,'Dog Collar',3.45,15);
INSERT INTO "User" ("UserId","Username","Password") VALUES 
 (1,'Pat_15','IlUv_Refs'),
 (2,'RL_52','Mans_Game'),
 (3,'DAK_4','Romo=Dak'),
 (4,'RG_3','@Gone2Soon');
COMMIT;
