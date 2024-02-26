print("Podaj nazwę pliku graficznego:")
path = input()
with open(path, "rb") as f:
    with open("lab1zad2.png", "wb") as newfile:
        newfile.write(f.read())