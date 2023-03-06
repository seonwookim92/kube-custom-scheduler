# Request size unit conversion
# There exists three types of unit: Ki, Mi, Gi
# The unit is used to represent the size of memory
# Returns the size in Ki
def convert_unit(size):
    if size[-2:] == "Ki":
        return int(size[:-2])
    elif size[-2:] == "Mi":
        return int(size[:-2]) * 1024
    elif size[-2:] == "Gi":
        return int(size[:-2]) * 1024 * 1024
    else:
        raise Exception("Invalid unit")