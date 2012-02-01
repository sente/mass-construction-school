-- load_data.sql
-- This should be ran after `schema.sql`


-- CREATE VIDEO ENTRIES

INSERT INTO "video" VALUES(1,'module1_1a',2488,'Module 1 - Part 1');
INSERT INTO "video" VALUES(2,'module1_2a',3479,'Module 1 - Part 2');
INSERT INTO "video" VALUES(3,'module1_3a',56,'Module 1 - Part 3');
INSERT INTO "video" VALUES(4,'module2_1',1099,'Module 2 - Part 1');
INSERT INTO "video" VALUES(5,'module2_2',4548,'Module 2 - Part 2');
INSERT INTO "video" VALUES(6,'module3_1a',3501,'Module 3 - Part 1');
INSERT INTO "video" VALUES(7,'module3_2a',2068,'Module 3 - Part 2');
INSERT INTO "video" VALUES(8,'module4_1a',3094,'Module 4 - Part 1');
INSERT INTO "video" VALUES(9,'module4_2a',2651,'Module 4 - Part 2');
INSERT INTO "video" VALUES(10,'module5_1a',2160,'Module 5 - Part 1');
INSERT INTO "video" VALUES(11,'module5_2a',2380,'Module 5 - Part 2');
INSERT INTO "video" VALUES(12,'module5_3a',1441,'Module 5 - Part 3');
INSERT INTO "video" VALUES(13,'module6_1a',3443,'Module 6 - Part 1');
INSERT INTO "video" VALUES(14,'module6_2a',2437,'Module 6 - Part 2');
INSERT INTO "video" VALUES(15,'module6_3a',104,'Module 6 - Part 3');


-- CREATE A TEST USER ENTRY

INSERT INTO "user" VALUES(1,'Stuart Powers','stuart.powers@gmail.com','test',NULL);


-- CREATE STATS ENTIRES FOR THE TEST USER

INSERT INTO "stats" VALUES(1,1,1,0,1);
INSERT INTO "stats" VALUES(2,1,2,0,0);
INSERT INTO "stats" VALUES(3,1,3,0,0);
INSERT INTO "stats" VALUES(4,1,4,0,0);
INSERT INTO "stats" VALUES(5,1,5,0,0);
INSERT INTO "stats" VALUES(6,1,6,0,0);
INSERT INTO "stats" VALUES(7,1,7,0,0);
INSERT INTO "stats" VALUES(8,1,8,0,0);
INSERT INTO "stats" VALUES(9,1,9,0,0);
INSERT INTO "stats" VALUES(10,1,10,0,0);
INSERT INTO "stats" VALUES(11,1,11,0,0);
INSERT INTO "stats" VALUES(12,1,12,0,0);
INSERT INTO "stats" VALUES(13,1,13,0,0);
INSERT INTO "stats" VALUES(14,1,14,0,0);
INSERT INTO "stats" VALUES(15,1,15,0,0);
