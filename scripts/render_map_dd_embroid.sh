#! /bin/bash
gimp -i -b '(python-fu-create-gimpmap RUN-NONINTERACTIVE
	"config_dd_embroid_map.json" "map"
)' '(gimp-quit 1)'