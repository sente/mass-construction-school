

#select the stats and user info by user.uid

uid=$1

if ((100>$uid)) && (($uid>1));
then
    echo "# checking $uid"
else
    echo "bad $uid"
    exit 1
fi


echo "# select"
echo "sqlite3 -header mare/dev.db 'select * from user where user.uid = $uid;'"
echo "sqlite3 -header mare/dev.db 'select * from stats where stats.user_uid = $uid;'"


# delete user/stats by user.uid
echo "# delete"
echo "sqlite3 -header mare/dev.db 'delete from user where user.uid = $uid;'"
echo "sqlite3 -header mare/dev.db 'delete from stats where stats.user_uid = $uid;'"


