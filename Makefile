VERSION=$(shell python3 -c "import getctstream; print getctstream.__version__")

help:
	@echo "To run raw script: \n\tmake run"
	@echo "To build Kodi plugin: \n\tmake build_kodi"
	@echo "To install: \n\tmake install"
	@echo "To install debian dependencies: \n\tmake install_dep_debian"
	@echo "To clean: \n\tmake clean"

run:
	python get_ct_stream.py

install: clean
	sudo python3 setup.py build install

uninstall:
	sudo pip3 uninstall -y getctstream

reinstall: uninstall install

install_dep_debian:
	sudo apt-get install python3 python3-pip
	sudo pip3 install requests

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
