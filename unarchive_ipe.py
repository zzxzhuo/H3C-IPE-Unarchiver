import sys, re, os
regex = b"(?i)\x00[\w\-\d]*\.bin\x00"
filename_chunk_size = 224
content_header_size = 12
'''
The actual file before packaging is 224+12 bytes after
where its filename is stored.
filename_offset corresponds to the starting position of
the name of an archived file.
'''
def get_file_size_int(in_file, filename_offset, is_littleendian):
    content_header_offset = filename_offset + filename_chunk_size
    in_file.seek(content_header_offset)
    hex_filesize = ""
    # the file size is stored in a 4 byte chunk with order w.r.t. to devices' endian
    if is_littleendian:
        for i in range(4):
            hex_filesize = in_file.read(1).hex() + hex_filesize
    else:
        for i in range(4):
            hex_filesize = hex_filesize + in_file.read(1).hex()
    in_file.seek(0) # reset seeking
    return int(hex_filesize, 16)

def extract_bytes_from_offset(in_file, filename_offset, size):
    local_offset_int = filename_offset + filename_chunk_size + content_header_size
    in_file.seek(local_offset_int)
    return in_file.read(size)

def get_filename_at_offset(in_file, filename_offset):
    filename = ""
    in_file.seek(filename_offset)
    current_hex = in_file.read(1).hex()
    while current_hex != '00':
        filename += current_hex
        current_hex = in_file.read(1).hex()
    in_file.seek(0)
    return bytes.fromhex(filename).decode("utf-8")

def check_file_endian(in_file, filename_offset):
    in_file.seek(filename_offset - 57)
    current_hex = in_file.read(1).hex()
    in_file.seek(0)
    # if the ipe content header consists \0xff then the filesize is encoded in little endian
    return current_hex == 'ff'

if __name__ == "__main__":
    infile_path = sys.argv[1]
    infile_size = os.path.getsize(infile_path)
    seeked_bytes = 0 # so far how many bytes have been processed
    with open(infile_path, "rb") as raw_ipe:
        while seeked_bytes < infile_size:
            raw_ipe.seek(seeked_bytes) # move to next archived file
            next_match = re.search(regex, raw_ipe.read())
            if next_match == None:
                print("Done.")
                break
            next_filename_offset = seeked_bytes + next_match.start() + 1 # starting location of the continuing .bin, ignore dummy \x00 when doing regex matching
            archived_filesize = get_file_size_int(raw_ipe, next_filename_offset, check_file_endian(raw_ipe, next_filename_offset))
            seeked_bytes = next_filename_offset + filename_chunk_size + content_header_size + archived_filesize
            archived_filename = get_filename_at_offset(raw_ipe, next_filename_offset)
            print("Found " + archived_filename + ", extracting...")
            outfile_path = os.path.join("out", archived_filename)
            if not os.path.exists(os.path.dirname(outfile_path)):
                os.makedirs(os.path.dirname(outfile_path))
            with open(outfile_path, "wb") as out_data:
                out_data.write(extract_bytes_from_offset(raw_ipe, next_filename_offset, archived_filesize))
            raw_ipe.seek(0)
