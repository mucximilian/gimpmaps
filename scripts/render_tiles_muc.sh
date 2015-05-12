#! /bin/bash
gimp -i -b '(python-fu-create-pgsvg-tiles RUN-NONINTERACTIVE
	12
	12
	1250000
	6160000
	1310000
	6080000
	256
	1
	TRUE
)' '(gimp-quit 1)'