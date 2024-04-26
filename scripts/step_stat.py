def print_stat(file0_path, file1_path, file2_path):    
    with open(file0_path, 'r') as file0:
        lines_file0 = sum(1 for line in file0)

    with open(file1_path, 'r') as file1:
        lines_file1 = sum(1 for line in file1)
    
    with open(file2_path, 'r') as file2:
        lines_file2 = sum(1 for line in file2)

    
    percentage_decrease = round((100 * (lines_file1 - lines_file2)) / lines_file1, 2)
    
    result_percentage_dtecrease = round((100 * (lines_file0 - lines_file2)) / lines_file0, 2)
    
    print(f"Количество строк в {file1_path}: {lines_file1}")
    print(f"Количество строк в {file2_path}: {lines_file2}")
    print(f"Отфильтровано строк: {lines_file1 - lines_file2}")    
    print(f"Потери данных за этот шаг составили по отношению к предыдущему {percentage_decrease} %.")
    print('------------')
    print(f"Общие потери данных {result_percentage_dtecrease} %.")