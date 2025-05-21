import struct
from agenda_structures import AgendaItem

AGENDA_FILE = "agenda.dat"
STRUCT_FORMAT = "i100s20s20s20s"  # Total size: 4 + 100 + 20 + 20 + 20 = 164 bytes per record
STRING_ENCODING = 'latin-1'

def initialize_agenda_file():
    """
    Opens AGENDA_FILE in binary write mode ("wb").
    Writes an initial sequence number of 0 (as a 4-byte integer) to the file.
    Closes the file.
    """
    with open(AGENDA_FILE, "wb") as f:
        f.write(struct.pack("i", 0))

def get_sequential() -> int:
    """
    Opens AGENDA_FILE in binary read mode ("rb").
    Reads the first 4 bytes (integer).
    Unpacks it to an integer.
    Closes the file and returns the integer.
    If FileNotFoundError occurs, call initialize_agenda_file() and then return 0.
    If any other error occurs (e.g., file too short), also attempt to initialize and return 0.
    """
    try:
        with open(AGENDA_FILE, "rb") as f:
            data = f.read(4)
            if len(data) < 4: # File too short or empty after creation
                initialize_agenda_file()
                return 0
            return struct.unpack("i", data)[0]
    except FileNotFoundError:
        initialize_agenda_file()
        return 0
    except Exception: # Catches other errors like struct.error if file is corrupted
        initialize_agenda_file()
        return 0

def read_agenda_items() -> list[AgendaItem]:
    """
    Calls get_sequential() to get the current max code (this also ensures the file exists).
    Opens AGENDA_FILE in binary read mode ("rb").
    Seeks past the first 4 bytes (the sequential number).
    Continuously reads chunks of data, each chunk being 164 bytes.
    For each chunk:
        Unpacks the data.
        Decodes string fields and removes trailing nulls.
        Creates an AgendaItem object.
        Appends to a list.
    Returns the list of AgendaItem objects.
    If FileNotFoundError, call initialize_agenda_file() and return an empty list.
    """
    _ = get_sequential() # Ensures file exists and initializes if needed.
    items = []
    record_size = struct.calcsize(STRUCT_FORMAT) # Should be 164

    try:
        with open(AGENDA_FILE, "rb") as f:
            f.seek(4) # Skip the sequential number
            while True:
                chunk = f.read(record_size)
                if not chunk or len(chunk) < record_size:
                    break
                
                unpacked_data = struct.unpack(STRUCT_FORMAT, chunk)
                
                codigo = unpacked_data[0]
                nome = unpacked_data[1].decode(STRING_ENCODING).rstrip('\x00')
                fone_fixo = unpacked_data[2].decode(STRING_ENCODING).rstrip('\x00')
                fone_celular = unpacked_data[3].decode(STRING_ENCODING).rstrip('\x00')
                fone_comercial = unpacked_data[4].decode(STRING_ENCODING).rstrip('\x00')
                
                items.append(AgendaItem(codigo, nome, fone_fixo, fone_celular, fone_comercial))
    except FileNotFoundError: # Should ideally be handled by get_sequential, but as a safeguard
        initialize_agenda_file()
        return []
    except Exception: # Catch other potential errors during read/unpack
        # For simplicity, if corruption is found, return what's read so far or an empty list.
        # A more robust solution might involve logging or specific error handling.
        return items # Or an empty list if preferred on any error: return []
        
    return items

def write_agenda_items(items: list[AgendaItem], seq: int):
    """
    Opens AGENDA_FILE in binary write mode ("wb").
    Packs and writes the seq (integer) to the start of the file.
    For each AgendaItem in the items list:
        Packs codigo.
        Encodes and pads/truncates string fields.
        Packs all fields into a single bytes object.
        Writes the packed record to the file.
    Closes the file.
    """
    with open(AGENDA_FILE, "wb") as f:
        f.write(struct.pack("i", seq))
        for item in items:
            packed_codigo = item.codigo
            packed_nome = item.nome.encode(STRING_ENCODING).ljust(100, b'\0')[:100]
            packed_fone_fixo = item.fone_fixo.encode(STRING_ENCODING).ljust(20, b'\0')[:20]
            packed_fone_celular = item.fone_celular.encode(STRING_ENCODING).ljust(20, b'\0')[:20]
            packed_fone_comercial = item.fone_comercial.encode(STRING_ENCODING).ljust(20, b'\0')[:20]
            
            record = struct.pack(
                STRUCT_FORMAT,
                packed_codigo,
                packed_nome,
                packed_fone_fixo,
                packed_fone_celular,
                packed_fone_comercial
            )
            f.write(record)
