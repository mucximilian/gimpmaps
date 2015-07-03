#! /bin/bash
gimp -i -b '(python-fu-create-pgsvg-map RUN-NONINTERACTIVE
	"config_dd_embroid.json"
)' '(gimp-quit 1)'