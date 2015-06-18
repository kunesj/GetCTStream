VERSION=$(shell python -c "import getctstream; print getctstream.__version__")

help:
	@echo "To run raw script: \n\tmake run"
	@echo "To build Kodi plugin: \n\tmake build_kodi"
	@echo "To clean: \n\tmake clean"
	
run:
	python get_ct_stream.py

install: clean
	sudo python setup.py build install

install_dep_debian:
	sudo apt-get install python python-pip
	sudo pip install requests beautifulsoup4

build_kodi: clean
	rm -f *kodi.zip
	mkdir -p build/plugin.video.streamct
	
	cp -r Kodi/plugin.video.streamct build/
	cp Kodi/KODI_README.md build/
	cp getctstream/get_ct_stream.py build/plugin.video.streamct
	
	sed -i -e 's/__VERSION__/$(VERSION)/g' build/plugin.video.streamct/addon.xml
	
	cd build; zip -r plugin.video.streamct.zip plugin.video.streamct
	cd build; zip -r ../get_ct_stream_kodi.zip plugin.video.streamct.zip KODI_README.md

clean:
	sudo rm -rf build dist getctstream.egg-info
