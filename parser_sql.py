import struct
import os
import sys
from tkinter import Tk, filedialog, Button, Label, Entry, Checkbutton, IntVar, StringVar, Text, END, Scrollbar, RIGHT, Y
from optparse import OptionParser
import csv

# Function to remove the non-printable characters, tabs, and white spaces
def remove_ascii_non_printable(chunk):
    chunk = ' '.join(chunk.split())
    return ''.join([ch for ch in chunk if 31 < ord(ch) < 126 or ord(ch) == 9])

def parse_sqlite_file(infile, outfile, raw, printpages, output_text):
    try:
        with open(infile, "rb") as f, open(outfile, 'w', newline='') as output:
            output_text.insert(END, f"Processing file: {infile}\n")
            filesize = os.stat(infile).st_size
            f.seek(0)
            header = f.read(16)
            if "SQLite" not in header.decode('utf-8'):
                output_text.insert(END, "File does not appear to be an SQLite File\n")
                return

            pagesize = struct.unpack('>H', f.read(2))[0]
            offset = 0

            writer = csv.writer(output)
            if not raw:
                writer.writerow(["Type", "Offset", "Length", "Data"])

            while offset < filesize:
                f.seek(offset)
                flag = struct.unpack('>b', f.read(1))[0]

                if flag == 13:
                    freeblock_offset = struct.unpack('>h', f.read(2))[0]
                    num_cells = struct.unpack('>h', f.read(2))[0]
                    cell_offset = struct.unpack('>h', f.read(2))[0]
                    num_free_bytes = struct.unpack('>b', f.read(1))[0]
                    start = 8 + (num_cells * 2)
                    length = cell_offset - start
                    f.read(num_cells * 2)
                    unallocated = f.read(length)

                    if raw:
                        output.write(f"Unallocated, Offset {offset+start} Length {length}\nData:\n")
                        output.write(unallocated.decode('utf-8', errors='ignore'))
                        output.write("\n\n")
                    else:
                        unallocated = remove_ascii_non_printable(unallocated.decode('utf-8', errors='ignore'))
                        if unallocated:
                            writer.writerow(["Unallocated", offset + start, length, unallocated])

                    while freeblock_offset != 0:
                        f.seek(offset + freeblock_offset)
                        next_fb_offset = struct.unpack('>h', f.read(2))[0]
                        free_block_size = struct.unpack('>hh', f.read(4))[0]
                        f.seek(offset + freeblock_offset)
                        free_block = f.read(free_block_size)

                        if raw:
                            output.write(f"Free Block, Offset {offset+freeblock_offset}, Length {free_block_size}\nData:\n")
                            output.write(free_block.decode('utf-8', errors='ignore'))
                            output.write("\n\n")
                        else:
                            free_block = remove_ascii_non_printable(free_block.decode('utf-8', errors='ignore'))
                            if free_block:
                                writer.writerow(["Free Block", offset + freeblock_offset, free_block_size, free_block])

                        freeblock_offset = next_fb_offset

                elif printpages:
                    pagestring = f.read(pagesize - 1)
                    printable_pagestring = remove_ascii_non_printable(pagestring.decode('utf-8', errors='ignore'))

                    if raw:
                        output.write(f"Non-Leaf-Table-Btree-Type_{flag}, Offset {offset}, Length {pagesize}\nData:\n")
                        output.write(printable_pagestring)
                        output.write("\n\n")
                    else:
                        writer.writerow([f"Non-Leaf-Table-Btree-Type_{flag}", offset, pagesize, printable_pagestring])

                offset += pagesize

            output_text.insert(END, "Parsing completed successfully.\n")
    except Exception as e:
        output_text.insert(END, f"An error occurred: {e}\n")

def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("SQLite files", "*.db"), ("All files", "*.*")])
    entry.set(filename)

def browse_output(entry):
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    entry.set(filename)

def run_parser(input_entry, output_entry, raw_var, printpages_var, output_text):
    infile = input_entry.get()
    outfile = output_entry.get()
    raw = bool(raw_var.get())
    printpages = bool(printpages_var.get())

    if not infile or not outfile:
        output_text.insert(END, "Please select both input and output files.\n")
        return

    output_text.delete(1.0, END)
    parse_sqlite_file(infile, outfile, raw, printpages, output_text)

# GUI Setup
root = Tk()
root.title("SQLite Parser")

input_entry = StringVar()
output_entry = StringVar()
raw_var = IntVar()
printpages_var = IntVar()

Label(root, text="Input SQLite file:").grid(row=0, column=0, sticky='e')
Entry(root, textvariable=input_entry, width=50).grid(row=0, column=1)
Button(root, text="Browse", command=lambda: browse_file(input_entry)).grid(row=0, column=2)

Label(root, text="Output file:").grid(row=1, column=0, sticky='e')
Entry(root, textvariable=output_entry, width=50).grid(row=1, column=1)
Button(root, text="Browse", command=lambda: browse_output(output_entry)).grid(row=1, column=2)

Checkbutton(root, text="Raw output", variable=raw_var).grid(row=2, column=0, columnspan=2, sticky='w')
Checkbutton(root, text="Print pages", variable=printpages_var).grid(row=2, column=1, columnspan=2, sticky='w')

Button(root, text="Run Parser", command=lambda: run_parser(input_entry, output_entry, raw_var, printpages_var, output_text)).grid(row=3, column=0, columnspan=3)

output_text = Text(root, height=15, width=80)
output_text.grid(row=4, column=0, columnspan=3, pady=5)
scrollbar = Scrollbar(root, command=output_text.yview)
scrollbar.grid(row=4, column=3, sticky='nsew')
output_text['yscrollcommand'] = scrollbar.set

root.mainloop()
