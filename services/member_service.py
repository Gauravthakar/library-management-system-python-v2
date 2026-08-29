from modules.member_repository import(
    add_member,
    get_all_members,
    get_member_by_id,
    update_member,
    soft_delete_member
)

def create_member(member_id, name, phone, email, address):

    return add_member(member_id, name, phone, email, address)

def get_members():

    return get_all_members()

def get_member(member_id):

    return get_member_by_id(member_id)

def edit_member(member_id, name, phone, email, address):

    return update_member(member_id, name, phone, email, address)

def delete_member(member_id):

    return soft_delete_member(member_id)