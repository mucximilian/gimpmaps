#! /bin/bash
gimp -i -b '(python-fu-create-pgsvg-map RUN-NONINTERACTIVE
	1275000
	6131500
	1289700
	6118200
	10000
	"test_tiles.json"
	TRUE
)' '(gimp-quit 1)'