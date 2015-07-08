#! /bin/bash
gimp -i -b '(python-fu-create-pgsvg-map RUN-NONINTERACTIVE
	"config_dd_embroid_map.json"
)' '(gimp-quit 1)'