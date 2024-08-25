import os

# Ścieżka do folderu, w którym znajdują się pliki
folder_path = "Cześć 2"

# Przechodzimy przez wszystkie pliki w folderze
for i in range(100):
    old_name = f"{i}.avi"
    new_name = f"{i + 100}.avi"

    # Pełne ścieżki do plików
    old_file_path = os.path.join(folder_path, old_name)
    new_file_path = os.path.join(folder_path, new_name)

    # Zmiana nazwy pliku
    if os.path.exists(old_file_path):
        os.rename(old_file_path, new_file_path)
        print(f"Zmieniono nazwę {old_name} na {new_name}")
    else:
        print(f"Plik {old_name} nie istnieje")
