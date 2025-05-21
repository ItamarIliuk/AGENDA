from agenda_structures import AgendaItem
from agenda_data_handler import read_agenda_items, write_agenda_items, get_sequential

def _load_contacts_and_seq() -> tuple[list[AgendaItem], int]:
    """
    Helper function to load contacts and the current sequence number.
    """
    items = read_agenda_items()
    seq = get_sequential()
    return items, seq

def add_contact(nome: str, fixo: str, celular: str, comercial: str) -> AgendaItem:
    """
    Adds a new contact to the agenda.
    Increments the sequence number for the new contact's code.
    Saves the updated list and sequence number to the file.
    Returns the newly created AgendaItem.
    """
    items, seq = _load_contacts_and_seq()
    
    new_seq = seq + 1
    new_item = AgendaItem(codigo=new_seq, nome=nome, fone_fixo=fixo, fone_celular=celular, fone_comercial=comercial)
    items.append(new_item)
    
    write_agenda_items(items, new_seq)
    return new_item

def list_contacts() -> list[AgendaItem]:
    """
    Retrieves all contacts from the agenda.
    Returns a list of AgendaItem objects.
    """
    items, _ = _load_contacts_and_seq()
    return items

def search_contact_by_name(query_name: str) -> list[AgendaItem]:
    """
    Searches for contacts by name.
    Returns a list of AgendaItem objects where query_name is a case-insensitive substring of item.nome.
    """
    items, _ = _load_contacts_and_seq()
    query_lower = query_name.lower()
    return [item for item in items if query_lower in item.nome.lower()]

def search_contact_by_code(query_code: int) -> AgendaItem | None:
    """
    Searches for a contact by its code.
    Returns the AgendaItem if found, otherwise None.
    """
    items, _ = _load_contacts_and_seq()
    for item in items:
        if item.codigo == query_code:
            return item
    return None

def update_contact(code: int, nome: str, fixo: str, celular: str, comercial: str) -> AgendaItem | None:
    """
    Updates an existing contact's details.
    If a provided detail string is empty, the existing value for that detail is kept.
    Saves the modified list to the file. The sequence number is not changed.
    Returns the updated AgendaItem, or None if the contact code is not found.
    """
    items, seq = _load_contacts_and_seq()
    
    target_item: AgendaItem | None = None
    item_index = -1

    for i, item in enumerate(items):
        if item.codigo == code:
            target_item = item
            item_index = i
            break
            
    if target_item is None:
        return None
        
    # Update fields only if new value is provided (not an empty string)
    if nome:
        target_item.nome = nome
    if fixo:
        target_item.fone_fixo = fixo
    if celular:
        target_item.fone_celular = celular
    if comercial:
        target_item.fone_comercial = comercial
        
    # Replace the old item with the updated one in the list
    # This is mostly for clarity or if AgendaItem was immutable, though here it's mutable
    items[item_index] = target_item 
    
    write_agenda_items(items, seq) # Use the original sequence number
    return target_item
