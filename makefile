MODULENAME=skygp

help:
	@echo ""
	@echo "Welcome to skygp!!!"
	@echo "To get started create an environment using:"
	@echo "	make init"
	@echo "	conda activate ./envs"
	@echo "  source activate ./envs"
	@echo ""
	@echo "To generate project documentation use:"
	@echo "	make doc"
	@echo ""
	@echo "To Lint the project use:"
	@echo "	make lint"
	@echo ""
	@echo "To run unit tests use:"
	@echo "	make test"
	@echo ""
	
init:
	conda env create --prefix ./envs --file environment.yml

doc:
	bash run_doc.sh $(MODULENAME)

lint:
	pylint $(MODULENAME)

test:
	pytest -v $(MODULENAME)/__tests__/

.PHONY: init doc lint test 

