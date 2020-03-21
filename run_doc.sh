# This script runs pdoc3 and updates __init__.py
# Since the index.html takes docstring from __init__.py,
# this script simply copy and paste everything from README.md to __init__.py
# so that index.html would show a nice README page.
# Run this script as below:
#		$ ./run_doc.sh skygp
# If it doesn't work, try:
#		$ bash run_doc.sh skygp

# arguments handling
basename=$(basename $1)

# copy & paste README.md to __init__.py as docstring
cat README.md > $basename/__init__.py
sed -i '1i """' $basename/__init__.py
echo '"""' >> $basename/__init__.py

# auto-documentation with pdoc3
pdoc3 --force --html --config latex_math=True --output-dir ./docs $basename

# import all modules under skygp to __init__.py
for file in skygp/*.py
do
	filebase=$(basename $file .py)
	if [[ $filebase == "__init__" ]]
	then
		continue
	else
		echo 'from .'$filebase' import '* >> $basename/__init__.py
	fi
done

# place all *.html right under ./docs for auto generation of gihub.io
mv ./docs/$basename/*.html ./docs
