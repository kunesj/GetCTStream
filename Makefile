
help:
	@echo "To build Kodi plugin run: make build_kodi"
	
run:
	python2 get_ct_stream.py

build_kodi: prepare_to_build
	cp -r Kodi/plugin.video.streamct build/
	cp -r get_ct_stream.py build/plugin.video.streamct
	rm -f dist/kodi_plugin.video.streamct.zip
	cd build; zip -r ../dist/kodi_plugin.video.streamct.zip plugin.video.streamct 

prepare_to_build:
	rm -rf build
	mkdir -p build dist

clean:
	rm -rf dist build
