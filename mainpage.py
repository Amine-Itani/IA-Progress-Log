posts_2 = db.search("SELECT posts.*, users.username, users.image, users.email, topics.color FROM posts JOIN users ON posts.user_id = users.id JOIN topics ON posts.topic = topics.topic JOIN follows ON posts.user_id = follows.following WHERE follows.user_id = ? and posts.user_id = follows.following ORDER BY date DESC", multiple=True, params=(user_id,))
    for p in posts:
        db.run_query(f"UPDATE posts SET myself = ?", (False,))
    for p in posts:
        db.run_query(f"update posts set myself = TRUE where user_id = ?", (current_user_id,))
        if does_user_follow(current_user_id, int(p[1])):
            db.run_query(f"update posts set following_state = 'Unfollow' where user_id = ?", (current_user_id,))
        else:
            db.run_query("UPDATE posts SET following_state = 'Follow' WHERE user_id = ?", (current_user_id,))

if request.form.get('follow'): # here you must program the functionality of each follow button
    # databse queries for checks explained above

    if myself: # this will check if the post author is the current user and switch the follow button to delete if that is true 
        db.run_query(f"delete from posts where id = ?", (post_id,))

    if following_state == 'Not_following': # these queries will follow the post author
        db.insert(f"INSERT INTO follows (user_id, following) VALUES (?, ?)", (current_user_id, post_id))
        db.run_query(f"UPDATE posts SET following_state = 'Following' WHERE id = ?", (post_id,))

    else: # these queries will unfollow the post author
        db.run_query(f"DELETE FROM follows WHERE user_id = ? AND following = ?", (current_user_id, post_id))
        db.run_query(f"UPDATE posts SET following_state = 'Not_following' WHERE id = ?", (post_id,))
