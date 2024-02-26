
print("Podaj nazwę pliku tekstowego:")
path = input()
with open(path, "r") as f:
    with open("lab1zad1.txt", "w") as newfile:
        newfile.write(f.read())

