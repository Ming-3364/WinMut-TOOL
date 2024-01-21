# Makefile
SHELL = /bin/bash
SRC_DIR = src
BIN_DIR = bin

SRC_FILES = $(wildcard $(SRC_DIR)/*.c)
EXECUTABLES = $(patsubst $(SRC_DIR)/%.c,$(BIN_DIR)/%,$(SRC_FILES))
all: $(EXECUTABLES)

$(BIN_DIR)/%: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

# TEST
test:
	
	# -------------------------- 1_expr_clac ---------------------------------
	# ./$(BIN_DIR)/1_expr_clac
	# -------------------------- 1_expr_clac ---------------------------------
	
	# -------------------------- 2_icmp ---------------------------------
	# ./$(BIN_DIR)/2_icmp
	# -------------------------- 2_icmp ---------------------------------

	# -------------------------- file_sys ---------------------------------
	# echo "0 0" | ./$(BIN_DIR)/file_sys_without_goodvar

	# -------------------------- mut_output-carrymut ---------------------------------
	# -./$(BIN_DIR)/mut_output-carrymut		已弃用，见demo

	# -------------------------- quick_sort ---------------------------------
	# -./$(BIN_DIR)/quick_sort				已弃用，见demo

	# ----------------------- demo ----------------------------
	-./$(BIN_DIR)/demo-bubble_sort
	-echo "5" | ./$(BIN_DIR)/demo-fibonacci
	-./$(BIN_DIR)/demo-mut_output-carrymut
	-./$(BIN_DIR)/demo-quick_sort
	-./$(BIN_DIR)/demo-reverse_string


	# -------------------------- multi-cond if ---------------------------------

	# echo "33 33 33" | ./$(BIN_DIR)/m-cond-if
	# echo "0 0" | ./$(BIN_DIR)/goodvar
	
	# -------------------------- mutrepeat ---------------------------------

	# echo -e "1 2\n3 4" | ./$(BIN_DIR)/mutrepeat
	# echo -e "1 2\n3 4" | ./$(BIN_DIR)/mutrepeat
	# echo -e "1 2\n3 4" | ./$(BIN_DIR)/mutrepeat
	# echo -e "1 2\n3 4" | ./$(BIN_DIR)/mutrepeat

	# echo -e "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# echo -e "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# echo -e "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# echo -e "1 2 3 4" | ./$(BIN_DIR)/mutrepeat

	# echo -e "1 2\n3 4" > tmpf1 ; ./$(BIN_DIR)/mutrepeat < tmpf1
	# echo -e "1 2\n3 4" > tmpf2 ; ./$(BIN_DIR)/mutrepeat < tmpf2
	# echo -e "1 2\n3 4" > tmpf3 ; ./$(BIN_DIR)/mutrepeat < tmpf3
	# echo -e "1 2\n3 4" > tmpf4 ; ./$(BIN_DIR)/mutrepeat < tmpf4

	# echo -e "1 2 3 4" > tmpf5 ; ./$(BIN_DIR)/mutrepeat < tmpf5
	# echo -e "1 2 3 4" > tmpf6 ; ./$(BIN_DIR)/mutrepeat < tmpf6
	# echo -e "1 2 3 4" > tmpf7 ; ./$(BIN_DIR)/mutrepeat < tmpf7
	# echo -e "1 2 3 4" > tmpf8 ; ./$(BIN_DIR)/mutrepeat < tmpf8

	# echo  "1 2\n3 4" > tmpf1 ; ./$(BIN_DIR)/mutrepeat < tmpf1
	# echo  "1 2\n3 4" > tmpf2 ; ./$(BIN_DIR)/mutrepeat < tmpf2
	# echo  "1 2\n3 4" > tmpf3 ; ./$(BIN_DIR)/mutrepeat < tmpf3
	# echo  "-e 1 2 3 4" > tmpf4 ; ./$(BIN_DIR)/mutrepeat < tmpf4

	# echo  "1 2 3 4" > tmpf5 ; ./$(BIN_DIR)/mutrepeat < tmpf5
	# echo  "1 2 3 4" > tmpf6 ; ./$(BIN_DIR)/mutrepeat < tmpf6
	# echo  "1 2 3 4" > tmpf7 ; ./$(BIN_DIR)/mutrepeat < tmpf7
	# echo  "1 2 3 4" > tmpf8 ; ./$(BIN_DIR)/mutrepeat < tmpf8

	# echo  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# echo  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# echo  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# echo  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat

	# printf  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# printf  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# printf  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat
	# printf  "1 2 3 4" | ./$(BIN_DIR)/mutrepeat

	# printf  "1 2 3 5" | tr '5' '4' | ./$(BIN_DIR)/mutrepeat
	# printf  "1 2 3 5" | tr '5' '4' | ./$(BIN_DIR)/mutrepeat
	# printf  "1 2 3 5" | tr '5' '4' | ./$(BIN_DIR)/mutrepeat
	# printf  "1 2 3 5" | tr '5' '4' | ./$(BIN_DIR)/mutrepeat


	

# 清理规则
clean:
	rm -f $(EXECUTABLES) 
	rm -f $(SRC_DIR)/*.ll $(SRC_DIR)/*.mut $(SRC_DIR)/*.stat

clean-mut_output:
	rm -f mut_output-*

