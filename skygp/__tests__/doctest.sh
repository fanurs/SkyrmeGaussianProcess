# This script runs all the .py files in skygp with doctest except __init__.py
# If the following command doesn't work,
#		$ ./doctest.sh
# try
#		$ bash doctest.sh

for python_file in ../*.py
do
	basename=$(basename -- $python_file)
	if [[ $basename == '__init__.py' ]]
	then
		echo 'skipping ' $python_file
		continue
	else
		echo 'doctesting ' $python_file
		python -m doctest -o ELLIPSIS $python_file
	fi
done
