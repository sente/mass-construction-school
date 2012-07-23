-- load_data.sql
-- This should be ran after `schema.sql`


-- CREATE VIDEO ENTRIES



INSERT INTO "video" VALUES(1,'video_1',6089,'Video 1');
INSERT INTO "video" VALUES(2,'video_2',6394,'Video 2');
INSERT INTO "video" VALUES(3,'video_3',5577,'Video 3');
INSERT INTO "video" VALUES(4,'video_4',5886,'Video 4');
INSERT INTO "video" VALUES(5,'video_5',6489,'Video 5');
INSERT INTO "video" VALUES(6,'video_6',4616,'Video 6');


-- CREATE A TEST USER ENTRY

INSERT INTO "user" VALUES(1,'Stuart Powers','stuart.powers@gmail.com','test',69,NULL);

-- CREATE STATS ENTIRES FOR THE TEST USER

INSERT INTO "stats" VALUES(1,1,1,0,1);
INSERT INTO "stats" VALUES(2,1,2,0,0);
INSERT INTO "stats" VALUES(3,1,3,0,0);
INSERT INTO "stats" VALUES(4,1,4,0,0);
INSERT INTO "stats" VALUES(5,1,5,0,0);
INSERT INTO "stats" VALUES(6,1,6,0,0);
