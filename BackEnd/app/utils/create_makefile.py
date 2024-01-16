import os

def getMakeList(run_case_list):
    makeList = []
    return makeList

def getMakeTest(run_case_list):
    makeTest = ["quick_sort	12 35 45 64", "quick_sort	12 35"]
    makeTest = []
    for run_case in run_case_list:
        print(run_case)
        run_file = run_case['file']
        run_argv = run_case['argv']

        makeTest.append(run_file + " " + run_argv)
    return makeTest

def generateMakefile(run_dir_path, run_case_list):
    makefile_path = os.path.join(run_dir_path, "makefile")
    makeList = getMakeList(run_case_list)
    makeTest = getMakeTest(run_case_list)

    with open(makefile_path, 'w') as file:
        file.write("SHELL = /bin/bash\n")
        file.write("SRC_DIR = src\n")
        file.write("BIN_DIR = bin\n")
        file.write("\n")

        file.write("SRC_FILES = $(wildcard $(SRC_DIR)/*.c)\n")
        file.write("EXECUTABLES = $(patsubst $(SRC_DIR)/%.c,$(BIN_DIR)/%,$(SRC_FILES))\n")
        file.write("all: $(EXECUTABLES)\n")
        file.write("\n")
        file.write("$(BIN_DIR)/%: $(SRC_DIR)/%.c\n")
        file.write("	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<\n")
        
        file.write("\n")
        file.write("test:\n")
        for t in makeTest:
            file.write("	./$(BIN_DIR)/" + t + "\n")
        file.write("\n")



