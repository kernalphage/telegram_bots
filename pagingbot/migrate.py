import pickle
import string
chatroom_database = open("chatroom.db", "rb")
chatroom_pages = pickle.load(chatroom_database)

def write_to_cache(pages):
    cache = open("chatroom.db", "wb")
    pickle.dump(pages, cache)

valid_chars = string.digits + string.ascii_letters + "_"

def sanitize_tag(tag):
	_tag = "".join([c for c in tag if c in valid_chars])
	_tag = _tag.rstrip('s')	
	return _tag

mod_chats = {}

for room in chatroom_pages:
	print(room)
	cur_room = chatroom_pages[room]
	mod_room = {}
	for tag in cur_room:
		clean_tag = sanitize_tag(tag)
		if not clean_tag: continue
		print(clean_tag)
		mod_tag = mod_room.get(clean_tag, set())
		mod_tag |= cur_room[tag]
		mod_room[clean_tag] = mod_tag
	mod_chats[room] = mod_room

write_to_cache(mod_chats)

for room in mod_chats:
	cur_room = mod_chats[room]
	print(room)
	for tag in cur_room:
		print("\t{}: {}".format(tag, cur_room[tag]))	
