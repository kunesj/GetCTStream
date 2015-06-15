
help:
	@echo "To run raw script: \n\tmake run"
	@echo "To build Kodi plugin: \n\tmake build_kodi"
	@echo "To clean: \n\tmake clean"
	
run:
	python2 get_ct_stream.py

build_kodi: prepare_to_build
	rm -f dist/*kodi.zip
	
	cp -r Kodi/plugin.video.streamct build/
	cp Kodi/KODI_README.md build/
	cp get_ct_stream.py build/plugin.video.streamct
	
	cd build; zip -r plugin.video.streamct.zip plugin.video.streamct
	cd build; zip -r ../dist/get_ct_stream_kodi.zip plugin.video.streamct.zip KODI_README.md

prepare_to_build:
	rm -rf build
	mkdir -p build dist

clean:
	rm -rf dist build
