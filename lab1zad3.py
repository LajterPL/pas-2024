def is_ip_valid():
    print("Podaj adres IP:")
    string = input()

    string = string.split(".")
    if len(string) != 4:
        return False

    for x in string:
        try:
            if int(x) < 0 or int(x) > 255:
                return False
        except:
            return False

    return True

print(is_ip_valid())