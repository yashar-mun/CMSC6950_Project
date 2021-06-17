report.pdf: report.tex hexbin_argos_locations.png map_of_locations.png correlation1.png correlation2.png correlation3.png correlation4.png
	latexmk -pdf

hexbin_argos_locations.png: 2d_density_argos_locations.py
	python3 2d_density_argos_locations.py

map_of_locations.png: correlation_between_variables.py
	python3 correlation_between_variables.py

correlation1.png: correlation_between_variables.py
	python3 correlation_between_variables.py

correlation2.png: correlation_between_variables.py
	python3 correlation_between_variables.py

correlation3.png: correlation_between_variables.py
	python3 correlation_between_variables.py

correlation4.png: correlation_between_variables.py
	python3 correlation_between_variables.py

clean:
	rm *.png
	latexmk -c

.PHONY : clean

deepclean:
	rm *.png
	latexmk -c
	rm *.pdf

.PHONY : deepclean

pdfclean:
	rm *.pdf

.PHONY : pdfclean