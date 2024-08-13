import ctypes

# Example shellcode (this is a benign shellcode for demonstration; it will not do anything malicious)
# This is just a placeholder. Replace with your own.
SHELLCODE = b"\x90\x90\x90"  # NOP sled, non-functional

def run_shellcode(shellcode):
    shellcode = bytearray(shellcode)
    # Allocate memory with PAGE_EXECUTE_READWRITE permissions
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                              ctypes.c_int(len(shellcode)),
                                              ctypes.c_int(0x3000),
                                              ctypes.c_int(0x40))
    # Copy shellcode to allocated memory
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                         shellcode,
                                         ctypes.c_int(len(shellcode)))

    # Create a function pointer to the shellcode
    shell_func = ctypes.CFUNCTYPE(ctypes.c_void_p)(ptr)
    
    # Call the function pointer, effectively running the shellcode
    shell_func()

if __name__ == "__main__":
    run_shellcode(SHELLCODE)
