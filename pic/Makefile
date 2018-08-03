test:
	./sortpics.py add $(HOME)/Pictures
	sqlite3 sortpics.db  .dump

themedir:
	if [ ! -d themes ]; then \
		git clone --recursive https://github.com/spf13/hugoThemes.git themes; \
	fi




hugo: 
	rm -rf test
	hugo new site test
	cd test; git init; ln -s $(CURDIR)/gengallery/base16 themes/base16; 
	echo 'baseURL = "http://192.168.128.46:1313/"' > test/config.toml 
	echo 'languageCode = "en-us"'             >>test/config.toml 
	echo 'title = "Gallery"'                  >>test/config.toml 
	echo 'theme = "base16"'                   >>test/config.toml 
	mkdir -p test/layouts/shortcodes
	mkdir -p test/work/img
	mkdir -p test/public/ 
	mkdir -p test/content/img
	mkdir -p test/static/jss test/static/css test/static/data
	cp gengallery/PhotoSwipe/dist/*js test/static/jss/
	cp gengallery/PhotoSwipe/dist/*css test/static/css/
	cp -r gengallery/PhotoSwipe/dist/default-skin test/static/css/
	touch test/content/img/_index.md
	cp -r t/2013-08-16 test/static/data/
	cp -r t/2013-10-10 test/static/data/
	python3 gengallery.py --hugo test/content/img/ test/static/data/
	cp gengallery/photo.html test/layouts/shortcodes/
	cd test; \
	hugo 

server:
	cd $(CURDIR)/test/public; python $(CURDIR)/server.py

gen:
	python gengallery.py t/

#
# cd $(CURDIR)/test/; hugo

prepare:
	sudo apt-get install exiftool hugo

clean:
	rm sortpics.db

.PHONY: test
